from .base import Operator
from collections import defaultdict

class HashJoinOp(Operator):
    def __init__(self, left, right, left_key, right_key):
        self.left = left
        self.right = right
        self.left_key = left_key
        self.right_key = right_key
        self.hash_table = None
        self.left_row = None
        self.matches = []
        self.match_index = 0

    def open(self):
        self.left.open()
        self.right.open()
        self.hash_table = defaultdict(list)
        while True:
            r = self.right.next()
            if r is None:
                break
            key = r.get(self.right_key)
            if key is not None:
                self.hash_table[key].append(r)

    def next(self):
        while True:
            if self.match_index < len(self.matches):
                rrow = self.matches[self.match_index]
                self.match_index += 1
                combined = {**self.left_row, **rrow}
                return combined
            else:
                self.left_row = self.left.next()
                if self.left_row is None:
                    return None
                key = self.left_row.get(self.left_key)
                self.matches = self.hash_table[key]
                self.match_index = 0

    def close(self):
        self.left.close()
        self.right.close()
