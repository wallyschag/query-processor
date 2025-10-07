from operators.scan import ScanOp
from operators.select import SelectOp
from operators.project import ProjectOp
from operators.join import JoinOp
from operators.limit import LimitOp
from operators.hash_join import HashJoinOp
from operators.sort_merge_join import SortMergeJoinOp
from optimizer import optimize_plan
import os

# Global flag to control join algorithm
# Set via environment variable: CENGINE_JOIN_ALGO=hash|sort_merge|nested_loop
JOIN_ALGO = os.environ.get('CENGINE_JOIN_ALGO', 'hash')

# Global flag to enable/disable optimization
# Set via environment variable: CENGINE_OPTIMIZE=true|false
ENABLE_OPTIMIZE = os.environ.get('CENGINE_OPTIMIZE', 'false').lower() == 'true'

def build_operator_from_json(plan, optimize=None):
    # Apply optimization if enabled
    if optimize is None:
        optimize = ENABLE_OPTIMIZE
    
    if optimize:
        plan = optimize_plan(plan)
        print("Optimized plan applied (predicate pushdown)")
    
    op = plan["op"]

    if op == "Scan":
        return ScanOp(plan["table"], plan["as"])

    if op == "Select":
        child = build_operator_from_json(plan["input"], optimize=False)  # Don't re-optimize
        return SelectOp(child, plan["predicate"])

    if op == "Project":
        child = build_operator_from_json(plan["input"], optimize=False)
        return ProjectOp(child, plan["exprs"])
    
    if op == "Join":
        left = build_operator_from_json(plan["left"], optimize=False)
        right = build_operator_from_json(plan["right"], optimize=False)
        condition = plan["condition"]
        
        # Choose join algorithm based on environment variable
        if JOIN_ALGO == 'nested_loop':
            # Original nested loop join
            return JoinOp(left, right, condition)
        
        elif JOIN_ALGO == 'sort_merge':
            # Sort-merge join
            if condition["op"] != "EQ" or "col" not in condition["left"] or "col" not in condition["right"]:
                raise ValueError("Only simple equi-joins supported for sort-merge join")
            left_key = condition["left"]["col"]
            right_key = condition["right"]["col"]
            return SortMergeJoinOp(left, right, left_key, right_key)
        
        else:  # Default to hash join
            # Hash join
            if condition["op"] != "EQ" or "col" not in condition["left"] or "col" not in condition["right"]:
                raise ValueError("Only simple equi-joins supported for hash join")
            left_key = condition["left"]["col"]
            right_key = condition["right"]["col"]
            return HashJoinOp(left, right, left_key, right_key)

    if op == "Limit":
        child = build_operator_from_json(plan["input"], optimize=False)
        return LimitOp(child, plan["limit"])

    raise ValueError(f"Unknown operator: {op}")
