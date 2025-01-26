from models.cards import Card, Suit as s, Rank as r
from models.hand_rankings import (
    is_straight_flush,
    is_four_of_a_kind,
    is_full_house,
    is_flush,
    is_straight,
    is_three_of_a_kind,
    is_two_pair,
    is_one_pair, get_straight, get_straight_flush, get_three_of_a_kind, get_four_of_a_kind,
    get_full_house, get_flush, get_two_pair, get_one_pair, HandRanking,
    get_high_card
)



def test_straight_flush():
    sf = [Card(s.HEARTS, r.FIVE),
        Card(s.HEARTS, r.SIX),
        Card(s.HEARTS, r.SEVEN),
        Card(s.HEARTS, r.EIGHT),
        Card(s.HEARTS, r.NINE),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE)]

    sf_hand = list(reversed(sf[:5]))
    assert get_straight_flush(sf) == sf_hand

    not_sf = [Card(s.HEARTS, r.FIVE),
        Card(s.HEARTS, r.SIX),
        Card(s.HEARTS, r.SEVEN),
        Card(s.HEARTS, r.EIGHT),
        Card(s.CLUBS, r.NINE),
        Card(s.CLUBS, r.TWO),
        Card(s.HEARTS, r.THREE)]
    assert is_straight_flush(sf) == True
    assert is_straight_flush(not_sf) == False



def test_three_and_four_of_a_kind():
    three_of_kind = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.FIVE),
        Card(s.HEARTS, r.NINE),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE),
        Card(s.HEARTS, r.ACE),
    ]
    three_of_kind_hand = three_of_kind[:3] + [three_of_kind[6], three_of_kind[3]]
    assert get_three_of_a_kind(three_of_kind) == three_of_kind_hand
    not_three_of_kind = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.FOUR),
        Card(s.HEARTS, r.NINE),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE),
        Card(s.HEARTS, r.SEVEN),
    ]
    four_of_kind = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.FIVE),
        Card(s.DIAMONDS, r.FIVE),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE),
        Card(s.HEARTS, r.ACE),
    ]
    four_of_kind_hand = four_of_kind[:4] + [four_of_kind[6]]
    assert get_four_of_a_kind(four_of_kind) == four_of_kind_hand
    not_four_of_kind = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.FIVE),
        Card(s.DIAMONDS, r.NINE),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE),
        Card(s.HEARTS, r.SEVEN),
    ]

    assert is_three_of_a_kind(three_of_kind) == True
    assert is_three_of_a_kind(not_three_of_kind) == False
    assert is_four_of_a_kind(four_of_kind) == True
    assert is_four_of_a_kind(not_four_of_kind) == False

def test_full_house():
    #still a full house even with two three of a kinds
    full_house = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.FIVE),
        Card(s.HEARTS, r.TWO),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.TWO),
        Card(s.HEARTS, r.THREE),
    ]
    assert get_full_house(full_house) == full_house[:5]
    not_full_house = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.FOUR),
        Card(s.HEARTS, r.TWO),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE),
        Card(s.HEARTS, r.SEVEN),
    ]
    assert is_full_house(full_house) == True
    assert is_full_house(not_full_house) == False

def test_flush():
    flush = [
        Card(s.HEARTS, r.TWO),
        Card(s.HEARTS, r.FIVE),
        Card(s.HEARTS, r.NINE),
        Card(s.HEARTS, r.KING),
        Card(s.HEARTS, r.ACE),
        Card(s.CLUBS, r.THREE),
        Card(s.DIAMONDS, r.SEVEN),
    ]
    flush_hand = flush[:5]
    flush_hand.sort(key=lambda card: card.rank.value, reverse=True)
    assert get_flush(flush) == flush_hand
    not_flush = [
        Card(s.HEARTS, r.TWO),
        Card(s.HEARTS, r.FIVE),
        Card(s.HEARTS, r.NINE),
        Card(s.HEARTS, r.KING),
        Card(s.CLUBS, r.ACE),
        Card(s.CLUBS, r.THREE),
        Card(s.DIAMONDS, r.SEVEN),
    ]
    assert is_flush(flush) == True
    assert is_flush(not_flush) == False

def test_straight():
    straight = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.SIX),
        Card(s.SPADES, r.SEVEN),
        Card(s.DIAMONDS, r.EIGHT),
        Card(s.HEARTS, r.NINE),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE),
    ]
    assert get_straight(straight) == list(reversed(straight[:5]))
    low_straight = [
        Card(s.HEARTS, r.ACE),
        Card(s.CLUBS, r.TWO),
        Card(s.SPADES, r.THREE),
        Card(s.DIAMONDS, r.FOUR),
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.EIGHT),
        Card(s.DIAMONDS, r.THREE),
    ]
    assert get_straight(low_straight) == list(reversed(low_straight[:5]))
    not_straight = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.SIX),
        Card(s.SPADES, r.SEVEN),
        Card(s.DIAMONDS, r.EIGHT),
        Card(s.HEARTS, r.TEN),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE),
    ]
    assert is_straight(straight) == True
    assert is_straight(low_straight) == True
    assert is_straight(not_straight) == False

def test_two_pair():
    two_pair = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.NINE),
        Card(s.HEARTS, r.NINE),
        Card(s.CLUBS, r.TWO),
        Card(s.DIAMONDS, r.THREE),
        Card(s.HEARTS, r.ACE),
    ]
    assert get_two_pair(two_pair) == [two_pair[2],two_pair[3],two_pair[0],two_pair[1],two_pair[6]]
    not_two_pair = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.NINE),
        Card(s.HEARTS, r.TWO),
        Card(s.CLUBS, r.THREE),
        Card(s.DIAMONDS, r.FOUR),
        Card(s.HEARTS, r.SEVEN),
    ]
    assert is_two_pair(two_pair) == True
    assert is_two_pair(not_two_pair) == False

def test_one_pair():
    one_pair = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.FIVE),
        Card(s.SPADES, r.NINE),
        Card(s.HEARTS, r.TWO),
        Card(s.CLUBS, r.THREE),
        Card(s.DIAMONDS, r.FOUR),
        Card(s.HEARTS, r.SEVEN),
    ]
    assert get_one_pair(one_pair) == [one_pair[0],one_pair[1],one_pair[2],one_pair[6],one_pair[5]]
    not_one_pair = [
        Card(s.HEARTS, r.FIVE),
        Card(s.CLUBS, r.SIX),
        Card(s.SPADES, r.NINE),
        Card(s.HEARTS, r.TWO),
        Card(s.CLUBS, r.THREE),
        Card(s.DIAMONDS, r.FOUR),
        Card(s.HEARTS, r.SEVEN),
    ]
    assert is_one_pair(one_pair) == True
    assert is_one_pair(not_one_pair) == False

def test_high_card():
    high_card = [
        Card(s.HEARTS, r.ACE),
        Card(s.CLUBS, r.KING),
        Card(s.SPADES, r.QUEEN),
        Card(s.HEARTS, r.JACK),
        Card(s.CLUBS, r.NINE),
        Card(s.DIAMONDS, r.EIGHT),
        Card(s.HEARTS, r.SEVEN),
    ]
    assert get_high_card(high_card) == high_card[:5]
