#!/usr/bin/python3

# File 	:	

import os

def createBoard(boardStatus=None):
	#Default board content. Board is empty by default.
	boardContent = {	'A1': ' ', 'A2': ' ', 'A3': ' ',\
						'B1': ' ', 'B2': ' ', 'B3': ' ',\
						'C1': ' ', 'C2': ' ', 'C3': ' '}
	# If board contents are provided.
	if boardStatus!= None:
		boardContent = boardStatus

	leftPadding = 20 # Number of white spaces to insert in each row for padding the board from left.
	
	boardRow_1 = ' '*leftPadding + '    1   2   3'
	boardRow_2 = ' '*leftPadding + 'A   {A1} | {A2} | {A3}'.format(	A1 = boardContent['A1'],\
																	A2 = boardContent['A2'],\
																	A3 = boardContent['A3'])

	boardRow_3 = ' '*leftPadding + 'B   {B1} | {B2} | {B3}'.format(	B1 = boardContent['B1'],\
																	B2 = boardContent['B2'],\
																	B3 = boardContent['B3'])
	
	boardRow_4 = ' '*leftPadding + 'C   {C1} | {C2} | {C3}'.format(	C1 = boardContent['C1'],\
																	C2 = boardContent['C2'],\
																	C3 = boardContent['C3'])
	hLine = ' '*leftPadding + '   '+'---+'*2 + '---'

	newLine = '\n'

	# Put it all together.
	board = boardRow_1 + newLine + newLine + \
			boardRow_2 + newLine + hLine + newLine + \
			boardRow_3 + newLine + hLine + newLine + \
			boardRow_4
	# Put blank lines above & below the board then,
	# Return created board. 
	return '\n' + board + '\n'


def getUserData():	# Returns a tuple (markOne, markTwo, firstToPlay)
	markOne = 'x'	# Default markOne (Marking of user 1)
	markTwo = 'o'	# Default markTwo (Marking of user 2)
	print()
	markOne = input('User 1 Mark symbol: ')
	markTwo = input('User 2 Mark symbol: ')
	while(len(markOne)>1 or len(markTwo) > 1):
		print('Too long markers. Try again.')
		markOne = input('User 1 Mark symbol: ')
		markTwo = input('User 2 Mark symbol: ')

	firstToPlay = input('Who will play first ({} or {}): '.format(markOne,markTwo))
	while(not (firstToPlay==markTwo or firstToPlay == markOne)):
		firstToPlay = input('Who will play first ({} or {}): '.format(markOne,markTwo))
	return (markOne, markTwo,firstToPlay)

# Build a list of cells available in the board content.
def getAvailableCells(boardContent):
	# availableCells will hold a list of available cells in the board contents.
	availableCells = []
	for key in boardContent.keys():
		if boardContent[key]==' ':
			availableCells.append(key)
	return availableCells

# The following 'getOccupiedCells' method/function is redundant and not really important.
def getOccupiedCells(boardContent):
	occupiedCells = []
	for key in boardContent.keys():
		if boardContent[key]!=' ':
			occupiedCells.append(key)
	return occupiedCells

# Get user input. and store in the board content variable.
def getUserInput(boardContent,userData):

	availableCells = getAvailableCells(boardContent)
	if len(availableCells)>0:
		if boardContent['nextUser']==userData[0]:
			# It's 1st user's turn.
			cell = input('User 1({}) Enter cell id: '.format(userData[0])).upper()
			while (cell not in availableCells):
				cell = input('Enter a valid cell id: ').upper()
			boardContent[cell]=userData[0]
			# got 1st user's input. Set next to play 2nd user.
			boardContent['nextUser']=userData[1] # 2nd user will play next i.e. 1st index

		else: #boardContent['nextUser']==userData[1]:
			######################################################################################	
			#####	Future Development : In future 2nd user will be a Bot and not a human. 	######
			######################################################################################
			# It's 2nd user's turn.
			cell = input('User 2({}) Enter cell id: '.format(userData[1])).upper()
			while (cell not in availableCells):
				cell = input('Enter a valid cell id: ').upper()
			boardContent[cell]=userData[1]
			# God 2nd user's input. Set next to play 1st user.
			boardContent['nextUser']=userData[0] # 1st user will play next i.e. 0th index.
		printBoard(boardContent)
	return boardContent

# Win condition. Check once table has minimum 5 cells.
# Should return winners mark(x or o). return None otherwise.
def getWinner(boardContent,userData):
'''
		Let's say userData is ('x', 'o', 'x') i.e. (User1 mark = 'x', user2 mark = 'o', firstToplay = 'x')

				1   2   3

			A   o | x |  
			   ---+---+---
			B     | o |   
			   ---+---+---
			C   x | x | o

			In this case The diagonal line(list) will be ['o','o','o']
			And that the count of userData[1] i.e. 'o' is 3 then the function
			will return the index associated with that user mark - 1 in this case - in the user data tuple.
			For this particular case winLines will have value as following:

							row-1			row-2		 row-3			 col-1			col-2			col-3		Diagonal 		rDiagonal
			winLines = [['o','x',' '], [' ','o',' '], ['x','x','o'], ['o',' ','x'], ['x','o','x'], [' ',' ','o'], ['o','o','o'], [' ','o','x']]
'''
	if len(getAvailableCells(boardContent))<5:	
		row1 = [boardContent['A1'], boardContent['A2'],	boardContent['A3']]
		row2 = [boardContent['B1'], boardContent['B2'], boardContent['B3']]
		row3 = [boardContent['C1'], boardContent['C2'], boardContent['C3']]
		col1 = [boardContent['A1'], boardContent['B1'], boardContent['C1']]
		col2 = [boardContent['A2'], boardContent['B2'], boardContent['C2']]
		col3 = [boardContent['A3'], boardContent['B3'], boardContent['C3']]
		diagonal 	= [boardContent['A1'], boardContent['B2'], boardContent['C3']]
		rDiagonal 	= [boardContent['A3'], boardContent['B2'], boardContent['C1']]

		winLines = [row1, row2, row3, col1, col2, col3, diagonal, rDiagonal]
		for line in winLines:
			if line.count(userData[0]) == 3:
				return 0
			elif line.count(userData[1]) == 3:
				return 1
		else:
			return None
	else:
		return None

	## def anybodyWon(boardContent,userData):
	## 	# userData = (markOne, markTwo, firstToPlay)
	## 	#cellIds = ('A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3')
# D	## 	winConditions = [	'A1A2A3', 'A3A2A1',\
# E	## 						'B1B2B3', 'B3B2B1',\
# P	## 						'C1C2C3', 'C3C2C1',\
# R	## 						'A1B1C1', 'C1B1A1',\
# I	## 						'A2B2C2', 'C2B2A2',\
# C	## 						'A3B3C3', 'C3B3A3',\
# A	## 						'A1B2C3', 'C3B2A1',\
# T	## 						'A3B2C1', 'C1B2A3']
# E	## 	if len(getAvailableCells(boardContent))<5: # It means there are at least 5 cells occupied.
# D	## 		for item in winConditions:
	## 			itemCells = [item[:2],item[2:4],item[4:]]
# F	## 			userOne = ''
# U	##			userTwo = ''
# N	## 			for c in itemCells:
# C	##				if boardContent[c]==userData[0]:
# T	##					userOne += userData[0]
# I	## 				elif boardContent[c]==userData[1]:
# O	##					userTwo += userData[1]
# N	##				else:
	## 					continue
	##			if userOne == userData[0]*3:
	##				return 0 # Return that user one has won.
	##			elif userTwo == userData[1]*3:
	##				return 1 # Return that user two has won.
	##			else:
	##				continue
	##	else: # There couldn't possibly a winner yet with only 4 cells filled.
	##		return None


def printBoard(boardStatus):
	_=os.system('clear')
	print(createBoard(boardStatus))

if __name__=='__main__':


	# Get user input.
	choice = 'yes'
	while(choice in ['yes','y']):
		# Clear screen.
		_ = os.system('clear')

		userData = getUserData()

		# Initialize empty board first places.
		boardContent = {	'A1': ' ', 'A2': ' ', 'A3': ' ',\
							'B1': ' ', 'B2': ' ', 'B3': ' ',\
							'C1': ' ', 'C2': ' ', 'C3': ' ',\
							'nextUser': userData[-1]}

		printBoard(boardContent)

		while len(getAvailableCells(boardContent)):
			boardContent = getUserInput(boardContent,userData)
			winner = getWinner(boardContent,userData)
			if winner == 0 or winner == 1:
				print('\n{:-^100}'.format(' Congratulations!'))
				print('{:-^100}\n'.format(' User \'{}\' won. '.format(userData[winner])))
				break
			else:
				continue
		else:
			print('\n Oops...Better luck next time!!!')

		choice = input('Do you wish to play more(y/n): ')
		if choice.lower() in ['yes','y']:
			continue
		else:
			break