import requests

card_suits = {
    "S": "Spades",
    "H": "Hearts",
    "C": "Clubs",
    "D": "Diamonds",
}

#Aces high for now
card_faces = {
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

baseurl = "https://deckofcardsapi.com/api/deck/"

#blackjack uses multiple (6?)
deck_count = {
    "poker": 1,
    "blackjack": 6,
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

#does not work for multiple decks (i.e. blackjack)
def discard(deck_id, gametype, pile, hand):
    hand_input = ",".join(hand)
    requests.get(baseurl + deck_id + "/pile/" + pile + "/add/?cards=" + hand_input)

def deck_status(deck_id):
    status = requests.get(baseurl + deck_id + "/shuffle/?remaining=true")
    return status.json()["remaining"]
