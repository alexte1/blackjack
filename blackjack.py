import random
import numpy

index_card_dealt = 0;

class game:
	
	#2 3 4 5 . . . K A
	rank = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
	# rank = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
	#H, D, C, S
	suits = ["H", "D", "C", "S"]
	#combination of suits and rank
	deck = []
	#game board (dealer is at the end of the list)
	gameBoard = []
	#1-1 with gameBoard, now this just stores the number
	sumList = []


	def __init__(self):
		for x in range(len(self.rank)):
			for y in range(len(self.suits)):
				self.deck.append((self.rank[x],self.suits[y]))

	def shuffleDeck(self):
		self.gameBoard = []
		seed = random.randint(0,1000)
		for i in range(seed):
			random.shuffle(self.deck)

	def displayDeck(self):
		for i in self.deck:
			print i

	def gameLogic(self, playersList, numPlayers):
		global index_card_dealt
		# iterator = 0
		tmp = []
		# cards = []

		for i in playersList:
			# print i + "'s hand:"
			for j in range(2):
				tmp.append(self.deck[index_card_dealt])
				index_card_dealt += 1
			self.gameBoard.append(tmp)
			tmp = []

		self.sumCards(playersList)

		#index is used to know where to append the card to.
	def hit(self, playersList, index):
		global index_card_dealt
		tmp = []

		self.gameBoard[index].append(self.deck[index_card_dealt])
		index_card_dealt += 1
		# for i in playersList:
		# 	for j in range(1):
		# 		tmp.append(self.deck[index_card_dealt])
		# 		index_card_dealt += 1
		# 	self.gameBoard[index].append(tmp)
		# 	tmp = []

		self.sumCards(playersList)

	def gameProgression(self, playersList):

		for i in playersList:
			print i
			flag = True
			for j in self.gameBoard:
				print "Do you want to hit?"
				while flag:
					hitorStay = raw_input("y/n: ")
					if hitorStay == "y":
						self.hit(playersList, playersList.index(i))
						flag = True
					else:
						flag = False

		# for i,j in zip(playersList, self.gameBoard):
		# 	print i, j

	def sumCards(self, playersList):

		aceList = []
		self.sumList = []

		for i in range(len(self.gameBoard)):
			tmpSum = 0
			aceCard = False
			for j in range(len(self.gameBoard[i])):

				currCard = self.gameBoard[i][j][0];

				if currCard == "J" or currCard == "Q" or currCard == "K":
					tmpSum += 10
				elif currCard == "A":
					aceCard = True
				else:
					tmpSum += currCard

			if aceCard:
				tmpSum += 1
				self.sumList.append(tmpSum)
				tmpSum += 10
				self.sumList.append(tmpSum)
			else:
				self.sumList.append(tmpSum)

		for i,j in zip(self.gameBoard, self.sumList):
			print i, j



		# for i in range(len(self.gameBoard)):
		# 	print self.gameBoard[i]

		# for i in range(len(self.gameBoard)):
		# 	firstAce = False
		# 	secondAce = False
		# 	firstCard = self.gameBoard[i][0][0]
		# 	secondCard = self.gameBoard[i][1][0]


		# 	if not isinstance(firstCard, int):
		# 		if firstCard == "A":
		# 			firstAce = True
		# 		else:
		# 			firstCard = 10
		# 	elif not isinstance(secondCard, int):
		# 		if secondCard == "A":
		# 			secondAce = True
		# 		else:
		# 			secondCard = 10

		# 	if firstAce or secondAce:
		# 		if firstAce and secondAce:
		# 			print playersList[i] + "\'s hand\n", self.gameBoard[i], "\nhand value: ", 11 + 1, "or", 1 + 1
		# 		if firstAce and not secondAce:
		# 			print playersList[i] + "\'s hand\n", self.gameBoard[i], "\nhand value: ", 11 + secondCard, "or", 1 + secondCard
		# 		else:
		# 			print playersList[i] + "\'s hand\n", self.gameBoard[i], "\nhand value: ", firstCard + 11, "or", firstCard + 1
		# 	else:
		# 			print playersList[i] + "\'s hand\n", self.gameBoard[i], "\nhand value: ", firstCard + secondCard, "\n"

			

def main():

	playersList = []
	playFlag = True
	names = "aaa"
	while names != "done":
		names = raw_input("Enter the name of the players (exit: done)- ")
		if names != "done":
			playersList.append(names)

	while playFlag:
		gameobj = game()
		gameobj.shuffleDeck()
		# gameobj.displayDeck()
		gameobj.gameLogic(playersList, len(playersList))
		# print index_card_dealt
		# gameobj.gameProgression(playersList)

		var = raw_input("Another round? (y/n) - ")
		if var == "y" or var == "yes":
			playFlag = True
		else:
			playFlag = False





main()