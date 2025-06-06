import player
import enemy
import combat
import os
import socket
import sys


os.system('cls' if os.name == 'nt' else 'clear')    

def client():
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cSocket.connect((host, port))

    try:
        while True:
            data = input("Enter message to send to server (or 'exit' to quit): ")
            if data.lower() == 'exit':
                break
            
            cSocket.sendall(data.encode('utf-8'))
            response = cSocket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    client()



print("You are now in combat with an enemy!")

playerStats = player.playerStats()
enemyStats = enemy.enemyStats()

playerStats.printStats()
enemyStats.printStats()

while (True):
    x = input("Enter 'a' to attack, 'h' to heal, or 'r' to run: ").lower()

    if x == 'a':
        playerDamage = playerStats.attack()
        enemyStats.takeDamage(playerDamage)
        
        if enemyStats.health <= 0:
            print("Enemy defeated!")
            break
        
        enemyDamage = enemyStats.attack()
        playerStats.takeDamage(enemyDamage)

        playerStats.printStats()
        enemyStats.printStats()
        
        if playerStats.health <= 0:
            print("You have been defeated!")
            break

    elif x == 'h':
        playerStats.heal(10)
            
        playerStats.printStats()
        enemyStats.printStats()
    
    elif x == 'r':
        print("You ran away from the battle!")
        break