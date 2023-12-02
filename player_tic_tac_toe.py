import logging
class Player:
	"""Player class describes a client with connection to the server and
	as a player in the tic tac toe game."""

	# Count the players (for generating unique IDs)
	count = 0

	def __init__(self, connection):
		"""Initialize a player with its connection to the server"""
		# Generate a unique id for this player
		Player.count = Player.count + 1
		self.id = Player.count
		# Assign the corresponding connection 
		self.connection = connection
		# Set the player waiting status to True
		self.is_waiting = True	

	def send(self, command_type, msg):
		"""Sends a message to the client with an agreed command type token 
		to ensure the message is delivered safely."""
		# A 1 byte command_type character is put at the front of the message
		# as a communication convention
		try:
			self.connection.send((command_type + msg).encode())
		except:
			# If any error occurred, the connection might be lost
			self.__connection_lost()

	def recv(self, size, expected_type):
		"""Receives a packet with specified size from the client and check 
		its integrity by comparing its command type token with the expected
		one."""
		try:
			msg = self.connection.recv(size).decode()
			# If received a quit signal from the client
			if(msg[0] == "q"):
				# Print why the quit signal
				logging.info(msg[1:])
				# Connection lost
				self.__connection_lost()
			# If the message is not the expected type
			elif(msg[0] != expected_type):
				# Connection lost
				self.__connection_lost()
			# If received an integer from the client
			elif(msg[0] == "i"):
				# Return the integer
				return int(msg[1:])
			# In other case
			else:
				# Return the message
				return msg[1:]
			# Simply return the raw message if anything unexpected happended 
			# because it shouldn't matter any more
			return msg
		except:
			# If any error occurred, the connection might be lost
			self.__connection_lost()
		return None

	def check_connection(self):
		"""Sends a meesage to check if the client is still properly connected."""
		# Send the client an echo signal to ask it to repeat back
		self.send("E", "z")
		# Check if "e" gets sent back
		if(self.recv(2, "e") != "z"):
			# If the client didn't confirm, the connection might be lost
			self.__connection_lost()

	def send_match_info(self):
		"""Sends a the matched information to the client, which includes
		the assigned role and the matched player."""
		# Send to client the assigned role
		self.send("R", self.role)
		# Waiting for client to confirm
		if(self.recv(2,"c") != "2"):
			self.__connection_lost()
		# Sent to client the matched player's ID
		self.send("I", str(self.match.id))
		# Waiting for client to confirm
		if(self.recv(2,"c") != "3"):
			self.__connection_lost()

	def __connection_lost(self):
		"""(Private) This function will be called when the connection is lost."""
		# This player has lost connection with the server
		logging.warning("Player " + str(self.id) + " connection lost.")
		# Tell the other player that the game is finished
		try:
			self.match.send("Q", "The other player has lost connection" + 
				" with the server.\nGame over.")
		except:
			pass
		# Raise an error so that the client thread can finish
		raise Exception
