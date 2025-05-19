from logic.Card import Card

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

    def bet(self, chips:int):
        self.chips -= chips
        return chips

    def get_chips(self, chips:int):
        self.chips += chips

    def check_chips(self):
        return self.chips

    def ask_decision(self, available_decisions):
        print("Whats your decision: raise x, call, fold, check")
        decision = "None"
        while decision.split()[0] not in available_decisions:
            decision = input()
        return decision