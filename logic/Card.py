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

    def get_str_file(self):
        high_ranks = {
            '11': 'J',
            '12': 'Q',
            '13': 'K',
            '14': 'A'
        }
        if self.rank in high_ranks.keys():
            return high_ranks[self.rank] + self.suit[0]
        return self.rank + self.suit[0]
