from .base import Operator

class LimitOp(Operator):
    def __init__(self, child, limit):
        self.child = child
        self.limit = limit
        self.count = 0

    def open(self):
        self.child.open()
        self.count = 0

    def next(self):
        if self.count >= self.limit:
            return None
        row = self.child.next()
        if row is None:
            return None
        self.count += 1
        return row

    def close(self):
        self.child.close()
