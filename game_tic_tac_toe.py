import logging
class Game:
	"""Game class describes a game with two different players."""

	def start(self):
		"""Starts the game."""
		# Send both players the match info
		self.player1.send_match_info()
		self.player2.send_match_info()

		# Print the match info onto screen 
		logging.info("Player " + str(self.player1.id) + 
			" is matched with player " + str(self.player2.id))

		while True:
			# Player 1 move
			if(self.move(self.player1, self.player2)):
				return
			# Player 2 move
			if(self.move(self.player2, self.player1)):
				return

	def move(self, moving_player, waiting_player):
		"""Lets a player make a move."""
		# Send both players the current board content
		moving_player.send("B", ("".join(self.board_content)))
		waiting_player.send("B", ("".join(self.board_content)))
		# Let the moving player move, Y stands for yes it's turn to move, 
		# and N stands for no and waiting
		moving_player.send("C", "Y")
		waiting_player.send("C", "N")
		# Receive the move from the moving player
		move = int(moving_player.recv(2, "i"))
		# Send the move to the waiting player
		waiting_player.send("I", str(move))
		# Check if the position is empty
		if(self.board_content[move - 1] == " "):
			# Write the it into the board
		 	self.board_content[move - 1] = moving_player.role
		else:
			logging.warning("Player " + str(moving_player.id) + 
				" is attempting to take a position that's already " + 
				"been taken.")
		# 	# This player is attempting to take a position that's already
		# 	# taken. HE IS CHEATING, KILL HIM!
		# 	moving_player.send("Q", "Please don't cheat!\n" + 
		# 		"You are running a modified client program.")
		# 	waiting_player.send("Q", "The other playing is caught" + 
		# 		"cheating. You win!")
		# 	# Throw an error to finish this game
		# 	raise Exception

		# Check if this will result in a win
		result, winning_path = self.check_winner(moving_player)
		if(result >= 0):
			# If there is a result
			# Send back the latest board content
			moving_player.send("B", ("".join(self.board_content)))
			waiting_player.send("B", ("".join(self.board_content)))

			if(result == 0):
				# If this game ends with a draw
				# Send the players the result
				moving_player.send("C", "D")
				waiting_player.send("C", "D")
				print("Game between player " + str(self.player1.id) + " and player " 
					+ str(self.player2.id) + " ends with a draw.")
				return True
			if(result == 1):
				# If this player wins the game
				# Send the players the result
				moving_player.send("C", "W")
				waiting_player.send("C", "L")
				# Send the players the winning path
				moving_player.send("P", winning_path)
				waiting_player.send("P", winning_path)
				print("Player " + str(self.player1.id) + " beats player " 
					+ str(self.player2.id) + " and finishes the game.")
				return True
			return False

	def check_winner(self, player):
		"""Checks if the player wins the game. Returns 1 if wins, 
		0 if it's a draw, -1 if there's no result yet."""
		s = self.board_content

		# Check columns
		if(len(set([s[0], s[1], s[2], player.role])) == 1):
			return 1, "012"
		if(len(set([s[3], s[4], s[5], player.role])) == 1):
			return 1, "345"
		if(len(set([s[6], s[7], s[8], player.role])) == 1):
			return 1, "678"

		# Check rows
		if(len(set([s[0], s[3], s[6], player.role])) == 1):
			return 1, "036"
		if(len(set([s[1], s[4], s[7], player.role])) == 1):
			return 1, "147"
		if(len(set([s[2], s[5], s[8], player.role])) == 1):
			return 1, "258"

		# Check diagonal
		if(len(set([s[0], s[4], s[8], player.role])) == 1):
			return 1, "048"
		if(len(set([s[2], s[4], s[6], player.role])) == 1):
			return 1, "246"

		# If there's no empty position left, draw
		if " " not in s:
			return 0, ""

		# The result cannot be determined yet
		return -1, ""
