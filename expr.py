def eval_expr(expr, row):
    if "col" in expr:
        return _convert(row[expr["col"]])
    if "const" in expr:
        return expr["const"]

    op = expr["op"]
    if op == "NOT":
        return not eval_expr(expr["expr"], row)

    left = eval_expr(expr.get("left"), row) if "left" in expr else None
    right = eval_expr(expr.get("right"), row) if "right" in expr else None

    if op == "ADD": return left + right
    if op == "SUB": return left - right
    if op == "MUL": return left * right
    if op == "DIV": return left / right
    if op == "EQ":  return left == right
    if op == "NE":  return left != right
    if op == "LT":  return left < right
    if op == "LE":  return left <= right
    if op == "GT":  return left > right
    if op == "GE":  return left >= right
    if op == "AND": return left and right
    if op == "OR":  return left or right

    raise ValueError(f"Unsupported op: {op}")

def _convert(val):
    # try to convert numeric
    try:
        if "." in str(val):
            return float(val)
        return int(val)
    except:
        return val
