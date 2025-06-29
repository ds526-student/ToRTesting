import player
import server.enemy as enemy
import os
import socket
import sys
import threading 
import combat
import time

os.system('cls' if os.name == 'nt' else 'clear')    
playerStats = player.playerStats()
gameStart = False

def listen_for_server(cSocket):
    while True:
        try:
            response = cSocket.recv(1024)
            if not response:
                print("Server closed the connection.")
                break
            response = response.decode('utf-8')
            splitResult = response.split(' ', 2)
            # print(f"Server response: {response}")

            if splitResult[1] == "attack":
                playerStats.takeDamage(int(splitResult[2]))
                print(f"You have been attacked for {splitResult[2]} damage!")
                playerStats.printStats()
            elif splitResult[1] == "Stats":
                statResult = response.split(' ', 4)
                print(f"Enemy Stats:\nHealth: {statResult[2]}\nDamage: {statResult[4]}")
            elif splitResult[1] == "health":
                print(f"Enemy health: {splitResult[2]}")
            elif splitResult[1] == "wait":
                print(f"Waiting for another player to connect... {splitResult[2]}/2 players connected.")
            elif splitResult[1] == "connected":
                print(f"Game started! {splitResult[2]} players connected.")
                print("Dungeon is now starting!")
                global gameStart
                gameStart = True
            elif splitResult[1] == "no":
                statResult = response.split(' ', 3)
                print(f"Not your turn. It is player {statResult[3]}'s turn.")
            elif splitResult[1] == "attacked":
                print(f"Player {splitResult[0]} has attacked the enemy for {splitResult[2]} damage!")
        except Exception:
            print(f"You have been disconnected from the server")
            break

def client():
    print("What is your name, brave adventurer?")
    playerName = input("Name: ")

    host = '127.0.0.1'
    port = 39128

    # user enters host and port
    # print("What is the server host address?")
    # host = input("Host: ")

    # print("What is the server port?")
    # port = int(input("Port: "))

    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cSocket.connect((host, port))
    response = cSocket.recv(4)
    playerId = int.from_bytes(response, byteorder='big')
    print(f"Connected to server as player {playerId}.")

    # Start a thread to listen for server messages
    listener = threading.Thread(target=listen_for_server, args=(cSocket,), daemon=True)
    listener.start()

    try:
        while True:
            global gameStart
            while (gameStart):
                data = input("Enter 'a' to attack, 'h' to heal, or 'r' to run: ").lower()

                if data.lower() == 'a':
                    playerDamage = playerStats.attack()
                    data = f"{playerId} {playerName} attack {playerDamage}"
                    time.sleep(0.3)
                    print(f"You attack for {playerDamage} damage!")
                    cSocket.sendall(data.encode('utf-8'))

                    # No recv here! Listener thread will handle all server responses.
                    if playerStats.health <= 0:
                        print("You have been defeated!")
                        break

                elif data.lower() == 'h':
                    playerStats.heal(10)
                    playerStats.printStats()

                elif data.lower() == 'r':
                    print("You ran away from the battle!")
                    cSocket.close()
                    sys.exit()
                    break

                elif data.lower() == 'clear':
                    print('\033[H\033[J')
                    continue

                elif data.lower() == 'exit':
                    print("Exiting the game...")
                    cSocket.close()
                    sys.exit()
                    break

                time.sleep(0.5)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cSocket.close()
        print("Disconnected from server.")
    

if __name__ == "__main__":
    client()