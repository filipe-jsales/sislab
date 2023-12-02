#! /usr/bin/python3
import socket
import threading
import time
from sys import argv
import logging


import player_tic_tac_toe as pttt
import game_tic_tac_toe as gttt

# Set up logging to file  
logging.basicConfig(level=logging.DEBUG,
	format='[%(asctime)s] %(levelname)s: %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
	filename='ttt_server.log')
# Define a Handler which writes INFO messages or higher to the sys.stderr
# This will print all the INFO messages or higer at the same time
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# Add the handler to the root logger
logging.getLogger('').addHandler(console)

class TTTServer:
	"""TTTServer deals with networking and communication with the TTTClient."""

	def __init__(self):
		"""Initializes the server object with a server socket."""
		# Create a TCP/IP socket
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def bind(self, port_number):
		"""Binds the server with the designated port and start listening to
		the binded address."""
		while True:
			try:
				# Bind to an address with the designated port
				# The empty string "" is a symbolic name 
				# meaning all available interfaces
				self.server_socket.bind(("", int(port_number)))
				logging.info("Reserved port " + str(port_number))
				# Start listening to the binded address
				self.server_socket.listen(1)
				logging.info("Listening to port " + str(port_number))
				# Break the while loop if no error is caught
				break
			except:
				# Caught an error
				logging.warning("There is an error when trying to bind " + 
					str(port_number))
				# Ask the user what to do with the error
				choice = input("[A]bort, [C]hange port, or [R]etry?")
				if(choice.lower() == "a"):
					exit()
				elif(choice.lower() == "c"):
					port_number = input("Please enter the port:")

	def close(self):
		# Close the socket
		self.server_socket.close()

class TTTServerGame(TTTServer):
	"""TTTServerGame deals with the game logic on the server side."""

	def __init__(self):
		"""Initializes the server game object."""
		TTTServer.__init__(self)

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

# Define the main program
def main():
	# If there are more than 2 arguments 
	if(len(argv) >= 2):
		# Set port number to argument 1
		port_number = argv[1]
	else:
		# Ask the user to input port number
		port_number = input("Please enter the port:")

	try:
		# Initialize the server object
		server = TTTServerGame()
		# Bind the server with the port 
		server.bind(port_number)
		# Start the server
		server.start()
		# Close the server
		server.close()
	except BaseException as e:
		logging.critical("Server critical failure.\n" + str(e))

if __name__ == "__main__":
	# If this script is running as a standalone program,
	# start the main program.
	main()

