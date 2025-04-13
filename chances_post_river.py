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

def evaluate_player_hand(player_hand: list, table_cards: list):
    best_hand_power = [0, 0, 0 , 0, 0]
    best_hand = []
    for i in range(5):
        for j in range(5):
            if i != j:
                for k in range(5):
                    if i != j and j!= k and k!= i:
                        hand = [table_cards[i], table_cards[j], table_cards[k]]
                        hand.extend(player_hand)
                        hand_power = evaluate_five(hand)
                        for counter, point in enumerate(hand_power):
                            if counter > len(best_hand_power):
                                break
                            if point > best_hand_power[counter]:
                                best_hand_power = hand_power
                                best_hand = hand
                                break
                            elif best_hand_power[counter] > point:
                                break

    return best_hand, best_hand_power

def evaluate_power_on_river(hand: list, table_cards: list, deck: Deck):
    player_hand_power = evaluate_player_hand(hand, table_cards)
    available_cards = deck.cards
    better_hands = 0
    exact_same_hands = 0
    worse_hands = 0
    for i in table_cards:
        for j in table_cards:
            for k in table_cards:
                for x in available_cards:
                    for y in available_cards:
                        if len(set([i, j , k])) == 3 and x != y:
                            hand = [i, j, k, x, y]
                            hand_power = evaluate_five(hand)
                            if hand_power == player_hand_power[1]:
                                exact_same_hands += 1
                                break
                            for counter in range(6):
                                if hand_power[counter] > player_hand_power[1][counter]:
                                    better_hands += 1
                                    break
                                else:
                                    worse_hands += 1
                                    break
    print('Table cards are: ' + ', '.join(str(card) for card in table_cards))
    print('Player hand is: ' + ', '.join(str(card) for card in player_hand_power[0]))
    print('There are ' + str(better_hands) + ' better hands')
    print('There are ' + str(worse_hands) + ' worse hands')
    print('There are ' + str(exact_same_hands) + ' draw hands')



"""
deck = Deck()
player = Player()
table_cards=[]
for i in range(2):
    player.set_card(deck.deal_card())

for i in range(5):
    table_cards.append(deck.deal_card())

evaluate_power_on_river(player.get_cards(), table_cards, deck)
"""

table_cards_to_pass = [('4', 'Hearts'), ('2', 'Spades'), ('3', 'Clubs'), ('14', 'Spades'), ('14', 'Clubs')]
player_cards_to_pass = [('14', 'Diamonds'), ('14', 'Hearts')]

deck = Deck()
player = Player()
table_cards=[]

for rank, suit in table_cards_to_pass:
    table_cards.append(deck.deal_exact_card(rank, suit))

for rank, suit in player_cards_to_pass:
    player.set_card(deck.deal_exact_card(rank, suit))

evaluate_power_on_river(player.get_cards(), table_cards, deck)