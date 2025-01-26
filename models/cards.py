from enum import Enum
import random



class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card:
        def __init__(self, suit, rank):
            self.suit = suit
            self.rank = rank

        def __str__(self):
            return f"{self.rank.name.capitalize()} of {self.suit.value}"


class Deck:
    def __init__(self):
        #Generates all 52 cards using Suit and Rank enums
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        random.shuffle(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None


    def __str__(self):
        return f"Deck of {len(self.cards)} cards"

class Hand:
    def __init__(self, hand_ranking, hand):
        self.hand_rank = hand_ranking
        self.hand = hand

    def __str__(self):
        hand_rank_str = self.hand_rank.name.replace('_', ' ').title()
        hand_str = ', '.join(f"{card.rank.name} of {card.suit.name}" for card in self.hand)
        return f"{hand_rank_str}: {hand_str}"

    def __lt__(self, other):
        if self.hand_rank != other.hand_rank:
            return self.hand_rank.value < other.hand_rank.value
        # Compare tiebreakers if ranks are the same
        this_rank_nums = [card.rank.value for card in self.hand]
        other_rank_nums = [card.rank.value for card in other.hand]
        return this_rank_nums < other_rank_nums


    def __eq__(self, other):
        this_rank_nums = [card.rank.value for card in self.hand]
        other_rank_nums = [card.rank.value for card in other.hand]
        return self.hand_rank == other.hand_rank and this_rank_nums == other_rank_nums

    def __gt__(self, other):
        if self.hand_rank != other.hand_rank:
            return self.hand_rank.value > other.hand_rank.value
        this_rank_nums = [card.rank.value for card in self.hand]
        other_rank_nums = [card.rank.value for card in other.hand]
        return this_rank_nums > other_rank_nums












