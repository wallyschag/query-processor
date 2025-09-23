import sys
import json
from plan import build_operator_from_json

def main():
    if len(sys.argv) < 2:
        print("Usage: python query_processor.py plan.json")
        sys.exit(1)

    plan_file = sys.argv[1]
    with open(plan_file) as f:
        plan_json = json.load(f)

    root = build_operator_from_json(plan_json)

    root.open()
    results = []
    while True:
        row = root.next()
        if row is None:
            break
        results.append(row)
    root.close()

    # print results
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
