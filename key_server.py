import paramiko
import threading
import json
import socket

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# This dictionary will store the public keys for each client
client_public_keys = {}

# Function to generate a new key pair
def generate_keys():
    private_key = paramiko.RSAKey.generate(2048)
    public_key = private_key.get_base64().encode()
    public_key = private_key.get_base64()

    return private_key, public_key

# Handle client connections
def handle_client_connection(client_socket, client_address):
    print(f"New connection from {client_address}")
    
    # Generate a new key pair for the client
    private_key, public_key = generate_keys()
    
    client_socket.send(public_key.encode())
    print(f'Sending public key: {public_key}')
    
    # Receive a client ID from the client
    client_id = client_socket.recv(1024).decode()
    
    # Store the public key with the associated client ID
    client_public_keys[client_id] = public_key
    
    # Wait for a request for a public key of another client
    target_client_id = client_socket.recv(1024).decode()
    
    # Send the requested public key to the client
    if target_client_id in client_public_keys:
        client_socket.send(client_public_keys[target_client_id].encode())
        client_socket.send(client_public_keys[target_client_id])
    else:
        client_socket.send(b"Client not found.")

    # Close the connection
    client_socket.close()

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

try:
    while True:
        # Wait for a client to connect
        client_sock, client_addr = server_socket.accept()
        
        # Create a new thread to handle the client connection
        client_thread = threading.Thread(
            target=handle_client_connection,
            args=(client_sock, client_addr)
        )
        client_thread.start()
except KeyboardInterrupt:
    print("Server is shutting down.")
finally:
    server_socket.close()
