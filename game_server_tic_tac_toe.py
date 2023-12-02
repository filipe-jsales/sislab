
import logging
import threading
import server_tic_tac_toe as sttt
import time
import player_tic_tac_toe as pttt
import game_tic_tac_toe as gttt
class TTTServerGame(sttt.TTTServer):
	"""TTTServerGame deals with the game logic on the server side."""

	def __init__(self):
		"""Initializes the server game object."""
		sttt.TTTServer.__init__(self)

	def start(self):
		"""Starts the server and let it accept clients."""
		# Create an array object to store connected players
		self.waiting_players = []
		# Use a simple lock to synchronize access when matching players
		self.lock_matching = threading.Lock()
		# Start the main loop
		self.__main_loop()

	def __main_loop(self):
		"""(Private) The main loop."""
		# Loop to infinitely accept new clients
		while True:
			# Accept a connection from a client
			connection, client_address = self.server_socket.accept()
			logging.info("Received connection from " + str(client_address))

			# Initialize a new Player object to store all the client's infomation
			new_player = pttt.Player(connection)
			# Push this new player object into the players array
			self.waiting_players.append(new_player)

			try:
				# Start a new thread to deal with this client
				threading.Thread(target=self.__client_thread, 
					args=(new_player,)).start()
			except:
				logging.error("Failed to create thread.")

	def __client_thread(self, player):
		"""(Private) This is the client thread."""
		# Wrap the whole client thread with a try and catch so that the 
		# server would not be affected even if a client messes up
		try:
			# Send the player's ID back to the client
			player.send("A", str(player.id))
			# Send the client didn't confirm the message
			if(player.recv(2, "c") != "1"):
				# An error happened
				logging.warning("Client " + str(player.id) + 
					" didn't confirm the initial message.")
				# Finish 
				return

			while player.is_waiting:
				# If the player is still waiting for another player to join
				# Try to match this player with other waiting players
				match_result = self.matching_player(player)

				if(match_result is None):
					# If not matched, wait for a second (to keep CPU usage low) 
					time.sleep(1)
					# Check if the player is still connected
					player.check_connection()
				else:
					# If matched with another player

					# Initialize a new Game object to store the game's infomation
					new_game = gttt.Game()
					# Assign both players
					new_game.player1 = player
					new_game.player2 = match_result
					# Create an empty string for empty board content
					new_game.board_content = list("         ")

					try:
						# Game starts
						new_game.start()
					except:
						logging.warning("Game between " + str(new_game.player1.id) + 
							" and " + str(new_game.player2.id) + 
							" is finished unexpectedly.")
					# End this thread
					return
		except:
			print("Player " + str(player.id) + " disconnected.")
		finally:
			# Remove the player from the waiting list
			self.waiting_players.remove(player)

	def matching_player(self, player):
		"""Goes through the players list and try to match the player with 
		another player who is also waiting to play. Returns any matched 
		player if found."""
		# Try acquiring the lock
		self.lock_matching.acquire()
		try:
			# Loop through each player
			for p in self.waiting_players:
				# If another player is found waiting and its not the player itself
				if(p.is_waiting and p is not player):
					# Matched player with p
					# Set their match
					player.match = p
					p.match = player
					# Set their roles
					player.role = "X"
					p.role = "O"
					# Set the player is not waiting any more
					player.is_waiting = False
					p.is_waiting = False
					# Then return the player's ID
					return p
		finally:
			# Release the lock
			self.lock_matching.release()
		# Return None if nothing is found
		return None
