import socket
import json
import os

# Define global variables
DATABASE_FILE = 'authentication.json'
database = {}


def load_database():
    global database
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            database = json.load(f)

def authenticate(username, password):
    for user in database["users"]:
        if username == user['username'] and password == user['password']:
            return True
    return False

def start_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port
    server_address = ('localhost', 1236)
    server_socket.bind(server_address)
    
    # Listen for incoming connections
    server_socket.listen(1)
    
    while True:
        # Wait for a connection
        print("Waiting for a connection")
        connection, client_address = server_socket.accept()
        
        try:
            print(f"Connection from {client_address}")
            load_database()

            # Handle authentication request
            data = connection.recv(1024).decode()
            username, password = data.split(':')

            if authenticate(username, password):
                print(f"Authentication recognized from {username}")
                connection.sendall(b"Authenticated\n")
                
                # Receive the data in small chunks and retransmit it
                data = connection.recv(1024).decode()
                print(f"{data} from {client_address}")

                # Send a message to the client side
                template = "Connect successfully - IP: {}"
                greeting = template.format(client_address[0])
                connection.sendall(greeting.encode())
            
            else:
                print(f"Authentication failed for {username}")
                connection.sendall(b"Authentication failed\n")

        finally:
            # Clean up the connection
            connection.close()

if __name__ == "__main__":
    start_server()