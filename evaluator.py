import card
#_suits[0="H" 1="S" 2="D" 3="C"]

HRT = chr(3)
CLB = chr(5)
SPD = chr(6)
DIA = chr(4)

class Evaluator(object):
	def __init__(self):
		self._cards = []
		self._suits = [0,0,0,0]
		self._ranks= [0,0,0,0,0,0,0,0,0,0,0,0,0]
		self._rankVals = [[2,3,5,7,11,13,17,19,23,29,31,37,41],   #wysokie
						  [43,47,53,59,61,67,71,73,79,83,89,97,101],  #pary
						  [103,107,109,113,127,131,137,139,149,151,157,163,167]] #trojki
		#[0:wysoka, 1:para, 2:dwie pary, 3:trojka, 4:strit, 5:kolor, 6:ful, 7:kareta, 8:poker]
		self._handVals = [241,251,257,263,269,271,277,281,283]
		self._bestHand = []

	def _countRanksAndSuits(self):

		self._suits = [0,0,0,0]
		self._ranks = [0,0,0,0,0,0,0,0,0,0,0,0,0]
		self._allCards = [[0,0,0,0,0,0,0,0,0,0,0,0,0],
						  [0,0,0,0,0,0,0,0,0,0,0,0,0],
						  [0,0,0,0,0,0,0,0,0,0,0,0,0],
						  [0,0,0,0,0,0,0,0,0,0,0,0,0]]
		for c in self._cards:
			if c.show() != "[  ]":
				s = c.getSuit()
				r = c.getRank()

				suit = 0
				rank = 0

				if s == "H": 
					self._suits[0] += 1
					suit = 0
				if s == "S": 
					self._suits[1] += 1
					suit = 1
				if s == "D": 
					self._suits[2] += 1
					suit = 2
				if s == "C": 
					self._suits[3] += 1
					suit = 3

				if r == "2": self._ranks[0] += 1; rank = 0 
				if r == "3": self._ranks[1] += 1; rank = 1 
				if r == "4": self._ranks[2] += 1; rank = 2 
				if r == "5": self._ranks[3] += 1; rank = 3 
				if r == "6": self._ranks[4] += 1; rank = 4 
				if r == "7": self._ranks[5] += 1; rank = 5 
				if r == "8": self._ranks[6] += 1; rank = 6 
				if r == "9": self._ranks[7] += 1; rank = 7 
				if r == "10": self._ranks[8] += 1; rank = 8 
				if r == "J": self._ranks[9] += 1; rank = 9 
				if r == "Q": self._ranks[10] += 1; rank = 10
				if r == "K": self._ranks[11] += 1; rank = 11
				if r == "A": self._ranks[12] += 1; rank = 12

				self._allCards[suit][rank] = 1

	def _getCardFromAllCards(self,r,s):
		
		suit = ""
		if s == 0:
			suit = "H"
		elif s == 1:
			suit = "S"
		elif s == 2:
			suit = "D"
		elif s == 3:
			suit = "C"

		rank = ""
		if r == 0:
			rank = "2"
		elif r == 1:
			rank = "3"
		elif r == 2:
			rank = "4"
		elif r == 3:
			rank = "5"
		elif r == 4:
			rank = "6"
		elif r == 5:
			rank = "7"
		elif r == 6:
			rank = "8"
		elif r == 7:
			rank = "9"
		elif r == 8:
			rank = "10"
		elif r == 9:
			rank = "J"
		elif r == 10:
			rank = "Q"
		elif r == 11:
			rank = "K"
		elif r == 12:
			rank = "A"

		return card.Card(rank,suit)

	def isHighCard(self):

		card = 0
		cards = []
		hand = []
		for x in [12,11,10,9,8,7,6,5,4,3,2,1,0]:
			for y in [0,1,2,3]:
				if card < 5:
					if self._allCards[y][x] == 1:
						cards.append(x)
						hand.append(self._getCardFromAllCards(x,y))
						card += 1
	
		highcard = 1
		for x in cards:
			highcard *= self._rankVals[0][x]

		self._bestHand = hand

		return self._handVals[0] * highcard

	def isPair(self):
		index = 0
		two = -1
		for x in self._ranks:
			if x == 2:
				two = index
			index += 1
		
		if two < 0:
			return -1

		index = 0
		firstKicker = -1
		for x in self._ranks:
			if x == 1:
				firstKicker = index
			index += 1

		index = 0
		secondKicker = -1
		for x in self._ranks:
			if x == 1 and index != firstKicker:
				secondKicker = index
			index += 1

		index = 0
		thirdKicker = -1
		for x in self._ranks:
			if x == 1 and index != firstKicker and index != secondKicker:
				thirdKicker = index
			index += 1

		hand = []
		for x in [0,1,2,3]:
			if self._allCards[x][two] == 1:
				hand.append(self._getCardFromAllCards(two,x))
		for x in [0,1,2,3]:
			if self._allCards[x][firstKicker] == 1:
				hand.append(self._getCardFromAllCards(firstKicker,x))
		for x in [0,1,2,3]:
			if self._allCards[x][secondKicker] == 1:
				hand.append(self._getCardFromAllCards(secondKicker,x))
		for x in [0,1,2,3]:
			if self._allCards[x][thirdKicker] == 1:
				hand.append(self._getCardFromAllCards(thirdKicker,x))

		self._bestHand = hand

		return self._rankVals[1][two] * self._handVals[1] * self._rankVals[0][firstKicker] * self._rankVals[0][secondKicker] * self._rankVals[0][thirdKicker]

	def isTwoPairs(self):
		index = 0
		firstpair = -1
		for x in self._ranks:
			if x == 2:
				firstpair = index
			index += 1
		
		index = 0
		secondpair = -1
		for x in self._ranks:
			if x == 2 and index != firstpair:
				secondpair = index
			index += 1

		index = 0
		kicker = -1
		for x in self._ranks:
			if x == 1:
				kicker = index
			index += 1

		if firstpair < 0 or secondpair < 0:
			return -1

		hand = []
		for x in [0,1,2,3]:
			if self._allCards[x][firstpair] == 1:
				hand.append(self._getCardFromAllCards(firstpair,x))
		for x in [0,1,2,3]:
			if self._allCards[x][secondpair] == 1:
				hand.append(self._getCardFromAllCards(secondpair,x))
		for x in [0,1,2,3]:
			if self._allCards[x][kicker] == 1:
				hand.append(self._getCardFromAllCards(kicker,x))

		self._bestHand = hand

		return self._rankVals[1][firstpair] * self._rankVals[1][secondpair] * self._handVals[2] * self._rankVals[0][kicker]

	def is3ofAKind(self):
		index = 0
		three = -1
		for x in self._ranks:
			if x == 3:
				three = index
			index += 1

		if three < 0:
			return -1

		index = 0
		firstKicker = -1
		for x in self._ranks:
			if x == 1:
				firstKicker = index
			index += 1

		index = 0
		secondKicker = -1
		for x in self._ranks:
			if x == 1 and index != firstKicker:
				secondKicker = index
			index += 1

		hand = []
		for x in [0,1,2,3]:
			if self._allCards[x][three] == 1:
				hand.append(self._getCardFromAllCards(three,x))
		for x in [0,1,2,3]:
			if self._allCards[x][firstKicker] == 1:
				hand.append(self._getCardFromAllCards(firstKicker,x))
		for x in [0,1,2,3]:
			if self._allCards[x][secondKicker] == 1:
				hand.append(self._getCardFromAllCards(secondKicker,x))

		self._bestHand = hand

		return self._rankVals[2][three] * self._handVals[3] * self._rankVals[0][firstKicker] * self._rankVals[0][secondKicker] 

	def isStraight(self):
		hand = []
		if self._ranks[12] > 0 and self._ranks[0] > 0 and self._ranks[1] > 0 and self._ranks[2] > 0 and self._ranks[3] > 0:
			for x in [3,2,1,0,12]:
				for y in [0,1,2,3]:
					if self._allCards[y][x] == 1:
						hand.append(self._getCardFromAllCards(x,y))
						break
			
			self._bestHand = hand
			return self._rankVals[0][0] * self._handVals[4]
		else:
			for x in [8,7,6,5,4,3,2,1,0]:
				if self._ranks[x] > 0 and self._ranks[x+1] > 0 and self._ranks[x+2] > 0 and self._ranks[x+3] > 0 and self._ranks[x+4] > 0:
					for z in [x+4, x+3, x+2, x+1, x]:
						for y in [0,1,2,3]:
							if self._allCards[y][z] == 1:
								hand.append(self._getCardFromAllCards(z,y))
								break
					
					self._bestHand = hand
					return self._rankVals[0][x+1] * self._handVals[4]
				else:
					pass
			return -1

	def isFlush(self):
		if not 5 in self._suits and not 6 in self._suits and not 7 in self._suits:
			return -1

		hand = []
		kicker = -1
		ind = 0
		i = 0
		for x in self._allCards:
			a = x.count(1)
			if a >= 5:
				ind = i
			i += 1

		kickersLeft = 5
		kickers = 1
		for x in [12,11,10,9,8,7,6,5,4,3,2,1,0]:
			if self._allCards[ind][x] == 1 and kickersLeft > 0:
				hand.append(self._getCardFromAllCards(x,ind))
				kickers *= self._rankVals[0][x]
				kickersLeft -= 1


		hand = hand[0:5]
		self._bestHand = hand

		return kickers * self._handVals[5]

	def isFullHouse(self):
		index = 0
		three = -1
		for x in self._ranks:
			if x == 3:
				three = index
			index += 1
		
		index = 0
		pair = -1
		for x in self._ranks:
			if x == 2 or (x == 3 and index != three):
				pair = index
			index += 1

		hand = []
		for x in [0,1,2,3]:
			if self._allCards[x][three] == 1:
				hand.append(self._getCardFromAllCards(three,x))
		for x in [0,1,2,3]:
			if self._allCards[x][pair] == 1:
				hand.append(self._getCardFromAllCards(pair,x))

		hand = hand[0:5]
		self._bestHand = hand

		if three >= 0 and pair >= 0:
			
			return self._rankVals[2][three] * self._rankVals[1][pair] * self._handVals[6] 
		return -1

	def is4ofAKind(self):
		if 4 in self._ranks:

			four = self._ranks.index(4)
	
			index = 0
			kicker = -1
			for x in self._ranks:
				if x == 1:
					kicker = index
				index += 1
	
				hand = []
			for x in [0,1,2,3]:
				if self._allCards[x][four] == 1:
					hand.append(self._getCardFromAllCards(four,x))
			for x in [0,1,2,3]:
				if self._allCards[x][kicker] == 1:
					hand.append(self._getCardFromAllCards(kicker,x))
	
			self._bestHand = hand

			return self._rankVals[2][self._ranks.index(4)] * self._handVals[7] * self._rankVals[0][kicker]
		return -1

	def isStraightFlush(self):
		
		hand = []
		index = 0
		for x in self._allCards:
			if x[12] > 0 and x[0] > 0 and x[1] > 0 and x[2] > 0 and x[3] > 0:
				for y in [3,2,1,0,12]:
					hand.append(self._getCardFromAllCards(y,index))

				self._bestHand = hand

				return self._rankVals[0][0] * self._handVals[8]
			else:
				for i in [8,7,6,5,4,3,2,1,0]:
					if x[i] > 0 and x[i+1] > 0 and x[i+2] > 0 and x[i+3] > 0 and x[i+4] > 0:
						for y in [i+4,i+3,i+2,i+1,i]:
							hand.append(self._getCardFromAllCards(y,index))

						self._bestHand = hand

						return self._rankVals[0][i+1] * self._handVals[8]
			index += 1
		return -1		

	def eval(self, hand, table):
		self._cards = hand.getCards() + table
		self._countRanksAndSuits()

		rank = self.isStraightFlush()
		name = "Poker       "
		if rank < 0:
			rank = self.is4ofAKind()
			name = "Kareta      "
		if rank < 0:
			rank = self.isFullHouse()
			name = "Ful         "
		if rank < 0:
			rank = self.isFlush()
			name = "Kolor       "
		if rank < 0:
			rank = self.isStraight()
			name = "Strit       "
		if rank < 0:
			rank = self.is3ofAKind()
			name = "Trojka      "
		if rank < 0:
			rank = self.isTwoPairs()
			name = "Dwie pary   "
		if rank < 0:
			rank = self.isPair()
			name = "Para        "
		if rank < 0:
			rank = self.isHighCard()
			name = "Wysoka karta"

		hand.setRank(self._bestHand, rank, name)
		
	def toPrimes(self,num):
		primes = []
		for x in [283,281,277,271,269,263,257,251,241,167,163,157,151,149,139,137,131,127,113,109,107,103,101,97,89,83,79,73,71,67,61,59,53,47,43,41,37,31,29,23,19,17,13,11,7,5,3,2]:
			if (num % x) == 0:
				num = num / x
				primes.append(x)
	
		return primes

	def ranking(self, *players):
		ranks = []
		ps = []
		for p in players:
			ranks.append(self.toPrimes(p.getRank()))

		ranks.sort(reverse=True)
		for r in ranks:
			val = 1
			for x in r:
				val *= x
			for p in players:
				if val == p.getRank() and not p in ps:
					ps.append(p)

		return ps

