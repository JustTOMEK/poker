from Player import Player
from Deck import Deck


def check_royal_flush(ranks:list, suits:list):
    if len(set(suits)) == 1 and set(ranks) == {10, 11, 12, 13, 14}:
        return [10, 1]
    else:
        return [0, 0]

def check_straight_flush(ranks:list , suits:list):
    if len(set(suits)) == 1:
        #checking for straight with ace
        if set(ranks) == {14, 2, 3, 4, 5}:
            return [9, 5]
        #checking for all other straights
        maks = max(ranks)
        for i in range(5):
            if maks - i not in ranks:
                return [0, 0]
        return [9, maks]

def check_four(ranks:list):
    four_rank = 0
    card = 0
    for rank in ranks:
        if ranks.count(rank) == 4:
            four_rank = rank
        else:
            card = rank
    if four_rank != 0:
        return [8, four_rank, card]
    return [0, 0]

def check_full_house(ranks:list):
    if len(set(ranks)) == 2:
        three_pair = 0
        two_pair = 0
        for rank in ranks:
            if ranks.count(rank) == 2:
                two_pair = rank
            else:
                three_pair = rank
        return [7, three_pair, two_pair]
    return [0, 0]

print(check_full_house([14, 14, 14, 3, 3]) == check_full_house([14, 14, 14, 3, 3]))

def check_flush(ranks:list, suits:list):
    if len(set(suits)) == 1:
        ranks = sorted(ranks)
        return [6, ranks[4], ranks[3], ranks[2], ranks[1], ranks[0]]
    return [0, 0]

def check_straight(ranks:list, suits:list):
    None

print(check_flush([4,7 ,8 ,6 ,4], [1,1,1,1,1]))

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
        score = check_royal_flush(ranks, suits)
        if score[0] == 10:
            return score
        score = check_straight_flush(ranks, suits)
