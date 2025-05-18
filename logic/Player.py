from Card import Card

class Player:
    def __init__(self):
        self.chips = 0
        self.cards = []

    def set_card(self, card : Card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards[0], self.cards[1]

    def set_chips(self, chips:int):
        self.chips = chips

    def get_chips(self, chips:int):
        self.chips -= chips
        return chips
    def ask_decision(self):
        print("Whats your decision: raise x, call, fold, check")
        decision = input()
        return decision