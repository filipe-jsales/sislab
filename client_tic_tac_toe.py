#! /usr/bin/python3

import socket
from sys import argv
import tic_tac_toe_client_game as tttcg
class TTTClient:
	"""TTTClient deals with networking and communication with the TTTServer."""

	def __init__(self):
		"""Initializes the client and create a client socket."""
		# Create a TCP/IP socket
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, address, port_number):
		"""Keeps repeating connecting to the server and returns True if 
		connected successfully."""
		while True:
			try:
				print("Connecting to the game server...")
				# Connection time out 10 seconds
				self.client_socket.settimeout(10)
				# Connect to the specified host and port 
				self.client_socket.connect((address, int(port_number)))
				# Return True if connected successfully
				return True
			except:
				# Caught an error
				print("There is an error when trying to connect to " + 
					str(address) + "::" + str(port_number))
				self.__connect_failed__()
		return False

	def __connect_failed__(self):
		"""(Private) This function will be called when the attempt to connect
		failed. This function might be overridden by the GUI program."""
		# Ask the user what to do with the error
		choice = input("[A]bort, [C]hange address and port, or [R]etry?")
		if(choice.lower() == "a"):
			exit()
		elif(choice.lower() == "c"):
			address = input("Please enter the address:")
			port_number = input("Please enter the port:")

	def s_send(self, command_type, msg):
		"""Sends a message to the server with an agreed command type token 
		to ensure the message is delivered safely."""
		# A 1 byte command_type character is put at the front of the message
		# as a communication convention
		try:
			self.client_socket.send((command_type + msg).encode())
		except:
			# If any error occurred, the connection might be lost
			self.__connection_lost()

	def s_recv(self, size, expected_type):
		"""Receives a packet with specified size from the server and check 
		its integrity by comparing its command type token with the expected
		one."""
		try:
			msg = self.client_socket.recv(size).decode()
			# If received a quit signal from the server
			if(msg[0] == "Q"):
				why_quit = ""
				try:
					# Try receiving the whole reason why quit
					why_quit = self.client_socket.recv(1024).decode()
				except:
					pass
				# Print the resaon
				print(msg[1:] + why_quit)
				# Throw an error
				raise Exception
			# If received an echo signal from the server
			elif(msg[0] == "E"):
				# Echo the message back to the server
				self.s_send("e", msg[1:])
				# Recursively retrive the desired message
				return self.s_recv(size, expected_type)
			# If the command type token is not the expected type
			elif(msg[0] != expected_type):
				print("The received command type \"" + msg[0] + "\" does not " + 
					"match the expected type \"" + expected_type + "\".")
				# Connection lost
				self.__connection_lost()
			# If received an integer from the server
			elif(msg[0] == "I"):
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

	def __connection_lost(self):
		"""(Private) This function will be called when the connection is lost."""
		print("Error: connection lost.")
		try:
			# Try and send a message back to the server to notify connection lost
			self.client_socket.send("q".encode())
		except:
			pass
		# Raise an error to finish 
		raise Exception

	def close(self):	
		"""Shut down the socket and close it"""
		# Shut down the socket to prevent further sends/receives
		self.client_socket.shutdown(socket.SHUT_RDWR)
		# Close the socket
		self.client_socket.close()

# Define the main program
def main():
	# If there are more than 3 arguments 
	if(len(argv) >= 3):
		# Set the address to argument 1, and port number to argument 2
		address = argv[1]
		port_number = argv[2]
	else:
		# Ask the user to input the address and port number
		address = input("Please enter the address:")
		port_number = input("Please enter the port:")

	# Initialize the client object
	client = tttcg.TTTClientGame()
	# Connect to the server
	client.connect(address, port_number)
	try:
		# Start the game
		client.start_game()
	except:
		print(("Game finished unexpectedly!"))
	finally:
		# Close the client
		client.close()

if __name__ == "__main__":
	# If this script is running as a standalone program,
	# start the main program.
	main()