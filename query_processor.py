import sys
import json
import time
import os
from plan import build_operator_from_json

def main():
    if len(sys.argv) < 2:
        print("Usage: python query_processor.py plan.json")
        print("\nEnvironment variables:")
        print("  CENGINE_JOIN_ALGO=hash|sort_merge|nested_loop  (default: hash)")
        print("  CENGINE_OPTIMIZE=true|false  (default: false)")
        sys.exit(1)

    plan_file = sys.argv[1]
    with open(plan_file) as f:
        plan_json = json.load(f)

    # Show current settings
    join_algo = os.environ.get('CENGINE_JOIN_ALGO', 'hash')
    optimize = os.environ.get('CENGINE_OPTIMIZE', 'false').lower() == 'true'
    
    print(f"Running query: {plan_file}")
    print(f"Join algorithm: {join_algo}")
    print(f"Optimization enabled: {optimize}")
    print("-" * 50)

    # Build and execute query
    start_time = time.time()
    root = build_operator_from_json(plan_json)
    build_time = time.time() - start_time

    root.open()
    results = []
    exec_start = time.time()
    while True:
        row = root.next()
        if row is None:
            break
        results.append(row)
    exec_time = time.time() - exec_start
    root.close()

    # Print results
    print(f"\nResults ({len(results)} rows):")
    for r in results:
        print(r)
    
    print(f"\nTiming:")
    print(f"  Build time: {build_time:.4f}s")
    print(f"  Execution time: {exec_time:.4f}s")
    print(f"  Total time: {build_time + exec_time:.4f}s")

if __name__ == "__main__":
    main()
