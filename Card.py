class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit