import random
import numpy

'''
Development Log:
	3/3/19
	potential problems to fix: in results, i am only taking care of a 2 way draw for now.
	Need to fix results.
	Tie is not working, and also need to account for 2+ way tie
	and an empty sum (means player bust)
		- could just delete that player from the results calculation
			-need to make sure they are not deleted when restarting



	3/4/19
	Ran into a bug when a player has 2 aces.
	Might be fixed when we set aceFlag = Flase in sumCards

	As of 9:23 pm. I think i fixed 2+ way tie and the sum with >= 2 aces
	As of 9:38... NEED TO FIX multiple aces still. 


	3/5/19
	If everyone busts, there is a bug.	[FIXED] 3/9/19
	Still havent fixed the multple aces

	3/9/19
	So far, first one to 21 wins.
 	
	Todo next:
		- Fix multiple aces
		- Assign a person to be dealer
			- If players list is: [Alex, Kris, Andrew], then
			  Alex is dealer in round 1. Then Kris, then Andrew
			- Make it so that one of the current dealer's card
			  can't be seen until it is their turn.
				- So if Alex is dealer, let Kris get asked first
				  wheter or not to hit or stay.
'''

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

		#need to reset bust List for each round
		self.bustList = []
		for i in range(len(playersList)):
			self.bustList.append(False)

	def gameNumber(self, gameNumber):
		print "\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		print "\t\tGame Number:", gameNumber
		print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"

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
		tmp = []

		for i in playersList:
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

		self.sumCards(playersList)

	def gameProgression(self, playersList):
		for i in range(len(playersList)):
			flag = True
			for j in self.gameBoard:
				# print self.sumList
				while flag and self.bustList[i] == False and [21] not in self.sumList:
					print "\n*************************\n" + playersList[i] + ", do you want to hit?"
					hitorStay = raw_input("y/n: ")
					if hitorStay == "y":
						print "\n" + playersList[i] + " chose to hit!"
						self.hit(playersList, playersList.index(playersList[i]))
						flag = True
					else:
						print "\n" + playersList[i] + " chose to stay!"
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
					tmpSum += 1
					playerSum.append(tmpSum)
					tmpSum += 10
					playerSum.append(tmpSum)
				else:
					tmpSum += currCard

			if aceCounter > 0:
				while aceCounter > 0:
					addOne = tmpSum + 1
					addEleven = tmpSum + 11
					if addOne == 21 or addEleven == 21:
						tmpSum = 21
						playerSum.append(tmpSum)
					else:
						if addOne <= 21:
							playerSum.append(addOne)
						if addEleven <= 21:
							playerSum.append(addEleven)
					aceCounter -= 1
			else:
				if tmpSum <= 21:
					playerSum.append(tmpSum)

			self.sumList.append(playerSum)


		#what is displayed to the terminal for players to see.
		for i in range(len(playersList)):
			print "\n" + playersList[i] + "'s hand:"
			if 21 in self.sumList[i]:
				# print self.sumList[i]
				if len(self.sumList[i]) == 2:
					# print playersList[i]
					print self.gameBoard[i]
					print "Blackjack!!!"
				else:
					# print playersList[i]
					print self.gameBoard[i]
					print "21!!!"
			elif len(self.sumList[i]) == 0:
				# print playersList[i]
				print self.gameBoard[i]
				print "Bust!!!"
				self.bustList[i] = True
			else:
				# print playersList[i]
				print self.gameBoard[i]
				print "Hand value:", self.sumList[i]
			
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
				draw = True
				firstDraw = winnerIndex
				secondDraw = i

		if draw == True:
			print "Tie between: "
			for i in range(len(self.sumList)):
				if len(self.sumList[i]) == 0:
					continue
				if self.sumList[i][0] == highest:
					print playersList[i]
		elif False in self.bustList:
			print "Winner is: " + playersList[winnerIndex] + " with: ", highest
		else:
			print "No one won."

def main():

	gameNumber = 1
	dealerIndex = 0
	playersList = []
	playFlag = True
	names = "aaa"
	while names != "done":
		names = raw_input("Enter the name of the players (exit: done)- ")
		if names != "done":
			playersList.append(names)

	while playFlag:
		gameobj = game(playersList)
		gameobj.gameNumber(gameNumber)
		gameobj.shuffleDeck()
		gameobj.gameLogic(playersList, len(playersList))
		gameobj.gameProgression(playersList)
		gameobj.results(playersList)

		var = raw_input("Another round? (y/n) - ")
		if var == "y":
			playFlag = True
			gameNumber += 1
		else:
			if var == "n":
				playFlag = False
			else:
				print "Unknow input. Exiting game."

main()
