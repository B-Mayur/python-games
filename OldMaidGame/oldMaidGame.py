class Card:
	suitList = ['Clubs','Diamonds', 'Hearts', 'Spades']
	rankList = ['narf', 'Ace', '2', '3',\
				'4', '5', '6', '7', '8',\
				'9', '10', 'Jack', 'Queen', 'King']
	def __init__(self, suit=0, rank=0):
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return ("{} of {}".format(self.rankList[self.rank],self.suitList[self.suit]))
	def __repr__(self):
		return ("{} of {}".format(self.rankList[self.rank], self.suitList[self.suit]))

		# Rich Comparisons
		# ==
	def __eq__(self,other):
		return (self.suit,self.rank) == (other.suit, other.rank)
		# !=
	def __ne__(self,other):
		return not(self==other)
		# <
	def __lt__(self,other):
		if (self==other): return False
		if (self.suit < other.suit): return True
		if (self.suit > other.suit): return False
		if (self.rank < other.rank): return True 
		return False
		# <=
	def __le__(self,other):
		return (self<other or self==other)
		# >
	def __gt__(self,other):
		if(self==other): return False
		if(self.suit > other.suit): return True
		if(self.suit < other.suit): return False
		if(self.rank > other.rank): return True
		return False
		# >=
	def __ge__(self,other):
		return (self==other or self>other)

class Deck:
	def __init__(self):
		self.cards = []
		for suit in range(0,4):
			for rank in range(1,14):
				self.cards.append(Card(suit,rank))
	def printDeck(self):
		for card in self.cards:
			print(card)
	def __str__(self):
		s = ""
		for i in range(len(self.cards)):
			s = s + " "*i + str(self.cards[i]) + "\n"
		return s

	def shuffle(self):
		import random
		nCards = len(self.cards)
		for i in range(nCards):
			j = random.randrange(i,nCards)
			self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
	def removeCard(self,card):
		if card in self.cards:
			self.cards.remove(card)
			return 1
		else:
			return 0
	def popCard(self):
		return self.cards.pop()
	def isEmpty(self):
		return (len(self.cards) == 0)
	def deal(self,hands,nCards=999):
		# no. of hands.
		nHands = len(hands)
		for i in range(nCards):
			if self.isEmpty():break 	# Break if out of cards
			card = self.popCard()
			hand = hands[i%nHands] 			# whose turn is next?
			hand.addCard(card) 				# add the card to the hand

class Hand(Deck):
	def __init__(self,name=""):
		self.cards = []
		self.name = name

	def addCard(self,card):
		self.cards.append(card)

	def __str__(self):
		s = "Hand " + self.name
		if self.isEmpty():
			s = s + " is empty.\n"
		else:
			s = s + " contains\n"
		return s + Deck.__str__(self)

class CardGame:
	def __init__(self):
		self.deck = Deck()
		self.deck.shuffle()

class OldMaidHand(Hand):
	def removeMatches(self):
		count = 0
		originalCards = self.cards[:] # For traversal purpose
		for card in originalCards:
			match = Card(3-card.suit,card.rank)
			if match in self.cards:
				self.cards.remove(match)
				self.cards.remove(card)
				print("Hand {name}: {card} matches {match}.".format(name=self.name, card=card, match=match))
				count += 1
		return count

class OldMaidGame(CardGame):
	def play(self,names):
		# Remove queen of clubs
		self.deck.removeCard(Card(0,12))

		# Make a hand for each player.
		self.hands = []
		for name in names:
			self.hands.append(OldMaidHand(name)) # Created hand object and append to hands list.

		# Deal the cards.
		self.deck.deal(self.hands) # Deal all cards.
		print("--------- Cards have been dealt.")
		self.printHands()

		# Remove initial matches.
		matches = self.removeAllMatches()
		print("--------- Matches discarded. Play begins.")
		self.printHands()

		# Play until all 50 cards are matched.
		turn = 0
		numHands = len(self.hands)
		# Play until all 50 cards are matched
		while matches < 25:
			matches = matches + self.playOneTurn(turn)
			turn = (turn+1) % numHands
		print("--------- Game is Over.\n")
		self.printHands()
		# Find loser and print on console.
		for hand in self.hands:
			if not hand.isEmpty():
				print(">>>>> {name} lost the game. <<<<<".format(name=hand.name))

	def removeAllMatches(self):
		count = 0
		for hand in self.hands:
			count = count + hand.removeMatches()
		return count

	def printHands(self):
		for hand in self.hands:
			print(hand)

	def playOneTurn(self,i):
		if self.hands[i].isEmpty():
			return 0
		neighbor = self.findNeighbor(i)
		pickedCard = self.hands[neighbor].popCard()
		self.hands[i].addCard(pickedCard)
		print("Hand {name} picked {card}".format(name=self.hands[i].name, card = pickedCard))
		count = self.hands[i].removeMatches()
		# Shuffle the hand.
		self.hands[i].shuffle()
		return count

	def findNeighbor(self,i):
		numHands = len(self.hands)
		for next in range(1,numHands):
			neighbor = (i+next) % numHands
			if (not self.hands[neighbor].isEmpty()):
				return neighbor