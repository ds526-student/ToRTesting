import socket
import sys
import threading
import os

os.system('cls' if os.name == 'nt' else 'clear')

def server(port):
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sSocket.bind(('localhost', port))
    sSocket.listen(5)

    print(f"Server started on port {port}")

    while True:
        cSocket, cAddress = sSocket.accept()
        threading.Thread(target=threadClient, args=(cSocket, cAddress)).start()

        print(f"Connection from {cAddress} has been established.")


def threadClient(con, addr):
        try:
            while True:
                data = con.recv(1024).decode('utf-8')
                if not data:
                    print(f"Connection closed by client on port {addr[1]}")
                    break

                print(f"Received data: {data}")
                response = f"Server received: {data}"
                con.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            con.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tcpServer.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError as e:
        print(f"Invalid port number: {e}")
        sys.exit(1)

    print(f"THE PORT IS: {port}")
    server(port)