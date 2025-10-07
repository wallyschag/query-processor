def optimize_plan(plan):
    """Apply predicate pushdown optimization to the query plan"""
    return pushdown_predicates(plan)

def pushdown_predicates(plan):
    """Recursively push down predicates through the plan tree"""
    op = plan.get("op")
    
    if op == "Select":
        # Try to push this select down
        child_op = plan["input"].get("op")
        
        if child_op == "Project":
            # Push select below project if possible
            project_plan = plan["input"]
            predicate = plan["predicate"]
            
            # Check if predicate uses only columns available before projection
            if can_push_through_project(predicate, project_plan):
                # Rewrite predicate to use original column names
                rewritten_predicate = rewrite_predicate_for_pushdown(predicate, project_plan)
                
                # Create new plan with select pushed down
                new_plan = {
                    "op": "Project",
                    "exprs": project_plan["exprs"],
                    "input": {
                        "op": "Select",
                        "predicate": rewritten_predicate,
                        "input": pushdown_predicates(project_plan["input"])
                    }
                }
                return new_plan
        
        elif child_op == "Join":
            # Try to push predicates down to join children
            join_plan = plan["input"]
            predicate = plan["predicate"]
            
            left_preds, right_preds, remaining_preds = split_predicates_for_join(predicate, join_plan)
            
            new_join = {
                "op": "Join",
                "condition": join_plan["condition"],
                "left": join_plan["left"],
                "right": join_plan["right"]
            }
            
            # Push predicates to left side if any
            if left_preds:
                new_join["left"] = {
                    "op": "Select",
                    "predicate": left_preds,
                    "input": pushdown_predicates(join_plan["left"])
                }
            else:
                new_join["left"] = pushdown_predicates(join_plan["left"])
            
            # Push predicates to right side if any
            if right_preds:
                new_join["right"] = {
                    "op": "Select",
                    "predicate": right_preds,
                    "input": pushdown_predicates(join_plan["right"])
                }
            else:
                new_join["right"] = pushdown_predicates(join_plan["right"])
            
            # Keep remaining predicates above join
            if remaining_preds:
                return {
                    "op": "Select",
                    "predicate": remaining_preds,
                    "input": new_join
                }
            else:
                return new_join
    
    # For other operators, just recurse on children
    if op == "Project":
        return {
            **plan,
            "input": pushdown_predicates(plan["input"])
        }
    elif op == "Join":
        return {
            **plan,
            "left": pushdown_predicates(plan["left"]),
            "right": pushdown_predicates(plan["right"])
        }
    elif op == "Limit":
        return {
            **plan,
            "input": pushdown_predicates(plan["input"])
        }
    
    # Leaf operators (Scan) or unknown operators
    return plan

def can_push_through_project(predicate, project_plan):
    """Check if predicate can be pushed through projection"""
    used_cols = get_columns_used(predicate)
    
    # Check if all columns used in predicate are computable before projection
    for col in used_cols:
        if not is_column_available_before_project(col, project_plan):
            return False
    return True

def is_column_available_before_project(col, project_plan):
    """Check if a column is available in the input to the project"""
    # For simplicity, we assume columns are available if they're referenced
    # in any of the project expressions
    for expr in project_plan["exprs"]:
        if contains_column(expr["expr"], col):
            return True
    return False

def contains_column(expr, col):
    """Check if expression contains a column reference"""
    if "col" in expr and expr["col"] == col:
        return True
    if "left" in expr and contains_column(expr["left"], col):
        return True
    if "right" in expr and contains_column(expr["right"], col):
        return True
    if "expr" in expr and contains_column(expr["expr"], col):
        return True
    return False

def rewrite_predicate_for_pushdown(predicate, project_plan):
    """Rewrite predicate to use original column names before projection"""
    # For simplicity, return the predicate as-is
    # In a full implementation, this would map projected names back to originals
    return predicate

def split_predicates_for_join(predicate, join_plan):
    """Split predicates into those that can go left, right, or must stay above join"""
    # Get aliases for left and right inputs
    left_alias = get_scan_alias(join_plan["left"])
    right_alias = get_scan_alias(join_plan["right"])
    
    # For AND predicates, we can split them
    if predicate.get("op") == "AND":
        left_preds = []
        right_preds = []
        remaining_preds = []
        
        # Recursively split left and right of AND
        left_l, right_l, remaining_l = split_predicates_for_join(predicate["left"], join_plan)
        left_r, right_r, remaining_r = split_predicates_for_join(predicate["right"], join_plan)
        
        # Combine results
        if left_l: left_preds.append(left_l)
        if left_r: left_preds.append(left_r)
        if right_l: right_preds.append(right_l)
        if right_r: right_preds.append(right_r)
        if remaining_l: remaining_preds.append(remaining_l)
        if remaining_r: remaining_preds.append(remaining_r)
        
        # Build combined predicates
        left_pred = combine_predicates(left_preds) if left_preds else None
        right_pred = combine_predicates(right_preds) if right_preds else None
        remaining_pred = combine_predicates(remaining_preds) if remaining_preds else None
        
        return left_pred, right_pred, remaining_pred
    
    # For single predicates, check which side they belong to
    used_cols = get_columns_used(predicate)
    uses_left = any(col.startswith(left_alias + ".") for col in used_cols)
    uses_right = any(col.startswith(right_alias + ".") for col in used_cols)
    
    if uses_left and not uses_right:
        return predicate, None, None
    elif uses_right and not uses_left:
        return None, predicate, None
    else:
        # Predicate uses both sides or neither, keep above join
        return None, None, predicate

def get_scan_alias(plan):
    """Get the scan alias from a plan tree"""
    if plan.get("op") == "Scan":
        return plan.get("as", "")
    if "input" in plan:
        return get_scan_alias(plan["input"])
    if "left" in plan:
        # For joins, return left alias (simplified)
        return get_scan_alias(plan["left"])
    return ""

def get_columns_used(expr):
    """Get all column references used in an expression"""
    cols = []
    if "col" in expr:
        cols.append(expr["col"])
    if "left" in expr:
        cols.extend(get_columns_used(expr["left"]))
    if "right" in expr:
        cols.extend(get_columns_used(expr["right"]))
    if "expr" in expr:
        cols.extend(get_columns_used(expr["expr"]))
    return cols

def combine_predicates(preds):
    """Combine multiple predicates with AND"""
    if len(preds) == 0:
        return None
    if len(preds) == 1:
        return preds[0]
    
    result = preds[0]
    for pred in preds[1:]:
        result = {
            "op": "AND",
            "left": result,
            "right": pred
        }
    return result
