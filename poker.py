import os, sys
import argparse
import cards_api as ca



game = "poker"

session = ca.new_table(game)

session_id = session["deck_id"]
print(session_id)

player_hand = ca.draw_cards(session_id, game)

dealer_hand = ca.draw_cards(session_id, game)
