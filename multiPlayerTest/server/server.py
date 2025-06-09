import socket
import sys
import threading
import os
import time

os.system('cls' if os.name == 'nt' else 'clear')
playerCount = 0
playerDict = {}
playerIds = []

def server(port):
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sSocket.bind(('0.0.0.0', port))
    sSocket.listen(5)

    print(f"Server started on port {port}")

    while True:
        cSocket, cAddress = sSocket.accept()
        threading.Thread(target=threadClient, args=(cSocket, cAddress)).start()

        print(f"Connection from {cAddress} has been established.")


def createPlayer(address, port):
    player = {
        "address": address,
        "port": port
    }
    return player

def newPlayerId():
    from random import randint
    newId = randint(1000, 9999)
    while newId in playerIds:
        newId = randint(1000, 9999)
    playerIds.append(newId)
    return newId


def threadClient(con, addr):
        import time
        global playerCount
        playerCount += 1

        playerId = newPlayerId()
        playerDict.update({playerId: createPlayer(addr[0], addr[1])})
        
        print(f"Player {playerId} connected from {playerDict[playerId]['address']}:{playerDict[playerId]['port']}")

        con.sendall(playerId.to_bytes(4, byteorder='big'))
        con.sendall(b"Welcome to the server!\n")
        time.sleep(2)

        con.sendall(b"You have now initiated the destruction process.\n")
        con.sendall(b"Establishing encrypted connection to remote server...\n")
        time.sleep(3)
        con.sendall(b"Transmitting sensitive data packets...\n")
        time.sleep(2)
        con.sendall(b"Bypassing local firewall and security protocols...\n")
        time.sleep(5)
        con.sendall(b"Data transfer beginning in 5 seconds. Please do not disconnect.\n")

        # Count backwards from 10 to 1, sending each number every second
        for i in range(5, 0, -1):
            time.sleep(1)
            con.sendall(str(i).encode('utf-8') + b"\n")

        # Send nonstop random lines for about 10 seconds
        from random import randint
        start = time.time()
        while time.time() - start < 5:
            random_message = ''.join(chr(randint(32, 126)) for _ in range(100))
            con.sendall((random_message + '\n').encode('utf-8'))

        con.sendall(b"\n" + b"\n" + b"\n" + b"\n" + b"jk ty for testing my server :)\n")
        con.sendall(b"You can now try sending messages to the server <3\n")
        # print(f"Player {playerCount} connected from {addr[0]}:{addr[1]}")
        try:
            while True:
                data = con.recv(1024).decode('utf-8')
                if not data:
                    print(f"Player {playerId} disconnected.")
                    del playerDict[playerId]
                    playerIds.remove(playerId)
                    break

                sections = data.split(" ", 1)
                if len(sections) < 2:
                    print("Invalid data received, expected format: '<playerId> <message>'")
                    continue

                print(f"Received data: {sections[0]} {sections[1]}")
                response = f"Server received: {sections[1]}"
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

    port = 39128
    print(f"THE PORT IS: {port}")
    server(port)

