import socket
import json

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 55555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_ADDRESS, SERVER_PORT))

def get_user_move():
    valid = False
    while not valid:
        user_input = input("Enter your move (row col): ")
        try:
            row, col = map(int, user_input.split())
            if 0 <= row <= 2 and 0 <= col <= 2:
                valid = True
            else:
                print("Invalid move. Row and column must be 0, 1, or 2.")
        except ValueError:
            print("Invalid input. Please enter the row and column numbers separated by a space.")
    return row, col

try:
    while True:
        data = sock.recv(1024).decode()
        if data == "Your move":
            print("Your turn.")
            row, col = get_user_move()
            move = {'row': row, 'col': col}
            sock.sendall(json.dumps(move).encode())
        elif data.startswith("Connected as Player"):
            print(data)  # Print the connection message
        else:
            try:
                game_state = json.loads(data)
                print("Current board:")
                for row in game_state:
                    print(' | '.join(row))
                print()
            except json.JSONDecodeError:
                print(data)  # Any other message from the server
except Exception as e:
    print(f"Error: {e}")
finally:
    print('Closing socket')
    sock.close()
