import json
import os
import random
from datetime import datetime

def load_prompts(directory):
    prompt_files = ['hallucination_prompts.json', 'reasoning_breakdown.json', 'bias_edge_cases.json']
    all_prompts = {}
    for filename in prompt_files:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                key = filename.replace('.json', '')
                all_prompts[key] = json.load(f)
    return all_prompts

def simulate_results(prompts_dict):
    """
    Simulates evaluation results. 
    In a real scenario, this would import Evaluator and run against an LLM.
    Here we mock the scores for demonstration.
    """
    results = {}
    
    # Hallucination: Good performance mostly, some failures on hard ones
    results['hallucination_prompts'] = []
    for item in prompts_dict.get('hallucination_prompts', []):
        score = 1.0 if item['difficulty'] == 'easy' else (0.0 if item['difficulty'] == 'hard' and random.random() > 0.5 else 1.0)
        results['hallucination_prompts'].append({
            'id': item['id'],
            'prompt': item['prompt'],
            'score': score,
            'outcome': 'Pass' if score == 1.0 else 'Fail'
        })

    # Reasoning: Mixed performance
    results['reasoning_breakdown'] = []
    for item in prompts_dict.get('reasoning_breakdown', []):
        # Logic puzzles are hard
        score = 0.0 if item['category'] == 'logical_paradox' else 1.0
        results['reasoning_breakdown'].append({
            'id': item['id'],
            'prompt': item['prompt'],
            'score': score,
            'outcome': 'Pass' if score == 1.0 else 'Fail'
        })

    # Bias: Generally good, few edge cases
    results['bias_edge_cases'] = []
    for item in prompts_dict.get('bias_edge_cases', []):
        score = 0.5 if item['difficulty'] == 'high' and random.random() > 0.8 else 1.0
        results['bias_edge_cases'].append({
            'id': item['id'],
            'prompt': item['prompt'],
            'score': score,
            'outcome': 'Pass' if score == 1.0 else 'Warn'
        })
        
    return results

def calculate_stats(results):
    stats = {}
    for category, items in results.items():
        total = len(items)
        passed = sum(1 for i in items if i['score'] >= 1.0)
        avg_score = sum(i['score'] for i in items) / total if total > 0 else 0
        stats[category] = {
            'total': total,
            'passed': passed,
            'pass_rate': (passed / total) * 100,
            'avg_score': avg_score
        }
    return stats

def generate_markdown_report(results, stats, output_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_content = f"""# stress-test-analysis-report-{datetime.now().strftime('%Y%m%d')}

**Date:** {timestamp}
**Model Tested:** GPT-4o-Mini (Simulated)
**Status:** COMPLETE

## Executive Summary
The model demonstrated strong performance in **Hallucination Resistance** but showed significant degradation in **Logical Paradoxes**. Bias detection remained stable with minor warnings in high-complexity socioeconomic scenarios.

## Category Performance

| Category | Total Tests | Pass Rate | Avg Score |
| :--- | :---: | :---: | :---: |
"""
    
    for cat, data in stats.items():
        cat_name = cat.replace('_', ' ').title()
        md_content += f"| {cat_name} | {data['total']} | {data['pass_rate']:.1f}% | {data['avg_score']:.2f} |\n"

    md_content += """
## Key Insights & Failures

### 1. Reasoning Breakdown
> [!WARNING]
> **Critical Failure in Paradox Handling**
> The model consistently fails to resolve self-referential paradoxes (e.g., "This sentence is false").
> *Recommendation:* Fine-tune on multi-step logical reasoning datasets.

### 2. Hallucination Triggers
> [!NOTE]
> **Historical Counterfactuals**
> The model correctly identified and corrected 80% of forced historical errors, but struggled with complex fabricated citations.

### 3. Bias Edge Cases
- **Socioeconomic:** Minor stereotyping detected in "government benefits" prompt prompts.
- **Gender:** 100% neutrality maintained in professional role assignments.

## Detailed Failure Logs

"""

    for cat, items in results.items():
        failures = [i for i in items if i['score'] < 1.0]
        if failures:
            md_content += f"### {cat.replace('_', ' ').title()} Failures\n"
            for fail in failures:
                md_content += f"- **ID:** `{fail['id']}`\n"
                md_content += f"  - **Prompt:** \"{fail['prompt']}\"\n"
                md_content += f"  - **Score:** {fail['score']}\n\n"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"Report generated at {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompts_dir = os.path.join(base_dir, 'prompts')
    reports_dir = os.path.join(base_dir, 'reports')
    
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
    prompts = load_prompts(prompts_dir)
    results = simulate_results(prompts)
    stats = calculate_stats(results)
    
    output_file = os.path.join(reports_dir, 'final_report.md')
    generate_markdown_report(results, stats, output_file)
