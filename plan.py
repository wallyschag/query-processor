from operators.scan import ScanOp
from operators.select import SelectOp
from operators.project import ProjectOp
from operators.join import JoinOp
from operators.limit import LimitOp

def build_operator_from_json(plan):
    op = plan["op"]

    if op == "Scan":
        return ScanOp(plan["table"], plan["as"])

    if op == "Select":
        child = build_operator_from_json(plan["input"])
        return SelectOp(child, plan["predicate"])

    if op == "Project":
        child = build_operator_from_json(plan["input"])
        return ProjectOp(child, plan["exprs"])

    if op == "Join":
        left = build_operator_from_json(plan["left"])
        right = build_operator_from_json(plan["right"])
        return JoinOp(left, right, plan["condition"])

    if op == "Limit":
        child = build_operator_from_json(plan["input"])
        return LimitOp(child, plan["limit"])

    raise ValueError(f"Unknown operator: {op}")
