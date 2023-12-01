from GNCounter import GNCounter
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
        if finalStatus == True:
            self.increment(1)
        else:
            self.decrement(1)
        
    
    def merge(self, other):
        self.positive_counter.merge(other.positive_counter)
        self.negative_counter.merge(other.negative_counter)
        
    def lookup(self):
        return self.positive_counter.gn_counter - self.negative_counter.gn_counter
    
    

