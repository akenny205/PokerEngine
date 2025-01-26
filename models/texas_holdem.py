from enum import Enum
from cards import Deck
from hand_rankings import get_hand


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.hole_cards = []  # Two cards dealt to the player
        self.chips = chips
        self.current_bet = 0
        self.folded = False

    def __str__(self):
        return f"{self.name} (Chips: {self.chips}, Hole Cards: {self.hole_cards})"

    def fold(self):
        self.folded = True



    def bet(self, amount):
        self.current_bet = min(self.chips, amount)
        self.chips = max(0, self.chips - amount)



class Stage(Enum):
    PRE_FLOP = 1
    POST_FLOP = 2
    TURN = 3
    RIVER = 4
    SHOWDOWN = 5


class TexasHoldEmRound:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.community_cards = []
        self.pot = 0
        self.current_stage = Stage.PRE_FLOP

    def add_player(self, player):
        self.players.append(player)

    # removes last player
    def remove_player(self):
        self.players.pop(-1)

    def deal_hole_cards(self):
        self.deck.shuffle()
        for player in self.players:
            player.hole_cards = [self.deck.draw_card(), self.deck.draw_card()]

    def deal_community_cards(self, num_cards):
        self.community_cards.extend([self.deck.draw_card() for _ in range(num_cards)])

    # bets = dictionary: player_name -> bet
    def betting_round(self, bets):
        for player in self.players:
            if not player.folded:
                bet = bets[player.name]
                player.bet(bet)
                self.pot += bet
                print(f"{player.name} bets {bet} chips.")

    def winning_players(self):
        non_folded_players = [player for player in self.players if not player.folded]
        non_folded_player_hands = []
        for player in non_folded_players:
            player_hand = get_hand(player.hole_cards + self.community_cards)
            non_folded_player_hands.append(player_hand)
        current_best_hand = non_folded_player_hands[0]
        for hand in non_folded_player_hands:
            if current_best_hand < hand:
                current_best_hand = hand
        winners = []
        for i in range(len(non_folded_players)):
            if non_folded_player_hands[i] == current_best_hand:
                winners.append(non_folded_players[i])
        return winners











