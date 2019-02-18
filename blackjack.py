import random
import numpy
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


	def __init__(self):
		for x in range(len(self.rank)):
			for y in range(len(self.suits)):
				self.deck.append((self.rank[x],self.suits[y]))

	def randomizeDeck(self):

		seed = random.randint(0,1000)
		for i in range(seed):
			random.shuffle(self.deck)

	def displayDeck(self):
		for i in self.deck:
			print i

	def gameLogic(self, playersList, numPlayers):

		iterator = 0
		tmp = []
		# cards = []

		for i in playersList:
			# print i + "'s hand:"
			for j in range(2):
				tmp.append(self.deck[iterator])
				iterator += 1
			self.gameBoard.append(tmp)
			tmp = []

		for i in range(len(self.gameBoard)):
			firstAce = False
			secondAce = False
			firstCard = self.gameBoard[i][0][0]
			secondCard = self.gameBoard[i][1][0]


			if not isinstance(firstCard, int):
				if firstCard == "A":
					firstAce = True
				else:
					firstCard = 10
			elif not isinstance(secondCard, int):
				if secondCard == "A":
					secondAce = True
				else:
					secondCard = 10

			if firstAce or secondAce:
				if firstAce and secondAce:
					print playersList[i] + "\'s hand\n", self.gameBoard[i], "\nhand value: ", 11 + 1, "or", 1 + 1
				if firstAce and not secondAce:
					print playersList[i] + "\'s hand\n", self.gameBoard[i], "\nhand value: ", 11 + secondCard, "or", 1 + secondCard
				else:
					print playersList[i] + "\'s hand\n", self.gameBoard[i], "\nhand value: ", firstCard + 11, "or", firstCard + 1
			else:
					print playersList[i] + "\'s hand\n", self.gameBoard[i], "\nhand value: ", firstCard + secondCard, "\n"



			

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
		gameobj.randomizeDeck()
		# gameobj.displayDeck()
		gameobj.gameLogic(playersList, len(playersList))
		# gameobj.gameProgression(playersList)

		var = raw_input("Another round? (y/n) - ")
		if var == "y" or var == "yes":
			playFlag = True
		else:
			playFlag = False





main()