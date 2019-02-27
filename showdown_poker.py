import copy
import distutils.core
from time import time
from random import randint,shuffle
from math import floor

#Individual Cards
class Card:
	def __init__ (self,value,suit):
		self.value = value
		self.suit = suit
		self.vname = ''
		self.sname = ''

	def valname(self, value):
		if self.value == 2:
			self.vname = 'Two'
		elif self.value == 3:
			self.vname = 'Three'
		elif self.value == 4:
			self.vname = 'Four'
		elif self.value == 5:
			self.vname = 'Five'
		elif self.value == 6:
			self.vname = 'Six'
		elif self.value == 7:
			self.vname = 'Seven'
		elif self.value == 8:
			self.vname = 'Eight'
		elif self.value == 9:
			self.vname = 'Nine'
		elif self.value == 10:
			self.vname = 'Ten'
		elif self.value == 11:
			self.vname = 'Jack'
		elif self.value == 12:
			self.vname = 'Queen'
		elif self.value == 13:
			self.vname = 'King'
		elif self.value == 14:
			self.vname = 'Ace'

	def suitname(self, suit):
		if self.suit == "Hearts":
			self.sname = '♥'
		elif self.suit == "Spades":
			self.sname = '♠'
		elif self.suit == "Clubs":
			self.sname = '♣'
		elif self.suit == "Diamonds":
			self.sname = '♦'

	def cardname(self):
		return f'{self.sname}{self.vname}{self.sname}'

#All Decks
class Deck:
	def __init__(self):
		self.cards = []
		self.create()

	def create(self):
		for _ in range(decks):
			for val in (2,3,4,5,6,7,8,9,10,11,12,13,14):
				for suit in ("Hearts", "Spades", "Clubs", "Diamonds"):
					self.cards.append(Card(val,suit))
		shuffle(self.cards)

	def draw(self):
		c1 = self.cards.pop()
		c2 = self.cards.pop()
		c3 = self.cards.pop()
		c4 = self.cards.pop()
		c5 = self.cards.pop()
		return (c1,c2,c3,c4,c5)

#Misc Functions
def ss():
	if show_strength: print(f'[{round(strength/10000,6)}]')
	else: print()

def hnumber(max,msg):
	while True:
		try:
			hn = int(input(msg))
			if hn <= max and hn>0:
				return hn
			else:
				print(f'Please enter an integer between 1 and {max}.')
		except ValueError:
			print('Please enter a positive integer.')

def decks(msg):
	while True:
		try:
			d = int(input(msg))
			if d > 0:
				return d
			else:
				print('Please enter a positive integer.')
		except ValueError:
			print('Please enter a positive integer.')

def sstrength(msg):
	while True:
		try:
			ss = distutils.util.strtobool(input(msg))
			if ss == 0 or ss == 1:
				return ss
			else:
				print('Please indicate whether you\'d like to show advanced stats')
		except ValueError:
			print('Please indicate whether you\'d like to show advanced stats')

#Evaluation Functions
def evalname(x):
	if x == 2:
		return 'Two'
	elif x == 3:
		return 'Three'
	elif x == 4:
		return 'Four'
	elif x == 5:
		return 'Five'
	elif x == 6:
		return 'Six'
	elif x == 7:
		return 'Seven'
	elif x == 8:
		return 'Eight'
	elif x == 9:
		return 'Nine'
	elif x == 10:
		return 'Ten'
	elif x == 11:
		return 'Jack'
	elif x == 12:
		return 'Queen'
	elif x == 13:
		return 'King'
	elif x == 14:
		return 'Ace'

def hcard(hand):
	global strength
	strength = 1000 + 10*vsort[0] + vsort[1] + .1*vsort[2] + .01*vsort[3] + .001*vsort[4]
	return f'High-Card {evalname(vsort[0])}'

def numpair(hand):
	global strength
	pairs = list(dict.fromkeys([val for val in values if values.count(val) == 2]))
	if len(pairs) < 1:
		return False
	if len(pairs) == 1:
		vp = vsort.copy()
		for _ in range(2):
			vp.remove(pairs[0])
		strength = 2000 + 10*pairs[0] + vp[0] + .1*vp[1] + .01*vp[2];
		return f'Pair of {evalname(pairs[0])}s'
	if len(pairs) == 2:
		vps = vsort.copy()
		for _ in range(2):
			vps.remove(pairs[0]); vps.remove(pairs[1])
		if pairs[0]>pairs[1]:
			strength = (3000 + 10*int(pairs[0]) + int(pairs[1])) + .1*vps[0]
			return f'{evalname(pairs[0])}s and {evalname(pairs[1])}s'
		else:
			strength = (3000 + 10*int(pairs[1]) + int(pairs[0])) + .1*vps[0]
			return f'{evalname(pairs[1])}s and {evalname(pairs[0])}s'


def detset(hand):
	global strength
	detsets = [val for val in values if values.count(val) == 3]
	if len(detsets) < 1:
		return False
	else:
		vs = vsort.copy()
		for _ in range(3):
			vs.remove(detsets[0])
		strength = 4000 + 10*detsets[0] + vs[0] + .1*vs[1]
		return f'Set of {evalname(detsets[0])}s'

def straight(hand):
	global strength
	if (max(vset) - min(vset) == 4) and numpair(hand) == False and detset(hand) == False and quads(hand) == False:
		strength = 5000 + 10*min(vset)
		straight = f'Straight from {evalname(min(vset))} to {evalname(max(vset))}'
	elif vset == {14,2,3,4,5}:
		strength = 5000
		straight = 'Straight from Ace to Five'
	else:
		straight = False
	return straight

def flush(hand):
	global strength
	flushes = [suit for suit in suits if suits.count(suit) == 5]
	if len(flushes) < 5:
		flush = False
	else:
		values.sort(reverse=True)
		strength = 6000 + 10*values[0] + values[1] + .1*values[2] + .01*values[3] + .001*values[4]
		flush = f'{evalname(max(values))}-High flush of {flushes[0]}'
	return flush

def fullhouse(hand):
	global strength
	pairs = [val for val in values if values.count(val) == 2]
	detsets = [val for val in values if values.count(val) == 3]
	if detset(hand) != False and numpair(hand) != False:
		strength = 7000 + 10*detsets[0] + pairs[0]
		fh = f'{evalname(detsets[0])}s full of {evalname(pairs[0])}s'
	else:
		fh = False
	return fh

def quads(hand):
	global strength
	quads = [val for val in values if values.count(val) == 4]
	if len(quads) < 1:
		return False
	else:
		vq = vsort.copy()
		for _ in range(4):
			vq.remove(quads[0])
		strength = 8000 + 10*quads[0] + vq[0]
		return f'Quad {evalname(quads[0])}s'

def straightflush(hand):
	global strength
	if (max(vset) - min(vset) == 4) and numpair(hand) == False and detset(hand) == False and quads(hand) == False and vset != {14,13,12,11,10}:
		straight = "True"
	elif vset == {14,2,3,4,5}:
		straight = 'Wheel'
	elif vset == {14,13,12,11,10}:
		straight = "Royal"
	else:
		straight = 'False'

	flushes = [suit for suit in suits if suits.count(suit) == 5]
	if len(flushes) < 1:
		flush = False
	else:
		flush = True

	if straight == "True" and flush == True:
		strength = 9000 + 10*min(vset)
		sf = f'{evalname(max(values))}-High Straight Flush of {flushes[0]}'
	elif straight == "Wheel" and flush == True:
		strength = 9000
		sf = f'Five-High Straight Flush of {flushes[0]}'
	elif straight == "Royal" and flush == True:
		strength = 10000
		sf = f'Royal Flush of {flushes[0]}'
	else:
		sf = False
	return sf

#Count Hand Occurence
hand_occurence = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
ho_names = ['High Card: ','Pair: ','Two-Pair: ','Three of a Kind: ','Straight: ','Flush: ','Full House: ','Four of a Kind: ','Straight Flush: ','Royal Flush: ']

decks = decks('How many decks are there? ')
deck = Deck()

hnumber = hnumber(floor((decks*52)/5), f'How many players are there (max {floor((decks*52)/5)})? ')
show_strength = sstrength("Would you like to show advanced stats? ")
h_inc = 0; h_strength = {}; start_time = time()

while h_inc < hnumber:
	print(f"\nPlayer {h_inc + 1}'s hand:")
	c1,c2,c3,c4,c5 = deck.draw(); hand = c1,c2,c3,c4,c5
	values = [hand[0].value,hand[1].value,hand[2].value,hand[3].value,hand[4].value]; vset = {hand[0].value,hand[1].value,hand[2].value,hand[3].value,hand[4].value}; vsort = sorted(values,reverse=True)
	suits = [hand[0].suit,hand[1].suit,hand[2].suit,hand[3].suit,hand[4].suit]
	c1.valname(c1.value); c2.valname(c2.value); c3.valname(c3.value); c4.valname(c4.value); c5.valname(c5.value)
	c1.suitname(c1.suit); c2.suitname(c2.suit); c3.suitname(c3.suit); c4.suitname(c4.suit); c5.suitname(c5.suit)
	print(f'| {c1.cardname()} | {c2.cardname()} | {c3.cardname()} | {c4.cardname()} | {c5.cardname()} |')

	hcard(hand); numpair(hand); detset(hand); straight(hand); flush(hand); fullhouse(hand); quads(hand); straightflush(hand)
	if strength < 2000:
		print(hcard(hand),end=" "); ss()
		hand_occurence[0]+=1
	elif strength < 3000:
		print(numpair(hand),end=" "); ss()
		hand_occurence[1]+=1
	elif strength < 4000:
		print(numpair(hand),end=" "); ss()
		hand_occurence[2]+=1
	elif strength < 5000:
		print(detset(hand),end=" "); ss()
		hand_occurence[3]+=1
	elif strength < 6000:
		print(straight(hand),end=" "); ss()
		hand_occurence[4]+=1
	elif strength < 7000:
		print(flush(hand),end=" "); ss()
		hand_occurence[5]+=1
	elif strength < 8000:
		print(fullhouse(hand),end=" "); ss()
		hand_occurence[6]+=1
	elif strength < 9000:
		print(quads(hand),end=" "); ss()
		hand_occurence[7]+=1
	elif strength < 10000:
		print(straightflush(hand),end=" "); ss()
		hand_occurence[8]+=1
	elif strength == 10000:
		print(straightflush(hand),end=" "); ss()
		hand_occurence[9]+=1

	h_strength[h_inc] = strength

	h_inc += 1

hss = sorted(h_strength.items(), key=lambda k: k[1], reverse=True)
print(f'\n\n\nPlayer {hss[0][0]+1} has the strongest hand! [{round(hss[0][1]/10000,6)}]\nPlayer {hss[hnumber-1][0] + 1} has the weakest hand :( [{round(hss[hnumber-1][1]/10000,6)}]') if show_strength else print(f'\n\n\nPlayer {hss[0][0] + 1} has the strongest hand!\nPlayer {hss[hnumber-1][0]+1} has the weakest hand :(')
if show_strength:

	print('\n\n\n\n\nHand Occurence:\n')
	for x in range(10):
		print(ho_names[x],hand_occurence[x],f'({int(round(100*hand_occurence[x]/len(hss),0))}%)')

	print('\n\n\n\n\nFull Player Ranking:\n')
	for x in range(len(hss)):
		print(f'{x+1}.',f'Player {hss[x][0]+1}',f'[{round(hss[x][1]/10000,6)}]')

	print('\n\n\nExecution Time:', "%ss" % (int(round(time()-start_time,2))))

