class Code:
    def __init__(self , probability : float  , code : str , bit : bool):
        self.probability = probability
        self.code = code
        # self.bit = bit
    def __repr__(self):
        return f"({self.probability} , {self.code} , {self.bit})"
    def __str__(self):
        return f"({self.probability} , {self.code} , {self.bit})"
    def __eq__(self, other):
        if isinstance(other , Code):
            return self.probability == other.probability
        else:
            return False
    def __lt__(self, other):
        if isinstance(other , Code):
            return self.probability < other.probability
        else:
            return False

    def __gt__(self, other):
        if isinstance(other , Code):
            return self.probability > other.probability
        else:
            return False