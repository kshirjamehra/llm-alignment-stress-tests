import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.evaluator import Evaluator

@pytest.fixture
def evaluator():
    return Evaluator()

def test_exact_match(evaluator):
    assert evaluator.calculate_exact_match("Hello World", "hello world") == 1.0
    assert evaluator.calculate_exact_match("Hello", "World") == 0.0
    assert evaluator.calculate_exact_match("  Spaces  ", "spaces") == 1.0

def test_semantic_similarity(evaluator):
    # Identical
    assert evaluator.calculate_semantic_similarity("abc", "abc") == 1.0
    # Completely different
    assert evaluator.calculate_semantic_similarity("abc", "xyz") == 0.0
    # Partial
    score = evaluator.calculate_semantic_similarity("The cat sat on the mat", "The cat sat on mat")
    assert 0.8 < score < 1.0

def test_check_refusal(evaluator):
    assert evaluator.check_refusal("I cannot do that.") == 1.0
    assert evaluator.check_refusal("I'm sorry, but I can't help.") == 1.0
    assert evaluator.check_refusal("Here is the answer.") == 0.0

def test_evaluate_response_orchestration(evaluator):
    response = "Paris"
    expected = "Paris"
    results = evaluator.evaluate_response(response, expected, checks=['exact'])
    assert results['exact_match'] == 1.0
    assert 'similarity_score' not in results

def test_evaluate_response_refusal(evaluator):
    response = "I cannot answer this query."
    results = evaluator.evaluate_response(response, checks=['refusal'])
    assert results['refusal_score'] == 1.0
