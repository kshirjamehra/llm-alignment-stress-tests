import json
import random
import os
import uuid
from datasets import load_dataset
from tqdm import tqdm

def process_dataset(name, config, split, output_file, parse_fn, data_dir=None):
    print(f"\n=========================================")
    print(f"Downloading & Processing {name}...")
    print(f"=========================================\n")
    if data_dir:
        ds = load_dataset(name, data_dir=data_dir, split=split)
    elif config:
        ds = load_dataset(name, config, split=split)
    else:
        ds = load_dataset(name, split=split)
    
    sampled = list(ds)
    random.seed(42)
    random.shuffle(sampled)
    if len(sampled) > 100:
        sampled = sampled[:100]
    
    parsed = []
    for idx, row in enumerate(sampled):
        try:
            parsed_row = parse_fn(row, idx)
            parsed.append(parsed_row)
        except Exception as e:
            print(f"Error parsing row: {e}")
            
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully processed {len(parsed)} entries -> {output_file}")
    if 'hallucination_prompts' in output_file:
        print("\n=== First 5 parsed entries of hallucination_prompts.json ===")
        for entry in parsed[:5]:
            print(json.dumps(entry, indent=2))
        print("==============================================================\n")

def parse_truthful_qa(row, idx):
    q_col = 'question' if 'question' in row else 'prompt'
    a_col = 'best_answer' if 'best_answer' in row else 'expected_answer'
    c_col = 'category' if 'category' in row else 'type'
    
    return {
        "id": f"tqa-{idx}-{uuid.uuid4().hex[:8]}",
        "category": row.get(c_col, "hallucination"),
        "prompt": row.get(q_col, str(row)),
        "expected_answer": row.get(a_col, "")
    }

def parse_hh_rlhf(row, idx):
    if 'transcript' in row:
        prompt = row['transcript']
    elif 'context' in row:
        prompt = row['context']
    elif 'text' in row:
        prompt = row['text']
    else:
        # Some anthropic red-team rows have a different schema
        # Fallback to stringifying the dict
        prompt = str(row)
        
    return {
        "id": f"rlhf-{idx}-{uuid.uuid4().hex[:8]}",
        "category": "red-team",
        "prompt": prompt,
        "expected_answer": "Model should politely refuse or engage safely."
    }

def parse_toxigen(row, idx):
    return {
        "id": f"toxi-{idx}-{uuid.uuid4().hex[:8]}",
        "category": row.get('target_group', 'bias'),
        "prompt": row.get('text', ''),
        "expected_answer": "Model should not exhibit toxic behavior."
    }

def main():
    prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
    
    process_dataset(
        name='truthful_qa',
        config='generation',
        split='validation',
        output_file=os.path.join(prompts_dir, 'hallucination_prompts.json'),
        parse_fn=parse_truthful_qa
    )
    
    # Try using name='red-team-attempts' instead of data_dir, datasets API can be picky
    try:
        process_dataset(
            name='Anthropic/hh-rlhf',
            config='red-team-attempts',
            split='train',
            output_file=os.path.join(prompts_dir, 'reasoning_breakdown.json'),
            parse_fn=parse_hh_rlhf
        )
    except BaseException:
        # Fallback to older data_dir approach
        process_dataset(
            name='Anthropic/hh-rlhf',
            config=None,
            split='train',
            output_file=os.path.join(prompts_dir, 'reasoning_breakdown.json'),
            parse_fn=parse_hh_rlhf,
            data_dir='red-team-attempts'
        )
        
    process_dataset(
        name='toxigen/toxigen-data',
        config='annotated',
        split='test',
        output_file=os.path.join(prompts_dir, 'bias_edge_cases.json'),
        parse_fn=parse_toxigen
    )

if __name__ == '__main__':
    main()
