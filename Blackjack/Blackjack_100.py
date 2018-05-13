
# coding: utf-8

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
        'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6,
          'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10,
          'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# Variable to keep playing on
playing = True


# Card class

class Card():
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + " of " + self.suit


# Deck class

class Deck():
    
    def __init__(self):
        self.deck = [Card(suit,rank) for suit in suits for rank in ranks]
    
    def __str__(self):
        #Deck composition
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__() #String representation of Card class instance.
        return "The Deck has: "+deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop() #self.deck is a list of Card objects.


class Hand():
    
    def __init__(self):
        self.cards = []
        self.value = 0      # Initialize hand value to 0
        self.aces = 0       # Keep track of number of aces in hand
    
    def add_card(self,card):
        # A card drawn from Deck is added to Hand.
        self.cards.append(card)
        # Update the hand value.
        self.value += values[card.rank] # Card rank has a value associated with it. eg. rank 'Seven':7
        # track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        # Convert ace(if available in hand) from value 11 to 1 if hand value is > 21
        # do it recursively
        while self.value>21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips():
    
    def __init__(self,total=100):
        self.total = total
        self.bet = 0       # initially bet is set to 0
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet
        


def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry, Please provide an integer!")
        else:
            if chips.bet > chips.total:
                print("Sorry! You do not have enough chips, you have {}".format(chips.total))
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    
    global playing
    while True:
        x = input('Hit or Stand? enter h or s: ')

        if x[0].lower()=='h':
            hit(deck,hand)
        elif x[0].lower()=='s':
            print("Player stands, Dealer's turn!")
            playing = False
        else:
            print("Sorry! I did not understand that, please enter only 'h' or 's'.")
            continue
        # if non of above then break
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print("<Card Hidden>")
    print(dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n')
    
def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n')
    print("\nDealer's hand=", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n')
    print("\nPlayer's hand=", player.value)


def player_busts(player,dealer,chips):
    print("PLAYER BUSTED!")
    chips.lose_bet()
    
def player_wins(player,dealer,chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("DEALER BUSTED! PLAYER WINS!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("DEALER WINS!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and Player tie! PUSH")


# Set up the players chips
player_chips = Chips()

while True:
    # Print an opening statement
    print("WELCOME TO BLACKJACK")
    
    # Create and shuffle the deck, deal two cards to player and dealer each
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    # Prompt player for their bet
    take_bet(player_chips)
    
    # Show cards, but keep dealer's one card hidden.
    show_some(player_hand, dealer_hand)
    
    while playing:
        # Prompt for player to hit or stand
        hit_or_stand(deck,player_hand)
        
        # Show cards but keep dealer's one card hidden
        show_some(player_hand, dealer_hand)
        
        # Check if player is busted.
        if player_hand.value > 21:
            show_all(player_hand, dealer_hand)
            player_busts(player_hand, dealer_hand, player_chips)
            break
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
        
        # Show all cards
        show_all(player_hand, dealer_hand)
        
        # Check different winning situations
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
        
    # Inform player of their chips total
    print("\nPlayer total chips are at: {}".format(player_chips.total))
    # ask to play again.
    new_game = input('Would you like to play again?(y/n): ')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("\nTHANK YOU FOR PLAYING!")
        break
        

