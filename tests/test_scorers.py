import pytest
from src.scorers import score_algorithmic_constraints, score_spatial_and_temporal, evaluate

def test_score_algorithmic_constraints_pass():
    prompt = "Write a paragraph explaining quantum computing, but every sentence must end with a word that has exactly three vowels. Do not use the letter 'z' anywhere in your response."
    response = "Quantum computing is complex but beautiful. It computes states very smoothly." # beautiful has 4 vowels, smoothly has 2... wait, let's write a targeted string
    
    # "beautiful" = e, a, u, i, u (5) - wait, this is just for testing the regex
    # Let's write one that explicitly passes: "outie" (o, u, i, e - 4)
    # "audio" (a, u, i, o - 4)
    # "movie" (o, i, e - 3)
    response_pass = "Quantum computing is a great movie. The particles move in a fluid." 
    # movie: m-o-v-i-e -> o,i,e (3)
    # fluid: f-l-u-i-d -> u,i (2) -> let's change to "louie" -> l-o-u-i-e (4) -> "cookie" -> c-o-o-k-i-e (3)
    response_pass = "Quantum computing is like a cookie. It operates using a specific manual."
    # cookie (o, o, i, e - 4) -> "radio" -> r-a-d-i-o (3). yes!
    # manual (a, u, a - 3). yes!
    response_pass = "Quantum computing is like a radio. It operates using a specific manual."
    
    expected = "Valid paragraph."
    res = score_algorithmic_constraints(response_pass, expected, prompt)
    assert res["score"] == 1.0

def test_score_algorithmic_constraints_forbidden_letter_fail():
    prompt = "Do not use the letter 't' anywhere."
    response = "This has the forbidden letter."
    expected = ""
    res = score_algorithmic_constraints(response, expected, prompt)
    assert res["score"] == 0.0
    assert "forbidden letter 't'" in res["reason"]

def test_score_spatial_pass():
    prompt = "I put the coin in the red cup. I moved the red cup to the safe. I took the coin out and put it in my pocket. I moved the safe to the garage. Where is the coin right now?"
    response = "The coin is currently located in your pocket."
    expected = "The coin is in the pocket."
    res = score_spatial_and_temporal(response, expected, prompt)
    assert res["score"] == 1.0

def test_score_spatial_fail():
    prompt = "I put the coin in the red cup. I moved the red cup to the safe. I took the coin out and put it in my pocket. I moved the safe to the garage. Where is the coin right now?"
    response = "Based on the movements, the coin is in the safe in the garage."
    expected = "The coin is in the pocket."
    res = score_spatial_and_temporal(response, expected, prompt)
    assert res["score"] == 0.0
    
def test_evaluate_router():
    res = evaluate("Negation & Constraint", "Do not use the letter 'z'.", "Hello world.", "")
    assert res["score"] == 1.0
    res = evaluate("State-Tracking", "Where is it?", "It is in the red cup.", "red cup")
    assert res["score"] == 1.0
