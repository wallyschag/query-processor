from .base import Operator
from expr import eval_expr

class SelectOp(Operator):
    def __init__(self, child, predicate):
        self.child = child
        self.predicate = predicate

    def open(self):
        self.child.open()

    def next(self):
        while True:
            row = self.child.next()
            if row is None:
                return None
            if eval_expr(self.predicate, row):
                return row

    def close(self):
        self.child.close()
