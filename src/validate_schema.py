import sys
from pydantic import ValidationError
from data_generator import ReasoningDataset

def main():
    try:
        with open("reasoning_breakdown.json", "r") as f:
            data = f.read()
            dataset = ReasoningDataset.model_validate_json(data)
            print("========================================")
            print("✅ JSON Schema Validation: SUCCESS")
            print("========================================")
            print(f"Total entries parsed: {len(dataset.tests)}")
            
            categories = {}
            for test in dataset.tests:
                categories[test.category] = categories.get(test.category, 0) + 1
                
            for cat, count in categories.items():
                print(f" - {cat}: {count} tests")
                
            print("\nSchema definition:")
            print(ReasoningDataset.model_json_schema())
            
    except ValidationError as e:
        print("❌ JSON Schema Validation: FAILED")
        print(e)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ reasoning_breakdown.json not found")
        sys.exit(1)

if __name__ == "__main__":
    main()
