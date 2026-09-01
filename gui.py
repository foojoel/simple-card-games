import tkinter as tk
import os
import blackjack as bj
import cards_api as ca

BASE_DIR = os.path.dirname(__file__)



def card2image(card_string):
    folder_name = "PNG-cards-1.3"
    cardvalue = (ca.card_values_display2[card_string[0]]).lower()
    image_name = "_of_"
    cardsuit  = (ca.card_suits_display[card_string[1]]).lower()

    image_name = cardvalue + "_of_" + cardsuit
    if len(cardvalue) > 3:
        image_name += "2"

    image_name += ".png"
    return BASE_DIR + "/" + folder_name + "/" + image_name



class BlackjackGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        self.root.title("Blackjack Game v. 0.1")
        self.root.geometry("800x600")

        self.dealer_frame = tk.Frame(root)
        self.dealer_frame.pack(pady=10)

        self.player_frame = tk.Frame(root)
        self.player_frame.pack(pady=10)

        self.dealer_cards_frame = tk.Frame(self.dealer_frame)
        self.dealer_cards_frame.pack()

        self.player_cards_frame = tk.Frame(self.player_frame)
        self.player_cards_frame.pack()

        self.controls = tk.Frame(root)
        self.controls.pack(pady=20)

        self.status = tk.Label(root, text="Welcome to Blackjack")
        self.status.pack(pady=10)

        self.dealer_score = tk.Label(self.dealer_frame, text="Dealer: 0")
        self.dealer_score.pack()

        self.dealer_cards = tk.Label(self.dealer_frame, text="")
        self.dealer_cards.pack()

        self.player_score = tk.Label(self.player_frame, text="Player: 0")
        self.player_score.pack()

        self.player_cards = tk.Label(self.player_frame, text="")
        self.player_cards.pack()        

        tk.Button(self.controls, text="Hit", command=self.hit).pack(side="left", padx=5)
        tk.Button(self.controls, text="Stand", command=self.stand).pack(side="left", padx=5)
        tk.Button(self.controls, text="New Game", command=self.new_game).pack(side="left", padx=5)

        self.new_game()

    def new_game(self):
        if self.game.active_round == True:
            self.status.config(text="Game is already in progress!")
        else:
            self.game.startgame()
            self.refresh()
            self.status.config(text="Welcome to Blackjack")

    def hit(self):
        if self.game.active_round == True:
            result = self.game.hitme()
            self.refresh()
            
            if result is not None:
                if result:
                    self.status.config(text="Player Win")
                else:
                    self.status.config(text="Dealer Win")
        else:
            self.status.config(text="You cannot hit while the game is over!")

    def stand(self):
        if self.game.active_round == True:
            result = self.game.stand()
            self.refresh()

            if result:
                self.status.config(text="Player Win")
            else:
                self.status.config(text="Dealer Win")
        else:
            self.status.config(text="The game is already over!")

    def refresh(self):
        #self.dealer_cards.config(text=ca.hand_display(self.game.dealer_hand))
        #self.player_cards.config(text=ca.hand_display(self.game.player_hand))
        self.dealer_score.config(text=f"Dealer: {bj.hand_eval(self.game.dealer_hand)}")
        self.player_score.config(text=f"Player: {bj.hand_eval(self.game.player_hand)}")
        self.display_hand(self.player_cards_frame, self.game.player_hand)
        self.display_hand(self.dealer_cards_frame, self.game.dealer_hand)

    def display_hand(self, frame, hand):
        for widget in frame.winfo_children():
            widget.destroy()

        images = []
        
        for i, card in enumerate(hand):
            iname = card2image(card)
            img = tk.PhotoImage(file=iname)
            img = img.subsample(5, 5)
            images.append(img)

            label = tk.Label(frame, image=img)
            label.grid(row=0, column=i, padx=5)

        frame.images = images



if __name__ == "__main__":
    root = tk.Tk()
    game = bj.BlackjackGame()
    app = BlackjackGUI(root, game)
    root.mainloop()
