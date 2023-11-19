
import paramiko

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Client configuration
CLIENT_ID = 'client1'
TARGET_CLIENT_ID = 'client2'

# Connect to the server
client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect(SERVER_HOST, port=SERVER_PORT)

# Send the client ID to the server
stdin, stdout, stderr = client.exec_command(f'echo {CLIENT_ID}')
client_id = stdout.read().decode().strip()

# Send the target client ID to the server
stdin, stdout, stderr = client.exec_command(f'echo {TARGET_CLIENT_ID}')
target_client_id = stdout.read().decode().strip()

# Request the public key of the target client from the server
stdin, stdout, stderr = client.exec_command(f'echo {target_client_id}')
public_key = stdout.read().decode().strip()

# Close the SSH connection
client.close()

# Print the received public key
print(f"Received public key: {public_key}")
