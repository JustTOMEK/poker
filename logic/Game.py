from logic.GuiPlayer import GuiPlayer
from logic.Player import Player
from logic.Deck import Deck


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
        self.deck = None
        self.on_big = self.players[0]
        self.on_small = self.players[1]
        self.table_cards = []
        self.round_pot = 0
        self.end_round = 0
        self.round_stage = None
        self.stage_in_progress = None
        self.bet_to_call = 0
        self.decision_in_the_round = 0

    def is_finished(self):
        if self.players[0].check_chips() == 0 or self.players[1].check_chips() == 0:
            return True
        return False

    def start_game(self):
        for player in self.players:
            player.set_chips(self.start_chips)

    def start_round(self):
        self.round_pot = 0
        self.deal_cards()
        self.round_stage = "preflop"
        self.stage_in_progress = True
        self.decision_in_the_round = 0
        self.pre_flop()

    def progress(self, waiting_for_input, decision):
        # TO DO FIX reraising and go through in game scenarios changing stages
        if not self.stage_in_progress:
            self.change_stage()
            return
        elif not isinstance(self.on_small, GuiPlayer):
            if self.bet_to_call > 0:
                decision = self.on_small.ask_decision(['call', 'fold', 'raise'])
            else:
                decision = self.on_small.ask_decision(['check', 'fold', 'raise'])
        elif isinstance(self.on_small, GuiPlayer) and waiting_for_input:
            return
        self.decision_in_the_round += 1
        if decision== "call":
            if self.decision_in_the_round > 1:
                self.stage_in_progress = False
            self.round_pot += self.on_small.bet(self.bet_to_call)
            self.bet_to_call = 0

        if decision[0].lower() == "r":
            bet = self.on_small.bet(int(decision.split()[1]))
            self.round_pot+=bet
            self.bet_to_call = bet - self.bet_to_call

        if decision == "check":
            if self.decision_in_the_round > 1:
                self.stage_in_progress = False

        if decision == "fold":
            self.on_big.get_chips(self.round_pot)
            self.stage_in_progress = False
        self.change_turn()


    def change_stage(self):
        if self.round_stage == "preflop":
            self.round_stage = "flop"
            self.flop()
            self.stage_in_progress = True
        elif self.round_stage == "flop":
            self.round_stage = "turn"
            self.turn()
            self.stage_in_progress = True
        elif self.round_stage == "turn":
            self.round_stage = "river"
            self.river()
            self.stage_in_progress = True
        elif self.round_stage == "river":
            self.round_stage = "turn"
            self.showdown()
            self.stage_in_progress = False
        self.decision_in_the_round = 0
        self.bet_to_call = 0

    def deal_cards(self):
        self.deck = Deck()
        self.table_cards = []
        for player in self.players:
            player.get_rid_of_cards()
            player.set_card(self.deck.deal_card())
            player.set_card(self.deck.deal_card())

    def pre_flop(self):
        self.put_blinds()
        self.bet_to_call = self.small_blind

    def flop(self):
        for i in range(3):
            self.table_cards.append(self.deck.deal_card())

    def turn(self):
        self.table_cards.append(self.deck.deal_card())

    def river(self):
        self.table_cards.append(self.deck.deal_card())

    def showdown(self):
        return None

    def put_blinds(self):
        self.round_pot += self.on_big.bet(self.big_blind)
        self.round_pot += self.on_small.bet(self.small_blind)

    def change_turn(self):
        temp_player = self.on_small
        self.on_small = self.on_big
        self.on_big = temp_player

    def deal_table(self):
        self.table_cards.append(self.deck.deal_card())

    def get_table_cards(self):
        return self.table_cards

    def check_who_won(self):
        player_1_best_hand = self.evaluate_hand(self.on_big)
        player_2_best_hand = self.evaluate_hand(self.on_small)
        if player_1_best_hand == player_2_best_hand:
            print("draw")
        for i in range(5):
            if player_1_best_hand[i] > player_2_best_hand[i]:
                self.on_big.get_chips(self.round_pot)
                print("player_1 won the round")
                break
            elif player_1_best_hand[i] < player_2_best_hand[i]:
                self.on_small.get_chips(self.round_pot)
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

