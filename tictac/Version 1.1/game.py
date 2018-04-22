#!/usr/bin/python3

#	File 			:	game.py
#	Dependencies	:	welcome.txt, instructions.txt, board.txt
#	Author			:	Mayur B.
# 	Date Created 	:	June 24, 2017

"""
ALERT: Make sure python3 is installed before running the game.

INTRODUCTION
A simple text based Tic-Tac-Toe game for two users sitting at the same computer. Both users can play simultaneously.
Game Intrustcions are stored in a file 'innstructions.txt' and it is placed in the same directory as this file.
There is an optional file 'preferences.txt' for user preference data storage.
One more file is created during the game 'board.txt' in the same directory as this file.
Enjoy the Game!

BOARD:
					1   2   3

		Row1	A     |   |   
				   ---+---+---
		Row2	B     |   |   
				   ---+---+---
		Row3	C     |   |   
"""

import os

# Global Variables

# Current markers on board. ' '=No Marker
bRow1 = [' ', ' ', ' ']		# Row 1 cells data 
bRow2 = [' ', ' ', ' ']		# Row 2 cells data
bRow3 = [' ', ' ', ' ']		# Row 3 cells data
coordinates = ('A1','A2','A3','B1','B2','B3','C1','C2','C3')
cellData = [bRow1, bRow2, bRow3] # Board cells data. A list of lists.
nextTurn = ''

def resetGlobalData():
	for j in range(3): 
		bRow3[j] = ' '
		bRow2[j] = ' '
		bRow1[j] = ' '
	cellData[0] = bRow1
	cellData[1] = bRow2
	cellData[2] = bRow3

# Clear screen. Runs differently on different OS's.
def clearScreen():
	# For Linux OS's
	os.system('clear')

# Print welcome message on standard output.
def welcomeUser():
	"""
	Introduces user with the welcome message. And author's introduction.
	"""
	# Clear terminal screen.
	clearScreen()
	# Open file 'welcome.txt' and print the welcome message on screen.
	message = open('welcome.txt','r')
	for line in message:
		print(line,end=' ')
	else:
		_=input('\n\n< Press Enter to continue. >')
	# Close file and return.
	message.close()
	return
	
# Print games instructions stored in file 'instructions.txt'
def instructions():
	"""
	Print game instructions on standard output.
	"""
	# Clear terminal screen.
	clearScreen()
	# Open file 'instructions.txt' in read mode and print it's content(instructions) on std output.
	instructions = open('instructions.txt','r')
	for line in instructions:
		print(line, end=' ')
	else:
		_=input('\n\n< Press Enter to continue. >')
	#Close file and return.
	instructions.close()
	return

# A function which is not supposed to be called explicitely.
# It is called from other functions, such as displayBoard() etc.
def paintBoard(cellData = cellData):
	"""
	INPUT: Marker positions to put markers on board.
	OUTPUT: Returns a string representation of board.
	ARGS: cellData > markers data.
	"""
	# Board Representation in form of multiple lists.
	newLine		= '\n'
	leftPadding	= '\t'*4
	hHeader 	= leftPadding + '    1   2   3 '						# Board horizontal header representations.
	rowOne  	= leftPadding + 'A   {} | {} | {} '.format(bRow1[0], bRow1[1], bRow1[2]) # Row 1 representation.
	rowTwo  	= leftPadding + 'B   {} | {} | {} '.format(bRow2[0], bRow2[1], bRow2[2]) # Row 2 representation.
	rowThree	= leftPadding + 'C   {} | {} | {} '.format(bRow3[0], bRow3[1], bRow3[2]) # Row 3 representation.
	hSeparator	= leftPadding + '   ---+---+---'
	boardRepr 	= 	hHeader + newLine + newLine + \
					rowOne + newLine + \
					hSeparator + newLine + \
					rowTwo + newLine + \
					hSeparator + newLine + \
					rowThree
	# Return board painting.
	return boardRepr

# Displays the board given marker positions.
def displayBoard(markerData=cellData,clrscr=True):
	"""
	Given the marker data, paints the board and displays it.
	Args: 	<makerData> Marker data to put on board.
			<clrscr> Whether or not to clear the screen before displaying board.
	"""
	#Clear screen before displaying the board.
	if clrscr:
		clearScreen()
	# Paint the board with current marker positions.
	board = paintBoard(markerData) # Cell data is a global variable.
	# Wrap a blank line above and below board representation for better visual.
	board = '\n' + board + '\n'
	# Now display the board without any hesitation.
	print(board)
	return 

# Asks user for marker symbols. and other questions.
def getUserData():
	"""
	Asks user for marker symbols and returns a tuple consisting of all the data.
	returns: tuple([<user1_marker>, <user2_marker>, <opening_user's_marker>])
	"""
	displayBoard()

	# Store User 1's maker in 'markerOne' variable.
	markerOne = input('\n\tUser One marker: ').lower()
	while(len(markerOne)>1):	# make sure marker is single character and not a long string.
		markerOne = input('\tTry again (Enter short marker): ').lower()

	# Store user 2's marker in 'markerTwo' variable.
	markerTwo = input('\n\tUser Two marker: ').lower()
	while(len(markerTwo)>1):
		markerTwo = input('\tTry again (Enter short marker): ').lower()

	# Now ask who will play first. 'markerOne' or 'markerTwo'.
	opener = input('\n\tWho will play first({} or {}): '.format(markerOne,markerTwo)).lower()
	while(not(opener == markerOne or opener == markerTwo)):
		opener = input('\tTry again({} or {}): '.format(markerOne,markerTwo))

	# Set opener as the next user to play.
	nextTurn = opener
	
	# Encapsulate all data in tuple and return it.
	return tuple([markerOne,markerTwo,opener])

# Switches first move maker from one user to another.
def switchOpener(data):
	"""
	Function changes userData's last element -from one mark to another- which represents the user who will make first move.
	"""
	if(data[-1] == data[0]):
		return (data[0], data[1], data[1])
	else:
		return (data[0],data[1],data[0])



# Whoever has the next turn, function will ask for marker coordinates accordingly.
def playTurn(nextTurn,userData):
	"""
	Asks the user where to place marker out of 9 coordinates.
	Return a tuple(<marker>,<marker_coordinate>)
	"""
	if nextTurn == userData[0]:
		loc = input('\tWhere to place ({}): '.format(userData[0])).upper()
		while loc not in coordinates:
			loc = input('\tInvalid: Try again({}): '.format(userData[0])).upper()
		while not placeMarker(userData[0],loc): # Place marker at user given location - 'loc'
			loc = input('\tInvalid coordinate: Try again({}): '.format(userData[0])).upper()
		nextTurn = userData[1]
	else:
		loc = input('\tWhere to place ({}): '.format(userData[1])).upper()
		while loc not in coordinates:
			loc = input('\tInvalid: Try again({}): '.format(userData[1])).upper()
		nextTurn = userData[0]
		while not placeMarker(userData[1],loc):
			loc = input('\tInvalid coordinate: Try again({}): '.format(userData[1])).upper()
		nextTurn = userData[0]
	displayBoard()
	return nextTurn


def placeMarker(marker,location):
	"""
	INPUT: marker symbol and board coordinate to place the marker.
	OUTPUT: True if marker was placed at given location. False otherwise.
	Places marker at a specified location <location> into board data <cellData>.
	"""
	# Obtain the index of marker from global 'coordinates' tuple using location.
	i = coordinates.index(location)
	rowIndex = i//3			# Finding cellData[r][c] 1st index(r in this case)
	colIndex = i%3			# Finding cellData[r][c] 2nd index(c in this case)
	if cellData[rowIndex][colIndex] == ' ':
		cellData[rowIndex][colIndex] = marker
		return True
	else:
		return False


def winner(userData):
	"""
	INPUT: Board cell data as a global variable. Both user's marker symbols in form of tuple.
	OUTPUT: Return winning marker symbol(such as 'x' or 'o') if any, False otherwise.
	"""
	# Create straigh lines in which markers can appear.
	r1 = ''.join(bRow1)										# First row line string
	r2 = ''.join(bRow2)										# Second row line string
	r3 = ''.join(bRow3)										# Third row line string
	c1 = ''.join([mark[0] for mark in cellData])			# First column line string
	c2 = ''.join([mark[1] for mark in cellData])			# Second column line string
	c3 = ''.join([mark[2] for mark in cellData])			# Third column line string
	fd = ''.join([cellData[i][i] for i in range(3)])		# Forward diagonal line string
	rd = ''.join([cellData[::-1][i][i] for i in range(3)])	# Reverse diagonal line string
	stream = [r1,r2,r3,c1,c2,c3,fd,rd]				# List of all line's strings.
	if userData[0]*3 in stream:	# if 'x'*3 i.e. 'xxx' appear in any line string. Here 'x' is assumed to be 1st user mark.
		return userData[0]
	elif userData[1]*3 in stream: # if 'x'*3 i.e. 'ooo' appear in any line string. Here 'o' is assumed to be 2nd user mark.		
		return userData[1]
	else: # if 'xxx' or 'ooo' appears nowhere, then nobody has won yet.
		return False

def boardFull():
	"""
	INPUT: Uses global board representing variable.
	OUTPUT: True if board is full. False if board is NOT full.
	"""
	stream = ''.join([''.join(i) for i in cellData])
	emptyCells = lambda s: s.count(' ')
	if emptyCells(stream):	# If there are empty cells, board is not full.
		return False
	else:
		return True

def congratulate(marker):
	"""
	Prints a message congratualing winner indicated by marker <marker>.
	"""
	print('\n\n\t\tCONGRATULATIONS USER "{}", YOU HAVE WON!!!'.format(marker.upper()))

def tiedMessage():
	"""
	Prints a message that match tied.
	"""
	print('\n\t\tOops...MATCH TIED......Better luck next time.\n')
	return

def playMore():
	"""
	Return True or False depending on user's wish whether to play more or not.
	"""
	choice = input('\nDo you wish to play again(y/n): ').lower()
	if choice.startswith('y'):
		return True
	else:
		return False

def playTicTacToe(userData):
	"""
	Play one iteration of game and Return None.
	"""
	resetGlobalData()
	nextTurn = userData[-1]
	displayBoard()
	turns = 0
	while(not boardFull()):
		nextTurn = playTurn(nextTurn,userData) # Nextturn user plays and then changes nextTurn to next user marker.
		turns += 1
		if turns >4: # There must be atleast 5 total turns for somebody to win.
			if winner(userData):
				congratulate(winner(userData))
				break
		else:
			continue
	return

def debug():
	_ = input('DEBUG:')

def playGame():
	"""
	This is the first function to run when game starts.
	INPUT: It takes no arguments as it's input.
	OUTPUT: Nothing. Just perform some tasks of Playing Single or Multiple iterations of game by
	running function such as playTicTacToe()
	"""
	welcomeUser()
	instructions()
	userData = getUserData()	# <Tuple> sets user markers and first to play.
	playTicTacToe(userData)
	replay = playMore()
	while(replay):
		newUserData = switchOpener(userData)
		playTicTacToe(newUserData)
		replay = playMore()
	else:
		clearScreen()
		print('\n\n\n\t\t THANK YOU FOR PLAYING \'TIC-TAC-TOE\'')
		print('\t\t Hope you liked the Game.\n')
		_ = input('\t\t<Press Enter to exit.>')
		return

if __name__=='__main__':
	playGame()