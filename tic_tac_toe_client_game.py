import client_tic_tac_toe as cttt
class TTTClientGame(cttt.TTTClient):
	"""TTTClientGame deals with the game logic on the client side."""

	def __init__(self):
		"""Initializes the client game object."""
		cttt.TTTClient.__init__(self)

	def start_game(self):
		"""Starts the game and gets basic game information from the server."""
		# Receive the player's ID from the server
		self.player_id = int(self.s_recv(128, "A"))
		# Confirm the ID has been received
		self.s_send("c","1")

		# Tell the user that connection has been established
		self.__connected__()

		# Receive the assigned role from the server
		self.role = str(self.s_recv(2, "R"))
		# Confirm the assigned role has been received
		self.s_send("c","2")

		# Receive the mactched player's ID from the server
		self.match_id = int(self.s_recv(128, "I"))
		# Confirm the mactched player's ID has been received
		self.s_send("c","3")

		print(("You are now matched with player " + str(self.match_id) 
			+ "\nYou are the \"" + self.role + "\""))

		# Call the __game_started() function, which might be implemented by
		# the GUI program to interact with the user interface.
		self.__game_started__()

		# Start the main loop
		self.__main_loop()

	def __connected__(self):
		"""(Private) This function is called when the client is successfully
		connected to the server. This might be overridden by the GUI program."""
		# Welcome the user
		print("Welcome to Tic Tac Toe online, player " + str(self.player_id) 
			+ "\nPlease wait for another player to join the game...")

	def __game_started__(self):
		"""(Private) This function is called when the game is getting started."""
		# This is a virtual function
		# The actual implementation is in the subclass (the GUI program)
		return

	def __main_loop(self):
		"""The main game loop."""
		while True:
			# Get the board content from the server
			board_content = self.s_recv(10, "B")
			# Get the command from the server 
			command = self.s_recv(2, "C")
			# Update the board
			self.__update_board__(command, board_content)

			if(command == "Y"):
				# If it's this player's turn to move
				self.__player_move__(board_content)
			elif(command == "N"):
				# If the player needs to just wait
				self.__player_wait__()
				# Get the move the other player made from the server 
				move = self.s_recv(2, "I")
				self.__opponent_move_made__(move)
			elif(command == "D"):
				# If the result is a draw
				print("It's a draw.")
				break
			elif(command == "W"):
				# If this player wins
				print("You WIN!")
				# Draw winning path
				self.__draw_winning_path__(self.s_recv(4, "P"))
				# Break the loop and finish
				break
			elif(command == "L"):
				# If this player loses
				print("You lose.")
				# Draw winning path
				self.__draw_winning_path__(self.s_recv(4, "P"))
				# Break the loop and finish
				break
			else:
				# If the server sends back anything unrecognizable
				# Simply print it
				print("Error: unknown message was sent from the server")
				# And finish
				break

	def __update_board__(self, command, board_string):
		"""(Private) Updates the board. This function might be overridden by
		the GUI program."""
		if(command == "Y"):
			# If it's this player's turn to move, print out the current 
			# board with " " converted to the corresponding position number
			print("Current board:\n" + TTTClientGame.format_board(
				TTTClientGame.show_board_pos(board_string)))
		else:
			# Print out the current board
			print("Current board:\n" + TTTClientGame.format_board(
				board_string))

	def __player_move__(self, board_string):
		"""(Private) Lets the user input the move and sends it back to the
		server. This function might be overridden by the GUI program."""
		while True:
			# Prompt the user to enter a position
			try:
				position = int(input('Please enter the position (1~9):'))
			except:
				print("Invalid input.")
				continue

			# Ensure user-input data is valid
			if(position >= 1 and position <= 9):
				# If the position is between 1 and 9
				if(board_string[position - 1] != " "):
					# If the position is already been taken,
					# Print out a warning
					print("That position has already been taken." + 
						"Please choose another one.")
				else:
					# If the user input is valid, break the loop
					break
			else:
				print("Please enter a value between 1 and 9 that" + 
					"corresponds to the position on the grid board.")
			# Loop until the user enters a valid value

		# Send the position back to the server
		self.s_send("i", str(position))

	def __player_wait__(self):
		"""(Private) Lets the user know it's waiting for the other player to
		make a move. This function might be overridden by the GUI program."""
		print("Waiting for the other player to make a move...")

	def __opponent_move_made__(self, move):
		"""(Private) Shows the user the move that the other player has taken. 
		This function might be overridden by the GUI program."""
		print("Your opponent took up number " + str(move))

	def __draw_winning_path__(self, winning_path):
		"""(Private) Shows to the user the path that has caused the game to 
		win or lose. This function might be overridden by the GUI program."""
		# Generate a new human readable path string
		readable_path = ""
		for c in winning_path:
			readable_path += str(int(c) + 1) + ", "

		print("The path is: " + readable_path[:-2])


	def show_board_pos(s):
		"""(Static) Converts the empty positions " " (a space) in the board 
		string to its corresponding position index number."""

		new_s = list("123456789")
		for i in range(0, 8):
			if(s[i] != " "):
				new_s[i] = s[i]
		return "".join(new_s)

	def format_board(s):
		"""(Static) Formats the grid board."""

		# If the length of the string is not 9
		if(len(s) != 9):
			# Then print out an error message
			print("Error: there should be 9 symbols.")
			# Throw an error 
			raise Exception

		# Draw the grid board
		#print("|1|2|3|")
		#print("|4|5|6|")
		#print("|7|8|9|")
		return("|" + s[0] + "|" + s[1]  + "|" + s[2] + "|\n" 
			+ "|" + s[3] + "|" + s[4]  + "|" + s[5] + "|\n" 
			+ "|" + s[6] + "|" + s[7]  + "|" + s[8] + "|\n")