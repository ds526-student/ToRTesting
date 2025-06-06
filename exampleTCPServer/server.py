import socket
import sys
from datetime import datetime

def server(port):
    # Create a socket object to receive incoming connections
    welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a public host and the specified port
    welcomeSocket.bind(('localhost', port))
    # Start listening for incoming connections
    welcomeSocket.listen(1)
    print(f"Server is listening on port {port}...")
    while True:
        # Accept a connection
        clientSocket, clientAddress = welcomeSocket.accept()
        print(f"Connection established with {clientAddress}")
        try:
            # Receive data from the client (up to 1024 bytes) using recv()
            data = clientSocket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received date from client: {data}")
            # Parse the date and calculate the weekday
            try:
                date_object = datetime.strptime(data, '%Y-%m-%d')
                weekday = date_object.strftime('%A')
            except ValueError:
                weekday = "Invalid date format. Use YYYY-MM-DD."
            # Send the weekday back to the client
            clientSocket.send(weekday.encode('utf-8'))
        finally:
            # Close the client connection
            clientSocket.close()
            print(f"Connection with {clientAddress} closed.")

if __name__ == "__main__":
    # Ensure the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    
    # Get the port number from the command line
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Please provide a valid integer.")
        sys.exit(1)
    
    # Start the server with the specified port
    server(port)