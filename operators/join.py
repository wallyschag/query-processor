from .base import Operator
from expr import eval_expr

class JoinOp(Operator):
    def __init__(self, left, right, condition):
        self.left = left
        self.right = right
        self.condition = condition
        self.left_row = None

    def open(self):
        self.left.open()
        self.right.open()
        self.left_row = self.left.next()
        self.right_rows = []
        # preload right table
        while True:
            r = self.right.next()
            if r is None:
                break
            self.right_rows.append(r)
        self.right_index = 0

    def next(self):
        while self.left_row is not None:
            while self.right_index < len(self.right_rows):
                rrow = self.right_rows[self.right_index]
                self.right_index += 1
                combined = {**self.left_row, **rrow}
                if eval_expr(self.condition, combined):
                    return combined
            # reset right side for next left row
            self.right_index = 0
            self.left_row = self.left.next()
        return None

    def close(self):
        self.left.close()
        self.right.close()
