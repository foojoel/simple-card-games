import os, sys
import argparse
import cards_api as ca

game = "blackjack"

session = ca.new_table(game)

session_id = session["deck_id"]
print(session_id)

player_hand = ca.draw_cards(session_id, game)

dealer_hand = ca.draw_cards(session_id, game)

print(player_hand)

print(dealer_hand)

def hand_eval(hand):
    hand_value = [x[0] for x in hand]
    hand_score = 0
    ace_count = 0
    for c in hand_value:
        if c in ['J', 'Q', 'K']:
            hand_score += 10
        elif c == 'A':
            hand_score += 11            
            ace_count += 1
        else:
            hand_score += int(c)

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

print(score_round(player_hand, dealer_hand))