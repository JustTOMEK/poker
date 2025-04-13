from Card import Card
import random

class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
        self.shuffle()

    def generate_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        return [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def deal_exact_card(self, rank: str, suit: str):
        for i, card in enumerate(self.cards):
            if card.rank == rank and card.suit == suit:
                return self.cards.pop(i)