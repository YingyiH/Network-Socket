import socket

def connect_to_server():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 1236)
    client_socket.connect(server_address)
    
    try:
        username = input("Username: ")
        password = input("Password: ")
        client_socket.sendall((f"{username}:{password}").encode())

        # Wait for authentication response
        response = client_socket.recv(1024).decode().strip()
        print(f"Authentication Status: {response}")

        if response == "Authenticated":
            # Send data
            message = input("Type in message: ")
            print(f'Sending a message: "{message}"')
            client_socket.sendall(message.encode())
            
            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            
            while amount_received < amount_expected:
                data = client_socket.recv(50)
                amount_received += len(data)
                print(f"Received: {data.decode()}")
        
        else:
            print("Sign-in failed.")

    finally:
        print("Closing socket..")
        client_socket.close()

if __name__ == "__main__":
    connect_to_server()