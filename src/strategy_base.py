# Abstract class for strategies

class BaseStrategy:
    def __init__(self, name):
        self.name = name
    
    def generate_signals(self, df):
        raise NotImplementedError
    
    def __str__(self):
        return self.name

class SMACrossover(BaseStrategy):
    def generate_signals(self, df):
        # returns df["Signal"] = 1/-1/0
        pass
