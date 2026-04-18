import os, sys
import argparse
import cards_api as ca

game = "blackjack"

def hand_eval(hand):
    hand_value = [x[0] for x in hand]
    hand_score = 0
    ace_count = 0
    for c in hand_value:
        hand_score += ca.card_values[c]
        if c == 'A':           
            ace_count += 1

    while hand_score > 21 and ace_count > 0:
        hand_score -= 10
        ace_count -= 1
    return hand_score

def score_round(player, dealer):
    victory = True
    if hand_eval(player) > 21:
        victory = False
    elif hand_eval(dealer) < 21:
        if hand_eval(player) < hand_eval(dealer):
            victory = False
    else:
        victory = True
    return victory

#print(score_round(player_hand, dealer_hand))

def startgame_call(blackjackobj):
    blackjackobj.startgame()
    print("The dealer's hand is:")
    print(ca.hand_display(blackjackobj.dealer_hand))
    print("The player's hand is: ")
    print(ca.hand_display(blackjackobj.player_hand))

def hitme_call(blackjackobj):
    blackjackobj.hitme()
    print("The player's hand is:")
    print(ca.hand_display(blackjackobj.player_hand))

def stand_call(blackjackobj):
    blackjackobj.stand()
    print("The game result is:")
    if blackjackobj.stand():
        print("Player win")
    else:
        print("Dealer win")

def exitgame_call():
    print("Okay")

def instructions_call():
        print("Here are your options. Input command in text:")
        print("1. Start")
        print("2. Hit")
        print("3. Stand")
        print("4. Instructions")
        print("5. Exit")
# Wrapper functions
commands = {
    "start": startgame_call,
    "hit": hitme_call,
    "stand": stand_call,
    "instructions": instructions_call,
    "exit": exitgame_call,    
}

class BlackjackGame:
    def __init__(self):
        self.deck_id = ca.new_table(game)["deck_id"]
        self.player_hand = []
        self.dealer_hand = []
        self.game_count = 0
        self.active_round = False

    def startgame(self):
        if self.active_round == True:
            print("There is already a game in progress!")
        else:
            ca.shuffle(self.deck_id)
            self.player_hand = ca.draw_cards(self.deck_id, game)
            self.dealer_hand = ca.draw_cards(self.deck_id, game)
            self.active_round = True

    def hitme(self):
        if hand_eval(self.player_hand) <= 21:
            self.player_hand = ca.hit_me(self.deck_id, self.player_hand)
        else:
            print("Player bust")
    
    def stand(self):
        while hand_eval(self.dealer_hand) < 17:
            self.dealer_hand = ca.hit_me(self.deck_id, self.dealer_hand)
    
    def endround(self):
        self.game_count += 1
        self.active_roud = False
        return score_round(self.player_hand, self.dealer_hand)


def blackjack_app():
    currentgame = BlackjackGame()
    print("Welcome to the Blackjack Table")
    instructions_call()

    while True:
        choice = input("What would you like to do? ").strip().lower()
        action = commands.get(choice)
        if choice == "exit":
            break
        elif choice in commands: # need to fix using wrapper functions
            action(currentgame)
        else:
            print("Unexpected command, break initiated")
            break

        

blackjack_app()
