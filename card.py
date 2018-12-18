from random import shuffle

HRT = chr(3)
CLB = chr(5)
SPD = chr(6)
DIA = chr(4)


class Card(object):

	def __init__(self,rank,suit):
		if suit in ["S","C","H","D"] and rank in ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]:
			self._suit = suit
			self._rank = rank
		else:
			self._suit = "N"
			self._rank = "N"

	def show(self):
		if self._rank == "N" or self._suit == "N":
			return "[  ]"
		elif self._suit == "S":
			return "{0}{1} ".format(self._rank,SPD)
		elif self._suit == "C":
			return "{0}{1} ".format(self._rank,CLB)
		elif self._suit == "D":
			return "{0}{1} ".format(self._rank,DIA)
		elif self._suit == "H":
			return "{0}{1} ".format(self._rank,HRT)

	def getRank(self):
		return self._rank

	def getSuit(self):
		return self._suit

class Deck(object):
	def __init__(self):
		self._cards = []
		for suit in ["S","C","H","D"]:
			for rank in ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]:
				self._cards.append(Card(rank,suit))
		self._index = 0

	def getCards(self):
		s = ""
		for card in self._cards:
			s += card.show()
		return s

	def shuffleDeck(self):
		shuffle(self._cards)
		self._index = 0

	def getCard(self):
		self._index+=1
		return self._cards[self._index-1]

class Hand(object):

	def __init__(self, name, fc, sc):
		self._firstCard = fc
		self._secondCard = sc
		self._name = name
		self._hand = []
		self._rank = 0
		self._handName = ""

	def showHand(self):
		s = "{0}{1} ".format(self._firstCard.show(),self._secondCard.show())
		return s

	def setCards(self, firstCard,secondCard):
		self._firstCard = firstCard
		self._secondCard = secondCard

	def getCards(self):
		return [self._firstCard, self._secondCard]

	def setValue(self, h, v):
		self._hand = h
		self._value = v

	def getHand(self):
		return self._hand

	def getValue(self):
		return self._value

	def setKickers(self, kicks):
		self._kickers = kicks

	def getKickers(self):
		return self._kickers

	def setRank(self, hand, rank, name):
		self._hand = hand
		self._rank = rank
		self._handName = name

	def handInfo(self):
		s = ""
		for c in self._hand:
			s += c.show() + " "
		return "{0}:      {1}".format(self._handName,s)

	def getRank(self):
		return self._rank

	def getName(self):
		return self._name
		
class Dealer(object):

	def __init__(self):
		self._deck = Deck()
		self._deck.shuffleDeck()
		self._cardsDealed = False
		self._flop = False
		self._turn = False
		self._river = False
		self._table = []

	def deal(self, *players):
		self._clearTable()
		self._deck.shuffleDeck()
		for p in players:
			p.setCards(self._deck.getCard(), self._deck.getCard())
		self._cardsDealed = True
		self._flop = False
		self._turn = False
		self._river = False

	def performFlop(self):
		if self._cardsDealed and not self._flop:
			self._table.append(self._deck.getCard())
			self._table.append(self._deck.getCard())
			self._table.append(self._deck.getCard())
			self._flop = True
			self._turn = False
			self._river = False

	def performTurn(self):
		if self._flop and not self._turn:
			self._table.append(self._deck.getCard())
			self._turn = True

	def performRiver(self):
		if self._turn and not self._river:
			self._table.append(self._deck.getCard())
			self._river = True

	def showTable(self):
		s = ""
		for card in self._table:
			s += card.show() + " "
		return s

	def _clearTable(self):
		self._table = []

	def getTable(self):
		return self._table
		

