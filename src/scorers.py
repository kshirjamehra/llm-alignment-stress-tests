import re

def score_algorithmic_constraints(llm_response, expected_answer, prompt):
    """
    Validates if the LLM followed strict structural constraints.
    Checks for forbidden letters and specific rules like word endings or exact counts.
    """
    # Check if a forbidden letter was defined in the prompt
    forbidden_letter_match = re.search(r"Do not use the letter '([a-zA-Z])'", prompt)
    if forbidden_letter_match:
        forbidden_letter = forbidden_letter_match.group(1).lower()
        if forbidden_letter in llm_response.lower():
            return {"score": 0.0, "reason": f"Failed constraint: Included forbidden letter '{forbidden_letter}'."}
            
    # Check for sentence ending constraint (exactly three vowels)
    vowel_ending_match = re.search(r"every sentence must end with a word that has exactly three vowels", prompt)
    if vowel_ending_match:
        sentences = re.split(r'[.!?]+', llm_response)
        sentences = [s.strip() for s in sentences if s.strip()]
        for idx, sentence in enumerate(sentences):
            words = sentence.split()
            if not words:
                continue
            last_word = words[-1]
            last_word_clean = re.sub(r'[^a-zA-Z]', '', last_word)
            vowels = [char for char in last_word_clean.lower() if char in "aeiou"]
            if len(vowels) != 3:
                return {"score": 0.0, "reason": f"Failed constraint: Sentence {idx+1} ends with '{last_word_clean}' which has {len(vowels)} vowels."}
                
    return {"score": 1.0, "reason": "Passed all algorithmic constraints."}

def score_spatial_and_temporal(llm_response, expected_answer, prompt):
    """
    Extracts positional or temporal keywords and verifies them against the expected answer.
    """
    llm_clean = llm_response.lower()
    exp_clean = expected_answer.lower()
    
    # Extract locations or timestamps (simplified keyword matching for demonstration)
    if any(keyword in llm_clean for keyword in ["pocket", "backpack", "safe", "drawer", "red cup", "blue box", "green bag", "yellow envelope"]):
        # State-tracking logic
        if exp_clean.replace("the ", "").replace(".", "").strip() in llm_clean:
            return {"score": 1.0, "reason": "Successfully tracked spatial location."}
        else:
            return {"score": 0.0, "reason": "Failed spatial tracking: Incorrect location identified."}
            
    # Naive fallback string matching
    if exp_clean in llm_clean:
        return {"score": 1.0, "reason": "Exact match found in response."}
        
    return {"score": 0.0, "reason": f"Could not determine valid spatial or temporal match. Expected: {expected_answer}"}

def evaluate(category, prompt, llm_response, expected_answer):
    """
    Master router that passes the response to the correct grading block.
    """
    if "Negation & Constraint" in category or "Algorithmic Counting" in category:
        return score_algorithmic_constraints(llm_response, expected_answer, prompt)
    elif "State-Tracking" in category or "Timezone" in category or "Spatial" in category:
        return score_spatial_and_temporal(llm_response, expected_answer, prompt)
    else:
        # Default fallback scorer
        if expected_answer.lower() in llm_response.lower():
            return {"score": 1.0, "reason": "Passed basic inclusion check."}
        return {"score": 0.0, "reason": "Failed basic inclusion check."}
