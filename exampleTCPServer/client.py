import socket
import sys

def client():
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python client.py <hostname> <port>")
        sys.exit(1)
    
    # Get hostname and port from command line arguments
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    
    # Create a socket object
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    clientSocket.connect((hostname, port))
    
    try:
        # Input a date from the user
        date = input("Enter a date (YYYY-MM-DD): ")
        
        # Send the date to the server
        clientSocket.send(date.encode('utf-8'))
        
        # Receive the response (weekday) from the server
        response = clientSocket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
    finally:
        # Close the connection
        clientSocket.close()

if __name__ == "__main__":
    client()