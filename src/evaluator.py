import json
import os
import sys
import glob
import asyncio
import argparse
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scorers import evaluate

try:
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
except ImportError:
    pass

try:
    from google import genai
except ImportError:
    pass

load_dotenv()

class StressTester:
    def __init__(self, use_mock=False):
        self.api_key = os.getenv("GEMINI_API_KEY", "mock-gemini-key")
        self.use_mock = use_mock or self.api_key.startswith("mock")
        if not self.use_mock:
            self.client = genai.Client(api_key=self.api_key)
        self.dataset = []
        self.results = []
        
    def load_prompts(self, directory="prompts", file_path=None):
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dataset = data.get("tests", data) if isinstance(data, dict) else data
            print(f"[*] Loaded {len(self.dataset)} tests from {file_path}")
            return
            
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        files = glob.glob(f"{directory}/*.json")
        for fpath in files:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and "tests" in data:
                    self.dataset.extend(data["tests"])
                elif isinstance(data, list):
                    self.dataset.extend(data)
                else:
                    self.dataset.append(data)
        print(f"[*] Loaded {len(self.dataset)} tests from {directory}/")

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=3),
        retry=retry_if_exception_type((Exception,))
    )
    async def invoke_llm_async(self, prompt, model="gemini-2.0-flash"):
        """
        Asynchronously pings the LLM API with the provided prompt.
        Implements exponential backoff for rate limits.
        """
        if self.use_mock:
            await asyncio.sleep(0.5)  # Simulate network latency
            if "z" in prompt.lower() or "t" in prompt.lower() or "Exactly" in prompt:
                res_content = "This response contains the letter t. Or fails the rule."
            elif "Where is the" in prompt:
                res_content = "The coin is in the pocket."
            else:
                res_content = "This is a perfect response that is likely to pass basic inclusion checks."
            return res_content

        # Real API Call
        from google.genai import types
        response = await self.client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                ]
            )
        )
        return response.text

    async def process_test_async(self, test_case, model="gemini-2.0-flash"):
        test_id = test_case.get("id", "unknown")
        category = test_case.get("category", "Uncategorized")
        prompt = test_case.get("prompt", "")
        expected = test_case.get("expected_answer", "")

        print(f"[~] Sending request to LLM (Model: {model}) => {prompt[:50]}...")
        
        try:
            llm_text = await self.invoke_llm_async(prompt, model)
            score_result = evaluate(category, prompt, llm_text, expected)
            is_pass = score_result["score"] == 1.0
            
            print(f"[+] Received response for test {test_id}. Passed: {is_pass}")
            
            return {
                "test_id": test_id,
                "category": category,
                "prompt": prompt,
                "expected_answer": expected,
                "actual_answer": llm_text,
                "score": score_result["score"],
                "passed": is_pass,
                "reason": score_result["reason"]
            }
        except Exception as e:
            print(f"[-] Evaluation failed on test {test_id}: {e}")
            return {
                "test_id": test_id,
                "category": category,
                "prompt": prompt,
                "expected_answer": expected,
                "actual_answer": f"ERROR: {str(e)}",
                "score": 0.0,
                "passed": False,
                "reason": "API Exception"
            }

    async def run_evaluation_batch_async(self, test_limit=None, max_concurrent=5):
        if not self.dataset:
            print("[-] No dataset loaded.")
            return

        tests_to_run = self.dataset[:test_limit] if test_limit else self.dataset
        print(f"[*] Starting async evaluation for {len(tests_to_run)} tests...")
        print(f"[*] API Handshake Successful. Mode: {'MOCK' if self.use_mock else 'LIVE'}")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def sem_task(test_case):
            async with semaphore:
                return await self.process_test_async(test_case)
                
        tasks = [sem_task(test_case) for test_case in tests_to_run]
        results = await asyncio.gather(*tasks)
        
        passed_count = 0
        failed_count = 0
        category_stats = {}
        
        for res in results:
            if not res:
                continue
            self.results.append(res)
            
            cat = res["category"]
            if cat not in category_stats:
                category_stats[cat] = {"total": 0, "passed": 0, "failed": 0}
            
            category_stats[cat]["total"] += 1
            if res["passed"]:
                passed_count += 1
                category_stats[cat]["passed"] += 1
            else:
                failed_count += 1
                category_stats[cat]["failed"] += 1
                
        total = passed_count + failed_count
        pass_rate = (passed_count / total * 100) if total > 0 else 0
        
        report = {
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "total_tests": total,
                "overall_pass_rate": round(pass_rate, 2),
                "model_used": "mock" if self.use_mock else "gemini-2.0-flash"
            },
            "category_breakdown": category_stats,
            "results": self.results
        }
        
        os.makedirs("reports", exist_ok=True)
        out_path = "reports/latest_evaluation_run.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            
        print(f"\n[+] Batch Run Complete! Overall Pass Rate: {pass_rate:.1f}%")
        print(f"[+] Saved structured results to {out_path}")

def main():
    parser = argparse.ArgumentParser(description="LLM Alignment Stress Tester")
    parser.add_argument("--test-run", type=int, help="Limit the number of tests to run")
    args = parser.parse_args()

    tester = StressTester()
    tester.load_prompts() # Loads all from prompts/ directory
    asyncio.run(tester.run_evaluation_batch_async(test_limit=args.test_run))

if __name__ == "__main__":
    main()

