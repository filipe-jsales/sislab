import socket
import json
import threading

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 55555
game_state = [[' ' for _ in range(3)] for _ in range(3)]
player_events = [threading.Event(), threading.Event()]

# Initialize the server socket and listen for two connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen(2)
print("Server started. Waiting for two connections...")

def print_board(board):
    for row in board:
        print("|" + "|".join(row) + "|")
    print()

def handle_client(connection, player):
    while True:
        player_events[player].wait()  # Wait for this player's turn
        player_events[player].clear()  # Clear the event for the next round

        # Notify the client it's their turn
        connection.sendall("Your move".encode())
        data = connection.recv(1024).decode()
        move = json.loads(data)
        row, col = move['row'], move['col']
        symbol = 'X' if player == 0 else 'O'
        game_state[row][col] = symbol
        print(f"Player {symbol} made a move: {move}")
        print_board(game_state)

        # Send the updated game state to both players
        for conn in connections:
            conn.sendall(json.dumps(game_state).encode())

        # Allow the other player to make a move
        player_events[1 - player].set()

connections = []
for i in range(2):
    conn, _ = server_socket.accept()
    connections.append(conn)
    threading.Thread(target=handle_client, args=(conn, i), daemon=True).start()
    if i == 0:
        conn.sendall("Connected as Player X. Please wait for Player O...".encode())
    else:
        conn.sendall("Connected as Player O. Player X will make the first move.".encode())
        player_events[0].set()  # Allow Player X to make the first move

print("Both players connected. Game starts.")
