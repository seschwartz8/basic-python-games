# Blackjack by Sarah Schwartz

import simplegui
import random
WIDTH = 600
HEIGHT = 600

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}



# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create an empty hand
        self.hand_cards = []

    def __str__(self):
        # string of what the hand contains
        string_hand = ""
        for c in range(len(self.hand_cards)):
            string_hand += " " + str(self.hand_cards[c])
        return "Hand contains:" + string_hand

    def add_card(self, card):
        # add a card to the hand
        self.hand_cards.append(card)

    def get_value(self):
        hand_value = 0
        has_ace = False
        
        for c in self.hand_cards: # hand_value is sum of card values with Ace as 1
               hand_value += VALUES[c.get_rank()]
        
        for c in self.hand_cards: # boolean to determine if Ace present
            if c.get_rank() == "A":
                has_ace = True
                break
            else:
                has_ace = False
        
        if has_ace == False: # Compute hand_value for ZERO aces in hand
            return hand_value
        else: #Compute hand_value for presence of 1 or 2 aces
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
   
    def draw(self, canvas, pos): # draw hand on canvas using draw method for cards
        for c in self.hand_cards:
            c.draw(canvas, pos)
            pos = [pos[0] + CARD_SIZE[0], pos[1]]

        
# define deck class 
class Deck:
    def __init__(self):
        # create the deck
        self.deck_cards = []
        for s in SUITS:
            for r in RANKS:
                card = Card(s, r)
                self.deck_cards.append(card)
        return self.deck_cards

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_cards)
        return self

    def deal_card(self):
        # deal a card object from the deck
        return self.deck_cards.pop(-1)
    
    def __str__(self):
        # return a string representing the deck
        string_deck = ""
        for c in range(len(self.deck_cards)):
            string_deck += " " + str(self.deck_cards[c])
        return "Deck contains:" + string_deck



#define event handlers for buttons
def deal():
    # creates and shuffles deck, creates hands
    global outcome, in_play, final_deck, player_hand, dealer_hand, score
    final_deck = Deck()
    final_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    
    for r in range(2): # deal 2 cards to dealer
        dealt_card = final_deck.deal_card()
        dealer_hand.add_card(dealt_card)
    for r in range(2): # deal 2 cards to player
        dealt_card =final_deck.deal_card()
        player_hand.add_card(dealt_card)
    
    if in_play == False:
        in_play = True
        outcome = "New Game! Hit or stand?"
    elif in_play == True:
        outcome = "Game Forfeited! Hit or stand?"
        score -= 1
    

def hit():
    global in_play, outcome, score
    if (in_play == True) and (player_hand.get_value() <= 21): # if the hand is in play, hit the player
        dealt_card = final_deck.deal_card()
        player_hand.add_card(dealt_card)
        outcome = "Player Hits. Hit or stand?"
    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "YOU HAVE BUSTED!"
            score -= 1
            in_play = False
 
       
def stand():
    global in_play, score, outcome
    if (in_play == True):# if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer_hand.get_value() < 17:
            dealt_card = final_deck.deal_card()
            dealer_hand.add_card(dealt_card)
        
    else: #if hand is not in play, remind player they busted
        outcome = "Game is over. Deal a new game."
    
    if (dealer_hand.get_value() > 21) and (in_play == True):
        outcome = "DEALER BUSTS! YOU WIN!"
        score += 1
        in_play = False
    # compare hand to see who wins:
    elif (player_hand.get_value() <= dealer_hand.get_value()) and (in_play == True):
        outcome = "DEALER WINS"
        score -= 1
        in_play = False
    elif (player_hand.get_value() > dealer_hand.get_value()) and (in_play == True):
        outcome = "YOU WIN"
        score += 1
        in_play = False
    

# draw handler    
def draw(canvas):
    
    #draw hands
    dealer_hand.draw(canvas, [50, 100])
    player_hand.draw(canvas, [50, 400])
    
    #draw name of game and player titles
    canvas.draw_text("Blackjack", (WIDTH/2, 70), 50, 'Yellow')
    canvas.draw_text("Dealer's hand:", (50, 70), 30, 'White')
    canvas.draw_text("Your hand:", (50, 370), 30, 'White')
    
    #draw outcome
    canvas.draw_text(outcome, (WIDTH/2, 300), 20, 'White')
    
    #draw score
    canvas.draw_text("Score: " + str(score), (WIDTH/2, 350), 20, 'White')
    
    #draw player's hand value
    canvas.draw_text("My value: " + str(player_hand.get_value()), (70, 550), 20, 'White')

    #cover dealer's first card if in_play
    if in_play:
        card_back_loc = (CARD_BACK_CENTER[0], 
                         CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 100 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE) 




# initialization frame
frame = simplegui.create_frame("Blackjack", WIDTH, HEIGHT)
frame.set_canvas_background("Blue")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
