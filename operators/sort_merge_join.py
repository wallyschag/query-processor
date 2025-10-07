from .base import Operator

class SortMergeJoinOp(Operator):
    def __init__(self, left, right, left_key, right_key):
        self.left = left
        self.right = right
        self.left_key = left_key
        self.right_key = right_key
        self.left_sorted = []
        self.right_sorted = []
        self.left_idx = 0
        self.right_idx = 0
        self.right_group_start = 0
        self.current_left_row = None
        
    def open(self):
        self.left.open()
        self.right.open()
        
        # Load and sort left input
        while True:
            row = self.left.next()
            if row is None:
                break
            self.left_sorted.append(row)
        self.left_sorted.sort(key=lambda x: self._get_key_value(x.get(self.left_key)))
        
        # Load and sort right input
        while True:
            row = self.right.next()
            if row is None:
                break
            self.right_sorted.append(row)
        self.right_sorted.sort(key=lambda x: self._get_key_value(x.get(self.right_key)))
        
        self.left_idx = 0
        self.right_idx = 0
        self.right_group_start = 0
        
    def _get_key_value(self, val):
        # Convert values for comparison, handling None
        if val is None:
            return (0, None)  # Sort None values first
        try:
            # Try to convert to number for proper numeric sorting
            if "." in str(val):
                return (1, float(val))
            return (1, int(val))
        except:
            return (1, str(val))
    
    def next(self):
        while self.left_idx < len(self.left_sorted):
            if self.current_left_row is None:
                self.current_left_row = self.left_sorted[self.left_idx]
                left_key_val = self._get_key_value(self.current_left_row.get(self.left_key))
                
                # Skip right rows that are less than current left key
                while (self.right_group_start < len(self.right_sorted) and 
                       self._get_key_value(self.right_sorted[self.right_group_start].get(self.right_key)) < left_key_val):
                    self.right_group_start += 1
                
                self.right_idx = self.right_group_start
            
            # Check if we have matching right rows
            if self.right_idx < len(self.right_sorted):
                right_row = self.right_sorted[self.right_idx]
                right_key_val = self._get_key_value(right_row.get(self.right_key))
                left_key_val = self._get_key_value(self.current_left_row.get(self.left_key))
                
                if left_key_val == right_key_val:
                    # Found a match
                    self.right_idx += 1
                    combined = {**self.current_left_row, **right_row}
                    return combined
                elif right_key_val > left_key_val:
                    # No more matches for this left row
                    self.left_idx += 1
                    self.current_left_row = None
                else:
                    # Should not happen if sorted correctly
                    self.right_idx += 1
            else:
                # No more right rows for this left row
                self.left_idx += 1
                self.current_left_row = None
                
        return None
    
    def close(self):
        self.left.close()
        self.right.close()
