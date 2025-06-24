import socket
import sys
import threading
import os
import time
import enemy

os.system('cls' if os.name == 'nt' else 'clear')
playerCount = 0 # Number of players connected to the server
playerDict = {} # Dictionary to hold player information with playerId as key
playerIds = [] # List to hold playerIds to ensure unique playerIds
currentPlayerTurn = 0 # Variable to hold the current player's turn
playerTurnCounter = 0
enemyStats = enemy.enemyStats() # Create an instance of enemyStats

# Function to start the server and listen for incoming connections
def server(port):
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
    sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow the socket to be reused
    sSocket.bind(('localhost', port)) # Bind the socket to all interfaces on the specified port
    sSocket.listen(5) # Listen for incoming connections

    print(f"Server started on port {port}") 

    # Forever loop to accept incoming connections
    while True:
        cSocket, cAddress = sSocket.accept()
        threading.Thread(target=threadClient, args=(cSocket, cAddress)).start()

        print(f"Connection from {cAddress} has been established.")

# Function to create a player dictionary with address and port
def createPlayer(con, address, port, playerId, totalDmg=0):
    player = {
        "connection": con,
        "address": address,
        "port": port,
        "playerId": playerId,
        "totalDmg": totalDmg
    }
    return player

# Function to generate a new unique playerId
def newPlayerId():
    from random import randint
    newId = randint(1000, 9999)
    while newId in playerIds:
        newId = randint(1000, 9999)
    playerIds.append(newId)
    return newId

# Function to handle each client connection in a separate thread
def threadClient(con, addr):
        global playerCount # Use global variable to keep track of player count
        playerCount += 1 # Increment player count when a new player connects

        playerId = newPlayerId() # Generate a new unique playerId
        playerDict.update({playerId: createPlayer(con, addr[0], addr[1], playerId)}) # Add the new player to the playerDict

        print(f"Player {playerId} connected from {playerDict[playerId]['address']}:{playerDict[playerId]['port']}")

        con.sendall(playerId.to_bytes(4, byteorder='big')) # Send the playerId to the client as a 4-byte integer
        global currentPlayerTurn # Use global variable to keep track of the current player's turn
        global playerTurnCounter # Use global variable to keep track of the player turn counter

        # Wait until two players are connected before starting the game 
        while playerCount < 2:
            con.sendall(f"playercount wait {playerCount}".encode('utf-8'))
            time.sleep(3)

        con.sendall("players connected 2".encode('utf-8'))
        print("two players are connected, starting dungeon...")


        # con.sendall(b"Two players are now connected. You can now start the dungeon.\n")
        # con.sendall("Press r to start the dungeon.\n".encode('utf-8'))


        print(f"it is now player {currentPlayerTurn}'s turn.")

        # print(f"Player {playerCount} connected from {addr[0]}:{addr[1]}")
        try: 
            global enemyStats
            currentPlayerTurn = playerIds[playerTurnCounter] # Set the first playerId as the current player's turn
            # Continuously receive data from the client until they disconnect
            while True:
                print(f"Current player turn is: {currentPlayerTurn}")
                data = con.recv(1024).decode('utf-8')
                if not data: # If no data is received, the client has disconnected
                    print(f"Player {playerId} disconnected.")
                    del playerDict[playerId]
                    playerIds.remove(playerId)
                    playerCount -= 1
                    break
                sections = data.split(" ", 3) # Split the data into playerId, playerName, action, value e.g. "1234 attack 50"
                print(f"currentPlayerTurn: {currentPlayerTurn}")
                # if sections[0] != currentPlayerTurn:
                if sections[0] != str(currentPlayerTurn):
                    print(f"Player {sections[0]} tried to take their turn, but it is not their turn.")
                    con.sendall(f"turn no {sections[0]} {currentPlayerTurn}".encode('utf-8'))
                else:
                    print(f"Player {sections[0]} is taking their turn.")
                    if len(sections) < 4:
                        print("Invalid data received, expected format: '<playerId> <playerName> <action> <value>'")
                    else:
                        if sections[2] == "attack":
                            # get enemy stats and print them to client and server
                            # con.sendall(enemyStats.getEnemyStats().encode('utf-8')) # Send the enemy stats to the client

                            # return the damage dealth by the player to everyone
                            # response = f"Player {sections[0]} attack {sections[2]}"
                            # con.sendall(response.encode('utf-8'))

                            # enemy takes damage from player attack -> print enemy stats
                            enemyStats.takeDamage(int(sections[3])) 
                            enemyStats.printStats()

                            # Find the playerId associated with the current connection (con)
                            found_player = None
                            for pid, pdata in playerDict.items():
                                if pdata["connection"] == con:
                                    found_player = pdata
                                    break

                            if found_player is not None:
                                found_player["totalDmg"] += int(sections[3])
                            else:
                                print("Error: Player not found for this connection.")

                            # current enemy health returned to clients
                            response = f"Enemy health {enemyStats.health}/{enemyStats.maxHealth} "
                            con.sendall(response.encode('utf-8'))

                            time.sleep(0.3)

                            # Pass ignorePlayerId as an integer, not a set
                            broadcast_attack(f"{sections[0]} attacked {sections[3]}", ignorePlayerId=int(sections[0]))

                            # print(f"Received data: {sections[0]} {sections[1]} {sections[2]}")
                        elif sections[2] == "forfeit":
                            print(f"Player {sections[0]} has forfeited the game.")
                            con.sendall(b"You have forfeited the game.\n")
                            del playerDict[int(sections[0])]
                            playerIds.remove(int(sections[0]))
                            break

                        if playerTurnCounter >= len(playerIds) - 1:
                            playerTurnCounter = 0

                            # Find the player with the highest totalDmg
                            max_dmg_player = None
                            for pdata in playerDict.values():
                                if max_dmg_player is None or pdata["totalDmg"] > max_dmg_player["totalDmg"]:
                                    max_dmg_player = pdata
                            if max_dmg_player is not None:
                                response = f"Enemy attack {enemyStats.attack()}"
                                max_dmg_player["connection"].sendall(response.encode('utf-8'))
                        else:
                            playerTurnCounter += 1

                        currentPlayerTurn = playerIds[playerTurnCounter]
        except Exception:
            print(f"Client {playerId} connected from {addr[0]}:{addr[1]} has disconnected from the server.")
            del playerDict[playerId]  # Remove the player from the playerDict
            playerIds.remove(playerId)  # Remove the playerId from the playerIds list
            # con.sendall(f"Player {playerId} has disconnected from the server.\n".encode('utf-8'))
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

def broadcast_attack(message, ignorePlayerId=None):
    for player in playerDict.values():
        if ignorePlayerId is not None and player["playerId"] == ignorePlayerId:
            continue
        else:
            try:
                player["connection"].sendall(message.encode('utf-8'))
                time.sleep(0.1)
                player["connection"].sendall(enemyStats.getEnemyStats().encode('utf-8'))
            except Exception as e:
                print(f"Failed to send message to player {player['playerId']}: {e}")