from Player import Player
from Deck import Deck
class Game:
    def __init__(self, small_blind: int, big_blind: int, players: list[Player], start_chips: int):
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.players = players
        self.start_chips = start_chips
        self.deck = Deck()
        self.on_big = self.players[0]
        self.on_small = self.players[1]
        self.table_cards = []
        self.round_pot = 0
        self.end_round = 0

    def start_game(self):
        for player in self.players:
            player.set_chips(self.start_chips)
        self.start_round()

    def start_round(self):
        self.pre_flop()
        if not self.end_round:
            self.flop()
            if not self.end_round:
                self.turn()
                if not self.end_round:
                    self.river()
                    self.check_who_won()



    def pre_flop(self):
        for player in self.players:
            player.set_card(self.deck.deal_card())
        for player in self.players:
            player.set_card(self.deck.deal_card())
        self.put_blinds()
        self.start_betting()

    def flop(self):
        for i in range(3):
            self.table_cards.append(self.deck.deal_card())
        self.start_betting()

    def turn(self):
        self.table_cards.append(self.deck.deal_card())
        self.start_betting()

    def river(self):
        self.table_cards.append(self.deck.deal_card())
        self.start_betting()


    def put_blinds(self):
        self.round_pot += self.on_big.get_chips(self.big_blind)
        self.round_pot += self.on_small.get_chips(self.small_blind)

    def start_betting(self):
        decision = ''
        check_counter = 0
        bet_to_call = 0
        while decision not in ["fold", "call"] and check_counter != 2:
            decision = self.on_small.ask_decision()
            if (decision == ""):
                decision = "check"
            if decision[0].lower() == "r":
                bet = self.on_small.get_chips(int(decision.split()[1]))
                self.round_pot+=bet
                bet_to_call = bet
            if decision== "call":
                self.round_pot += self.on_small.get_chips(bet_to_call)
            if decision == "check":
                check_counter+=1
            if decision == "fold":
                self.end_round = 1
            self.change_turn()
        print('end of round')



    def change_turn(self):
        temp_player = self.on_small
        self.on_small = self.on_big
        self.on_big = self.on_small

    def deal_table(self):
        self.table_cards.append(self.deck.deal_card())

    def check_who_won(self):
        player_1_best_hand = self.evaluate_hand(self.on_big)

    def evaluate_hand(self, player: Player):
        best_hand = [1, 1]
        for i in range(5):
            for j in range(5):
                if i != j:
                    for k in range(5):
                        if i != j and j!= k and k!= i:
                            print(str(i)+ " " + str(j) + " " + str(k))
                            hand = [self.table_cards[i], self.table_cards[j], self.table_cards[k]]
                            hand.extend(player.get_cards())
                            hand_power = self.evaluate_five(hand)

    def evaluate_five(self, hand: list):
        ranks = []
        suits = []
        for card in hand:
            suits.append(card.get_suit())
            ranks.append(card.get_rank())
            None
