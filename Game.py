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
    return[0, 0]

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

def check_flush(ranks:list, suits:list):
    if len(set(suits)) == 1:
        ranks = sorted(ranks)
        return [6, ranks[4], ranks[3], ranks[2], ranks[1], ranks[0]]
    return [0, 0]

def check_straight(ranks:list):
    if set(ranks) == {14, 2, 3, 4, 5}:
        return [5, 5]
    # checking for all other straights
    maks = max(ranks)
    for i in range(5):
        if maks - i not in ranks:
            return [0, 0]
    return [5, maks]

def check_three(ranks: list):
    three = 0
    others = []
    for rank in ranks:
        if ranks.count(rank) == 3:
            three = rank
        else:
            others.append(rank)
    if three != 0:
        others.sort()
        return [4, three, others[1], others[0]]
    return [0, 0]

def check_two_pair(ranks: list):
    pairs = []
    fifth_card = 0
    for rank in ranks:
        if ranks.count(rank) == 2:
            pairs.append(rank)
        else:
            fifth_card = rank
    if len(pairs) == 4:
        return [3,max(pairs), min(pairs), fifth_card]
    return [0, 0]

def check_pair(ranks: list):
    pair = 0
    others = []
    for rank in ranks:
        if ranks.count(rank) == 2:
            pair = rank
        else:
            others.append(rank)
    if pair != 0:
        others.sort()
        return [2, pair, others[2], others[1], others[0]]
    return [0, 0]

def check_high_card(ranks: list):
    ranks.sort()
    return [1, ranks[4], ranks[3], ranks[2], ranks[1], ranks[0]]


def evaluate_five(hand: list):
    ranks = []
    suits = []
    for card in hand:
        suits.append(card.get_suit())
        ranks.append(int(card.get_rank()))
    check_functions = [
        lambda: check_royal_flush(ranks, suits),
        lambda: check_straight_flush(ranks, suits),
        lambda: check_four(ranks),
        lambda: check_full_house(ranks),
        lambda: check_flush(ranks, suits),
        lambda: check_straight(ranks),
        lambda: check_three(ranks),
        lambda: check_two_pair(ranks),
        lambda: check_pair(ranks),
        lambda: check_high_card(ranks)
    ]

    for check in check_functions:
        score = check()
        if score[0] != 0:
            return score


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
        self.deal_cards()

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


    def deal_cards(self):
        for player in self.players:
            player.set_card(self.deck.deal_card())
        for player in self.players:
            player.set_card(self.deck.deal_card())

    def pre_flop(self):
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
            if bet_to_call > 0:
                decision = self.on_small.ask_decision(['call', 'fold', 'raise'])
            else:
                decision = self.on_small.ask_decision(['check', 'fold', 'raise'])
            if decision == "":
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
        self.on_big = temp_player

    def deal_table(self):
        self.table_cards.append(self.deck.deal_card())

    def check_who_won(self):
        player_1_best_hand = self.evaluate_hand(self.on_big)
        player_2_best_hand = self.evaluate_hand(self.on_small)
        if player_1_best_hand == player_2_best_hand:
            print("draw")
        for i in range(5):
            if player_1_best_hand[i] > player_2_best_hand[i]:
                print("player_1 won the round")
                break
            elif player_1_best_hand[i] < player_2_best_hand[i]:
                print("player_2 won the round")
                break



    def evaluate_hand(self, player: Player):
        best_hand = [0, 0, 0 , 0, 0]
        for i in range(5):
            for j in range(5):
                if i != j:
                    for k in range(5):
                        if i != j and j!= k and k!= i:
                            hand = [self.table_cards[i], self.table_cards[j], self.table_cards[k]]
                            hand.extend(player.get_cards())
                            hand_power = evaluate_five(hand)
                            for counter, point in enumerate(hand_power):
                                print(best_hand)
                                print(hand_power)
                                if counter > len(best_hand):
                                    break
                                if point > best_hand[counter]:
                                    best_hand = hand_power
                                    break
                                elif best_hand[counter] > point:
                                    break

        return best_hand

