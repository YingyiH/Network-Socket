import socket
import json
import os



class Server:
    DATABASE_FILE = '../authentication.json'
    database = {}

    def __init__(self):
        self.server_socket = None

    def load_database(self):
        if os.path.exists(Server.DATABASE_FILE):
            with open(Server.DATABASE_FILE, 'r') as f:
                Server.database = json.load(f)

    @staticmethod
    def authenticate(username, password):
        for user in Server.database["users"]:
            if username == user['username'] and password == user['password']:
                return True
        return False

    def start_server(self):
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to a specific address and port
        server_address = ('localhost', 1236)
        self.server_socket.bind(server_address)
        
        # Listen for incoming connections
        self.server_socket.listen(1)
        
        while True:
            # Wait for a connection
            print("Waiting for a connection")
            connection, client_address = self.server_socket.accept()
            
            try:
                print(f"Connection from {client_address}")
                self.load_database()

                # Handle authentication request
                data = connection.recv(1024).decode()
                username, password = data.split(':')

                if Server.authenticate(username, password):
                    print(f"Authentication recognized from user --- {username}")
                    connection.sendall(b"Authenticated\n")
                    
                    # Receive the data in small chunks and retransmit it
                    # data = connection.recv(100)
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
    server = Server()
    server.start_server()