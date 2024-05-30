import socket

class Client:
    def __init__(self, host='localhost', port=1236):
        self.client_socket = None
        self.host = host
        self.port = port

    def connect_to_server(self):
        # Create a TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (self.host, self.port)
        self.client_socket.connect(server_address)
        
        try:
            username = input("Username: ")
            password = input("Password: ")
            self.client_socket.sendall((f"{username}:{password}").encode())

            # Wait for authentication response
            response = self.client_socket.recv(1024).decode().strip()
            print(f"Authentication Status: {response}")

            if response == "Authenticated":
                # Send data
                message = input("Type in message: ")
                print(f'Sending a message: "{message}"')
                self.client_socket.sendall(message.encode())
                
                # Look for the response
                amount_received = 0
                amount_expected = len(message)
                
                while amount_received < amount_expected:
                    data = self.client_socket.recv(50)
                    amount_received += len(data)
                    print(f"Received: {data.decode()}")
            
            else:
                print("Sign-in failed.")

        finally:
            print("Closing socket..")
            self.client_socket.close()

if __name__ == "__main__":
    client = Client()
    client.connect_to_server()