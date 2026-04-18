import requests

card_suits_display = {
    "S": "Spades",
    "H": "Hearts",
    "C": "Clubs",
    "D": "Diamonds",
}

# Aces high for now
card_values = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

card_values_display = {
    "1": "One",
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eight",
    "9": "Nine",
    "0": "Ten",
    "J": "Jack",
    "Q": "Queen",
    "K": "King",
    "A": "Ace",
}


baseurl = "https://deckofcardsapi.com/api/deck/"

#blackjack uses multiple (6?)
deck_count = {
    "poker": 1,
    "blackjack": 1, # Should be more, but right now not necessary
}

game_draw = {
    "poker": 5,
    "blackjack": 2,
}

def new_table(gametype):
    deck_of_cards = requests.get(baseurl + "new/shuffle/?deck_count=" + str(deck_count[gametype]))
    return deck_of_cards.json()


def draw_cards(deck_id, gametype):
    hand = requests.get(baseurl + deck_id + "/draw/?count=" + str(game_draw[gametype]))
    hand_data = hand.json()
    return [x["code"] for x in hand_data["cards"]]

def hit_me(deck_id, current_hand):
    hand = requests.get(baseurl + deck_id + "/draw/?count=1")
    hand_data = hand.json()
    temp_hand = [x["code"] for x in hand_data["cards"]]
    return current_hand + temp_hand

# Does not work for multiple decks (i.e. blackjack)
def discard(deck_id, gametype, pile, hand):
    hand_input = ",".join(hand)
    requests.get(baseurl + deck_id + "/pile/" + pile + "/add/?cards=" + hand_input)

#
def deck_status(deck_id):
    status = requests.get(baseurl + deck_id + "/shuffle/?remaining=true")
    return status.json()["remaining"]

# Returns all cards to deck to shuffle
def shuffle(deck_id):
    status1 = requests.get(baseurl + deck_id + "/return/")
    status2 = requests.get(baseurl + deck_id + "/shuffle/")

# A card is a two character string
def card_display(card):
    return card_values_display[card[0]] + " of " + card_suits_display[card[1]]

# A hand is a list of cards
def hand_display(hand):
    hand_value = ""
    for c in hand:
        hand_value += card_display(c) + "; "
    return hand_value
        

