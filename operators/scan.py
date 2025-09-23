import csv
from .base import Operator

class ScanOp(Operator):
    def __init__(self, table, alias):
        self.table = table
        self.alias = alias
        self.file = None
        self.reader = None
        self.headers = None

    def open(self):
        self.file = open(self.table, newline="")
        self.reader = csv.DictReader(self.file)
        self.headers = self.reader.fieldnames

    def next(self):
        try:
            row = next(self.reader)
        except StopIteration:
            return None
        # prefix alias
        return {f"{self.alias}.{k}": v for k, v in row.items()}

    def close(self):
        if self.file:
            self.file.close()
