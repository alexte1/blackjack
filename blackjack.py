import random
import numpy

####################################################################################################
#Development Log:
#	3/3/19
#	potential problems to fix: in results, i am only taking care of a 2 way draw for now.
#	Need to fix results.
#	Tie is not working, and also need to account for 2+ way tie
#	and an empty sum (means player bust)
#		- could just delete that player from the results calculation
#			-need to make sure they are not deleted when restarting
#
#
#
#	3/4/19
#	Ran into a bug when a player has 2 aces.
#	Might be fixed when we set aceFlag = Flase in sumCards
#
#	As of 9:23 pm. I think i fixed 2+ way tie and the sum with >= 2 aces
#	As of 9:38... NEED TO FIX multiple aces still. 
#
#
#	3/5/19
#	If everyone busts, there is a bug.
#	Still havent fixed the multple aces
####################################################################################################


index_card_dealt = 0;

class game:
	
	#2 3 4 5 . . . K A
	rank = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
	# rank = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
	#H, D, C, S
	suits = ["Hearts", "Diamonds", "Clover", "Spades"]
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
					hitorStay = raw_input("\n\nDo you want to hit? y/n: ")
					print "\n\n"
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
			aceCounter = 0
			for j in range(len(self.gameBoard[i])):

				currCard = self.gameBoard[i][j][0];

				if currCard == "J" or currCard == "Q" or currCard == "K":
					tmpSum += 10
				elif currCard == "A":
					# aceCard = True
					aceCounter += 1
				else:
					tmpSum += currCard

			if aceCounter > 0:
				while aceCounter > 0:
					# aceCard = False
					tmpSum += 1
					if tmpSum <= 21:
						playerSum.append(tmpSum)

					tmpSum += 10
					if tmpSum <= 21:
						playerSum.append(tmpSum)

					aceCounter -= 1
			else:
				if tmpSum <= 21:
					playerSum.append(tmpSum)

			self.sumList.append(playerSum)


		#what is displayed to the terminal for players to see.
		for i in range(len(playersList)):
			print "--------------------------------------"
			if 21 in self.sumList[i]:
				print self.sumList[i]
				if len(self.sumList[i]) == 2:
					print playersList[i]
					print self.gameBoard[i]
					print "Blackjack!!!"
				else:
					print playersList[i]
					print self.gameBoard[i]
					print "21!!!"
			elif len(self.sumList[i]) == 0:
				print playersList[i]
				print self.gameBoard[i]
				print "Bust!!!"
				self.bustList[i] = True
			else:
				print playersList[i]
				print self.gameBoard[i]
				print self.sumList[i]
		print "--------------------------------------"
			
	def results(self, playersList):

		#want to sort it so removing the smallest sum is best
		for i in range(len(self.sumList)):
			if len(self.sumList[i]) == 1:
				continue
			elif len(self.sumList[i]) != 0:
				self.sumList[i].sort()
				tmp = self.sumList[i][-1]
				self.sumList[i] = []
				self.sumList[i].append(tmp)

		highest = -1
		winnerIndex = -1
		draw = False
		firstDraw = -1
		secondDraw = -1

		for i in range(len(self.sumList)):
			if len(self.sumList[i]) == 0:
				continue
			#need sumList[i][0] because we are checking a list, and need to check
			#its number in the list, hence the [0]
			#save the winner index so we can just say winner is at
			#playerList[winnerIndex] or something like that
			if self.sumList[i][0] > highest:
				# print "Highest Changed. New highest is: ", self.sumList[i][0], "by", playersList[i] 
				highest = self.sumList[i][0]
				winnerIndex = i
				draw = False
			elif self.sumList[i][0] == highest:
				# print "Draw Detected."
				# print "Previous Highest = ", highest, "Which is", playersList[winnerIndex], "'s card"
				# print "Now there is a tie with", playersList[i], "'s card"
				#could be a problem if there are more than 2 draws...
				draw = True
				firstDraw = winnerIndex
				secondDraw = i
				# print "asd"

		if draw == True:
			# print "Tie between: ", playersList[firstDraw], playersList[secondDraw]
			print "Tie between: "
			#done so we can iterate through and print out whoever has the same highest
			for i in range(len(self.sumList)):
				if len(self.sumList[i]) == 0:
					continue
				if self.sumList[i][0] == highest:
					print playersList[i]
		elif False in self.bustList:
			# print self.bustList
			print "Winner is: ", playersList[winnerIndex]
		else:
			# print "Winner is: ", playersList[winnerIndex]
			print "No one won."


		#need to reset bust List for next round
		self.bustList = []


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