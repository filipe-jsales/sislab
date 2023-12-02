#! /usr/bin/python3
import socket
# import threading
# import time
from sys import argv
import logging


import player_tic_tac_toe as pttt
import game_tic_tac_toe as gttt
import game_server_tic_tac_toe as gsttt

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
		server = gsttt.TTTServerGame()
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

