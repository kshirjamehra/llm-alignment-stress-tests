import json
import uuid
import random
from pydantic import BaseModel, Field
from typing import List, Optional

class ReasoningTestInfo(BaseModel):
    id: str
    category: str = Field(..., description="E.g., Algorithmic Counting, Negation & Constraint")
    prompt: str
    expected_answer: str
    common_failure_mode: str
    image_url: Optional[str] = None

class ReasoningDataset(BaseModel):
    tests: List[ReasoningTestInfo]

def generate_counting_puzzles():
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    tests = []
    for _ in range(20):
        words = []
        for _ in range(random.randint(3, 6)):
            word = "".join(random.choices(consonants, k=random.randint(2,4))) + \
                   "".join(random.choices(vowels, k=random.randint(1,2))) + \
                   "".join(random.choices(consonants, k=random.randint(1,3)))
            words.append(word)
        target_char = random.choice(list("abcdefghijklmnopqrstuvwxyz"))
        nonsense_string = "".join(words)
        count = nonsense_string.count(target_char)
        
        prompt = f"Consider the following concatenated nonsense string: '{nonsense_string}'. How many times does the letter '{target_char}' appear in this string? Think step by step and then provide the final count."
        
        tests.append(ReasoningTestInfo(
            id=str(uuid.uuid4()),
            category="Algorithmic Counting",
            prompt=prompt,
            expected_answer=str(count),
            common_failure_mode="Token-blindness: The LLM processes the string as abstract tokens rather than individual characters, causing it to miscount the occurrences of the specific character."
        ))
    return tests

def generate_negation_puzzles():
    topics = ["quantum computing", "black holes", "photosynthesis", "ancient Rome", "machine learning", "neural networks", "the history of jazz", "blockchain technology", "CRISPR gene editing", "the deep sea", "mars colonization", "the water cycle", "string theory", "volcanic eruptions", "the human immune system", "artificial intelligence", "classical mechanics", "the internet of things", "renewable energy", "cryptography"]
    tests = []
    for topic in topics:
        forbidden_letter = random.choice(["t", "e", "a", "s"])
        prompt = f"Write a paragraph explaining {topic}, but every sentence must end with a word that has exactly three vowels. Do not use the letter '{forbidden_letter}' anywhere in your response."
        
        tests.append(ReasoningTestInfo(
            id=str(uuid.uuid4()),
            category="Negation & Constraint",
            prompt=prompt,
            expected_answer="A paragraph explaining the topic where NO words contain the forbidden letter, and EVERY sentence ends with a word containing exactly three vowels.",
            common_failure_mode="Token-blindness & Constraint Forgetting: The LLM tends to accidentally include the forbidden letter due to subword tokenization, or fails the structural constraint (3 vowels at the end of each sentence) because it focuses on the topic explanation."
        ))
    return tests

from datetime import datetime, timedelta
import pytz

def generate_temporal_puzzles():
    cities = [
        ("Tokyo", "Asia/Tokyo"),
        ("LA", "America/Los_Angeles"),
        ("NY", "America/New_York"),
        ("London", "Europe/London"),
        ("Sydney", "Australia/Sydney"),
    ]
    tests = []
    
    # Let's generate 20 random flights
    for _ in range(20):
        # Pick 3 unique cities
        c1, c2, c3 = random.sample(cities, 3)
        
        # Random start day and time
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        start_day = random.choice(days)
        start_hour = random.randint(1, 11)
        ampm = random.choice(["AM", "PM"])
        
        f1_dur = random.randint(5, 14)
        wait_dur = random.randint(1, 8)
        f2_dur = random.randint(4, 12)
        
        prompt = f"A flight leaves {c1[0]} at {start_hour} {ampm} {start_day}, flies {f1_dur} hours to {c2[0]}, waits {wait_dur} hours, flies {f2_dur} hours to {c3[0]}. Accounting for daylight savings and time zones, what is the exact local time and day in {c3[0]} upon arrival?"
        
        tests.append(ReasoningTestInfo(
            id=str(uuid.uuid4()),
            category="Timezone & Relativity",
            prompt=prompt,
            expected_answer=f"The correct calculated time in {c3[0]} time zone. (Evaluation requires executing the exact delta over real timezone conversions).",
            common_failure_mode="Temporal Hallucination: The LLM adds hours sequentially but forgets or hallucinates the timezone offsets (DST boundaries) between the intermediate and final nodes, reporting a relative time rather than absolute local time."
        ))
    return tests

def generate_causal_puzzles():
    events = ["A", "B", "C", "D", "E"]
    triggers = ["triggers", "causes", "initiates"]
    prevents = ["strictly prevents", "blocks", "nullifies"]
    requires = ["is required for", "is a prerequisite for"]
    
    tests = []
    for _ in range(20):
        e1, e2, e3, e4 = random.sample(events, 4)
        t = random.choice(triggers)
        p = random.choice(prevents)
        r = random.choice(requires)
        
        prompt = f"Event {e1} {t} {e2}. {e2} {p} {e3}. {e3} {r} {e4}. If Event {e1} occurs, map the probability of {e4} occurring and explain the exact blocker in the causal chain."
        
        expected = f"Since {e1} {t} {e2}, {e2} happens. Since {e2} {p} {e3}, {e3} cannot happen. Since {e3} {r} {e4}, {e4} cannot happen. Probability of {e4} is 0%. Blocker is {e2} preventing {e3}."
        
        tests.append(ReasoningTestInfo(
            id=str(uuid.uuid4()),
            category="Causal Chain Breakdown",
            prompt=prompt,
            expected_answer=expected,
            common_failure_mode="Causal Skip: The LLM loses track of the negation in the middle of the chain ('prevents'), assuming positive correlation flows all the way to the end, hallucinating that the final event occurs."
        ))
    return tests

def generate_state_tracking_puzzles():
    tests = []
    containers = ["red cup", "blue box", "green bag", "yellow envelope", "safe", "drawer", "pocket", "backpack"]
    locations = ["garage", "kitchen", "office", "bedroom", "living room", "attic"]
    items = ["coin", "key", "ring", "marble", "watch"]
    
    for _ in range(20):
        item = random.choice(items)
        c1, c2, c3 = random.sample(containers, 3)
        l1, l2 = random.sample(locations, 2)
        
        prompt = f"I put the {item} in the {c1}. I moved the {c1} to the {l1}. I took the {item} out and put it in my {c3}. I moved the {l1} to the {l2}. Where is the {item} right now?"
        
        tests.append(ReasoningTestInfo(
            id=str(uuid.uuid4()),
            category="State-Tracking",
            prompt=prompt,
            expected_answer=f"The {item} is in the {c3}.",
            common_failure_mode="Spatial Disconnect: The LLM gets confused by the movement of the container (l1 to l2) acting as a distractor since the item was already removed and placed in c3."
        ))
    return tests

def generate_spatial_diagram_puzzles():
    tests = []
    for i in range(20):
        prompt = f"Based on the provided spatial-reference diagram, deduce the position of the unseen blocks. If block A is visible at the top, and block B is supporting it but partially occluded, what is the minimum number of blocks required to support this structure from the ground up? (Variation {i+1})"
        
        tests.append(ReasoningTestInfo(
            id=str(uuid.uuid4()),
            category="Spatial Diagram",
            prompt=prompt,
            expected_answer="The exact number of supporting blocks deduced from the isomorphic projection rules.",
            common_failure_mode="Multimodal Hallucination: The LLM fails to correctly infer the 3D volume from the 2D isometric projection and guesses the number of supporting blocks.",
            image_url="/spatial-reference.png"
        ))
    return tests

if __name__ == "__main__":
    counting = generate_counting_puzzles()
    negation = generate_negation_puzzles()
    temporal = generate_temporal_puzzles()
    causal = generate_causal_puzzles()
    state_tracking = generate_state_tracking_puzzles()
    spatial_diagram = generate_spatial_diagram_puzzles()
    
    dataset = ReasoningDataset(tests=counting + negation + temporal + causal + state_tracking + spatial_diagram)
    
    with open("reasoning_breakdown.json", "w") as f:
        f.write(dataset.model_dump_json(indent=2))
        
    print(f"Generated {len(dataset.tests)} tests and saved to reasoning_breakdown.json")
