from abc import ABC, abstractmethod
import socket
import logging

class IServer(ABC):
    """Interface for a server."""

    @abstractmethod
    def bind(self, port_number):
        """Binds the server to a specified port number."""
        pass

    @abstractmethod
    def close(self):
        """Closes the server's connection."""
        pass

class TTTServer(IServer):
    """TTTServer deals with networking and communication with the TTTClient."""

    def __init__(self):
        """Initializes the server object with a server socket."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self, port_number):
        """Binds the server with the designated port and start listening to
        the binded address."""
        while True:
            try:
                self.server_socket.bind(("", int(port_number)))
                logging.info("Reserved port " + str(port_number))
                self.server_socket.listen(1)
                logging.info("Listening to port " + str(port_number))
                break
            except:
                logging.warning("There is an error when trying to bind " + str(port_number))
                choice = input("[A]bort, [C]hange port, or [R]etry?")
                if(choice.lower() == "a"):
                    exit()
                elif(choice.lower() == "c"):
                    port_number = input("Please enter the port:")

    def close(self):
        """Closes the server socket."""
        self.server_socket.close()
