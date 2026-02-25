import json
import os
import glob

def verify_json_files(directory):
    json_files = glob.glob(os.path.join(directory, "*.json"))
    all_valid = True
    
    print(f"Found {len(json_files)} JSON files in {directory}...")
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[PASS] {os.path.basename(file_path)} - Valid JSON. Contains {len(data)} items.")
        except json.JSONDecodeError as e:
            print(f"[FAIL] {os.path.basename(file_path)} - Invalid JSON: {e}")
            all_valid = False
        except Exception as e:
            print(f"[FAIL] {os.path.basename(file_path)} - Error: {e}")
            all_valid = False
            
    if all_valid:
        print("\nAll JSON files verified successfully.")
        exit(0)
    else:
        print("\nSome files failed verification.")
        exit(1)

if __name__ == "__main__":
    prompts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts")
    verify_json_files(prompts_dir)
