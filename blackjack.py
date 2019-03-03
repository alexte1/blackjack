import random
import numpy

####################################################################################################
#Development Log:
#	3/3/19
#	potential problems to fix: in results, i am only taking care of a 2 way draw for now.
#	Need to fix results.
#	Tie is not working, and also need to account for 2+ way tie
#	and an emply sum (means player bust)
#		- could just delete that player from the results calculation
#			-need to make sure they are not deleted when restarting
####################################################################################################


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
	#bust list to stop asking when to hit.
	bustList = []


	def __init__(self, playersList):
		for x in range(len(self.rank)):
			for y in range(len(self.suits)):
				self.deck.append((self.rank[x],self.suits[y]))

		for i in range(len(playersList)):
			self.bustList.append(False)

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

		for i in range(len(playersList)):
			flag = True
			for j in self.gameBoard:
				while flag and self.bustList[i] == False:
					print playersList[i]
					hitorStay = raw_input("Do you want to hit? y/n: ")
					if hitorStay == "y":
						self.hit(playersList, playersList.index(playersList[i]))
						flag = True
					else:
						flag = False

	def sumCards(self, playersList):

		aceList = []
		self.sumList = []

		for i in range(len(self.gameBoard)):
			tmpSum = 0
			aceCard = False
			playerSum = []
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
				if tmpSum <= 21:
					playerSum.append(tmpSum)
				tmpSum += 10
				if tmpSum <= 21:
					playerSum.append(tmpSum)
			else:
				if tmpSum <= 21:
					playerSum.append(tmpSum)

			self.sumList.append(playerSum)


		#what is displayed to the terminal for players to see.
		for i in range(len(playersList)):
			print "------------------"
			if 21 in self.sumList[i]:
				print playersList[i]
				print self.gameBoard[i]
				print "Blackjack!!!"
			elif len(self.sumList[i]) == 0:
				print self.gameBoard[i]
				print "Bust!!!"
				self.bustList[i] = True
			else:
				print playersList[i]
				print self.gameBoard[i]
				print self.sumList[i]
		print "------------------"
			
	def results(self, playersList):
		#want to sort it so removing the smallest sum is best
		for i in range(len(self.sumList)):
			self.sumList[i].sort()
			if len(self.sumList[i]) == 1:
				continue
			elif len(self.sumList[i]) != 0:
				tmp = self.sumList[i][-1]
				self.sumList[i] = []
				self.sumList[i].append(tmp)

		highest = -1
		winnerIndex = -1
		draw = False
		firstDraw = -1
		secondDraw = -1

		for i in range(len(self.sumList)):
			#need sumList[i][0] because we are checking a list, and need to check
			#its number in the list, hence the [0]
			#save the winner index so we can just say winner is at
			#playerList[winnerIndex] or something like that
			if self.sumList[i][0] > highest:
				highest = self.sumList[i][0]
				winnerIndex = i
				draw = False
			elif self.sumList[i][0] == highest:
				#could be a problem if there are more than 2 draws...
				draw = True
				firstDraw = winnerIndex
				secondDraw = i
				print "asd"

		if draw == False:
			print "Tie between: ", playersList[firstDraw], playersList[secondDraw] 
		else:
			print "Winner is: ", playersList[winnerIndex]


def main():

	playersList = []
	playFlag = True
	names = "aaa"
	while names != "done":
		names = raw_input("Enter the name of the players (exit: done)- ")
		if names != "done":
			playersList.append(names)

	while playFlag:
		gameobj = game(playersList)
		gameobj.shuffleDeck()
		# gameobj.displayDeck()
		gameobj.gameLogic(playersList, len(playersList))
		gameobj.gameProgression(playersList)
		gameobj.results(playersList)
		var = raw_input("Another round? (y/n) - ")
		if var == "y" or var == "yes":
			playFlag = True
		else:
			playFlag = False





main()