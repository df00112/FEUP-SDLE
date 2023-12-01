class GNCounter:
    def __init__(self,inital_value=0):
        self.gn_counter = inital_value

    def increment(self, amount=1):
        self.gn_counter += amount

    def merge(self, other):
        self.gn_counter = max(self.gn_counter, other.gn_counter)
