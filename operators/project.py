from .base import Operator
from expr import eval_expr

class ProjectOp(Operator):
    def __init__(self, child, exprs):
        self.child = child
        self.exprs = exprs  # list of {"as": alias, "expr": expr_json}

    def open(self):
        self.child.open()

    def next(self):
        row = self.child.next()
        if row is None:
            return None
        out = {}
        for spec in self.exprs:
            alias = spec["as"]
            val = eval_expr(spec["expr"], row)
            out[alias] = val
        return out

    def close(self):
        self.child.close()
