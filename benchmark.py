import subprocess
import time
import json
import os

queries = [
    "data/example1/query_high_balance.json",
    "data/example2/query_open_order_line_totals.json",
    "data/example2/query_open_high_value_orders.json"
]

configurations = [
    {"name": "Nested Loop Join", "env": {"CENGINE_JOIN_ALGO": "nested_loop", "CENGINE_OPTIMIZE": "false"}},
    {"name": "Nested Loop Join + Optimization", "env": {"CENGINE_JOIN_ALGO": "nested_loop", "CENGINE_OPTIMIZE": "true"}},
    {"name": "Hash Join", "env": {"CENGINE_JOIN_ALGO": "hash", "CENGINE_OPTIMIZE": "false"}},
    {"name": "Hash Join + Optimization", "env": {"CENGINE_JOIN_ALGO": "hash", "CENGINE_OPTIMIZE": "true"}},
    {"name": "Sort-Merge Join", "env": {"CENGINE_JOIN_ALGO": "sort_merge", "CENGINE_OPTIMIZE": "false"}},
    {"name": "Sort-Merge Join + Optimization", "env": {"CENGINE_JOIN_ALGO": "sort_merge", "CENGINE_OPTIMIZE": "true"}},
]

def run_benchmark(query, env_vars):
    """Run a single query with given environment variables"""
    env = os.environ.copy()
    env.update(env_vars)
    
    start = time.time()
    result = subprocess.run(
        ["python3", "query_processor.py", query],
        capture_output=True,
        text=True,
        env=env
    )
    elapsed = time.time() - start
    
    return {
        "time": elapsed,
        "output": result.stdout,
        "error": result.stderr
    }

def main():
    print("Running benchmarks...")
    print("=" * 80)
    
    results = {}
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        results[query] = {}
        
        for config in configurations:
            print(f"  Running {config['name']}...", end="", flush=True)
            result = run_benchmark(query, config["env"])
            results[query][config["name"]] = result["time"]
            print(f" {result['time']:.4f}s")
    
    # Print summary table
    print("\n\nSummary Table (execution times in seconds):")
    print("=" * 80)
    
    # Header
    print(f"{'Query':<40}", end="")
    for config in configurations:
        print(f"{config['name']:<20}", end="")
    print()
    
    print("-" * 80)
    
    # Data rows
    for query in queries:
        query_name = os.path.basename(query).replace(".json", "")
        print(f"{query_name:<40}", end="")
        for config in configurations:
            time_val = results[query][config["name"]]
            print(f"{time_val:<20.4f}", end="")
        print()
    
    # Save results to JSON
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to benchmark_results.json")

if __name__ == "__main__":
    main()
