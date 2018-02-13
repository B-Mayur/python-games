#!/usr/bin/python3

import oldMaidGame
import sys
try:
	users = sys.argv[1:]
	game = oldMaidGame.OldMaidGame()
	game.play(users)
except:
	print("TRY: ./play.py user1 user2 ...")