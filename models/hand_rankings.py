from collections import Counter
from enum import Enum
from cards import Card, Rank, Suit, Hand, Deck


class HandRanking(Enum):
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __str__(self):
        return f"{self.name.replace('_', ' ').title()}"



def get_hand(hand):
    if is_straight_flush(hand):
        return Hand(HandRanking.STRAIGHT_FLUSH, get_straight_flush(hand))
    elif is_four_of_a_kind(hand):
        return Hand(HandRanking.FOUR_OF_A_KIND, get_four_of_a_kind(hand))
    elif is_full_house(hand):
        return Hand(HandRanking.FULL_HOUSE, get_full_house(hand))
    elif is_flush(hand):
        return Hand(HandRanking.FLUSH, get_flush(hand))
    elif is_straight(hand):
        return Hand(HandRanking.STRAIGHT, get_straight(hand))
    elif is_three_of_a_kind(hand):
        return Hand(HandRanking.THREE_OF_A_KIND, get_three_of_a_kind(hand))
    elif is_two_pair(hand):
        return Hand(HandRanking.TWO_PAIR, get_two_pair(hand))
    elif is_one_pair(hand):
        return Hand(HandRanking.ONE_PAIR, get_one_pair(hand))
    return Hand(HandRanking.HIGH_CARD, get_high_card(hand))


def is_one_pair(hand):
    rank_counts = Counter(card.rank for card in hand)
    pairs = [rank for rank, count in rank_counts.items() if count == 2]
    return len(pairs) == 1

def is_two_pair(hand):
    rank_counts = Counter(card.rank for card in hand)
    pairs = [rank for rank, count in rank_counts.items() if count == 2]
    return len(pairs) >= 2

def is_three_of_a_kind(hand):
    rank_counts = Counter(card.rank for card in hand)
    return any(count == 3 for count in rank_counts.values())

def is_four_of_a_kind(hand):
    rank_counts = Counter(card.rank for card in hand)
    return any(count == 4 for count in rank_counts.values())

def is_straight(hand):
    ranks = sorted(set(card.rank.value for card in hand))
    if len(ranks) < 5:
        return False

    for i in range(len(ranks) - 4):
        if ranks[i] + 4 == ranks[i + 4]:
            return True

    # low straight Ace -> 5
    if ranks[-1] == Rank.ACE.value and ranks[3] == Rank.FIVE.value:
        return True
    return False

def is_flush(hand):
    suit_counts = Counter(card.suit for card in hand)
    return any(count >= 5 for count in suit_counts.values())

def is_full_house(hand):
    rank_counts = Counter(card.rank for card in hand)
    three_of_a_kind = sum(1 for count in rank_counts.values() if count >= 3)
    pair = sum(1 for count in rank_counts.values() if count == 2)
    return three_of_a_kind == 2 or (three_of_a_kind == 1 and pair >= 1)

def is_straight_flush(hand):
    suits = [card.suit for card in hand]
    suit_counts = Counter(suits)
    most_common_suit = suit_counts.most_common(1)[0][0]
    ranks_of_most_common_suit = [card for card in hand if card.suit == most_common_suit]
    return is_straight(ranks_of_most_common_suit)

# The below functionality will get the best 5 card hand from the 7 possible cards
# and sort them in descending order for clarity and mainly sorting purposes.
# Ex: pair looks like 5 5 A 8 7, full house 5 5 5 3 3
# This makes sorting easy as comparing two hands of the same hand ranking
# consists of simply comparing the lists lexicographically.
# Ex: straights 87654 and 76543 (easy to compare now)
# Note: The below methods are taking into account that the given 7 cards has
# already been determined to be of the given function name's hand ranking.

def get_high_card(hand):
    hand.sort(key=lambda card: card.rank.value, reverse=True)
    return hand[:5]

def get_one_pair(hand):
    rank_counts = Counter(card.rank for card in hand)
    pair = [rank for rank, count in rank_counts.items() if count == 2][0]
    pair_cards = [card for card in hand if card.rank == pair]
    remaining_cards = [card for card in hand if card.rank != pair]
    remaining_cards.sort(key=lambda card: card.rank.value, reverse=True)
    return pair_cards + remaining_cards[:3]

def get_two_pair(hand):
    rank_counts = Counter(card.rank for card in hand)
    pair_ranks = [rank for rank, count in rank_counts.items() if count == 2]
    pair_cards = [card for card in hand if card.rank in pair_ranks]
    pair_cards.sort(key=lambda card: card.rank.value, reverse=True)
    remaining_cards = [card for card in hand if card.rank not in pair_ranks]
    highest_remaining_card = max(remaining_cards, key=lambda card: card.rank.value)
    return pair_cards + [highest_remaining_card]

def get_three_of_a_kind(hand):
    rank_counts = Counter(card.rank for card in hand)
    three = [rank for rank, count in rank_counts.items() if count == 3][0]
    three_cards = [card for card in hand if card.rank == three]
    remaining_cards = [card for card in hand if card.rank != three]
    remaining_cards.sort(key=lambda card: card.rank.value, reverse=True)
    return three_cards + remaining_cards[:2]

def get_four_of_a_kind(hand):
    rank_counts = Counter(card.rank for card in hand)
    four = [rank for rank, count in rank_counts.items() if count == 4][0]
    four_cards = [card for card in hand if card.rank == four]
    remaining_cards = [card for card in hand if card.rank != four]
    remaining_cards.sort(key=lambda card: card.rank.value, reverse=True)
    highest_remaining_card = max(remaining_cards, key=lambda card: card.rank.value)
    return four_cards + [highest_remaining_card]


def get_straight(hand):
    sorted_unique_ranks = sorted(set(card.rank.value for card in hand), reverse=True)
    if Rank.ACE.value in sorted_unique_ranks:
        sorted_unique_ranks.append(1)
    for i in range(len(sorted_unique_ranks) - 4):
        if sorted_unique_ranks[i] - sorted_unique_ranks[i + 4] == 4:
            straight_ranks = sorted_unique_ranks[i:i + 5]
            straight_cards = []
            seen_ranks = set()
            for card in hand:
                if card.rank.value in straight_ranks and card.rank.value not in seen_ranks:
                    straight_cards.append(card)
                    seen_ranks.add(card.rank.value)
            straight_cards.sort(key=lambda card: card.rank.value, reverse=True)
            # ace is low: len(straight_cards) would only be 4 as the straights high end is 5
            # but aces Rank.value is 14, so sorting the ranks by value does not find the ace
            if len(straight_cards) < 5:
                ace = [card for card in hand if card.rank.value == Rank.ACE.value][0]
                straight_cards.append(ace)
            return straight_cards
    # should never get here

    return []

def get_flush(hand):
    suit_counts = Counter(card.suit for card in hand)
    flush_suit = [suit for suit, count in suit_counts.items() if count >= 5][0]
    flush_cards = [card for card in hand if card.suit == flush_suit]
    flush_cards.sort(key=lambda card: card.rank.value, reverse=True)
    return flush_cards[:5]


def get_full_house(hand):
    rank_counts = Counter(card.rank for card in hand)
    three_of_kind_ranks = sorted(
        [rank for rank, count in rank_counts.items() if count >= 3],
        key=lambda rank: rank.value,
        reverse=True,
    )
    pair_ranks = sorted(
        [rank for rank, count in rank_counts.items() if count >= 2],
        key=lambda rank: rank.value,
        reverse=True,
    )
    three_of_kind_rank = three_of_kind_ranks[0]
    three_of_kind_cards = [card for card in hand if card.rank == three_of_kind_rank]
    remaining_pair_ranks = [rank for rank in pair_ranks if rank != three_of_kind_rank]
    pair_rank = remaining_pair_ranks[0]
    pair_cards = [card for card in hand if card.rank == pair_rank][:2]
    full_house = three_of_kind_cards + pair_cards
    return full_house

def get_straight_flush(hand):
    suit_counts = Counter(card.suit for card in hand)
    flush_suit = [suit for suit, count in suit_counts.items() if count >= 5][0]
    flush_cards = [card for card in hand if card.suit == flush_suit]
    return get_straight(flush_cards)


def get_random_hand():
    deck = Deck()
    deck.shuffle()
    total_cards = [deck.draw_card() for i in range(7)]
    hand = get_hand(total_cards)
    return hand




