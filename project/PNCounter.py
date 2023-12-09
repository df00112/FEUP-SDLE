from GNCounter import GNCounter
# CRDT Type: PN-Counter
# Supports incrementing and decrementing
# Merging is done by maintaining two G-Counters
# One for positive increments and one for negative increments
# The show result is done by subtracting the negative counter from the positive counter
class PNCounter:
    def __init__(self,initial_value=0):
        self.positive_counter = GNCounter(initial_value)
        self.negative_counter = GNCounter()

    def increment(self,amount):
        self.positive_counter.increment(amount)
    
    def decrement(self,amount):
        self.negative_counter.increment(amount)
    
    def update_quantity(self,finalAmount):
        if finalAmount > self.lookup():
            self.increment(finalAmount - self.lookup())
        else:
            self.decrement(self.lookup() - finalAmount)
    
    def update_status(self,finalStatus):
        if finalStatus == self.lookup():
            return
        
        if finalStatus>self.lookup():
            self.increment(1)
        else:
            self.decrement(1)
        
    
    def merge(self, other):
        self.positive_counter.merge(other.positive_counter)
        self.negative_counter.merge(other.negative_counter)
        
    def lookup(self):
        #print("Positive Counter:",self.positive_counter.gn_counter)
        #print("Negative Counter:",self.negative_counter.gn_counter)
        return self.positive_counter.gn_counter - self.negative_counter.gn_counter
    
    

