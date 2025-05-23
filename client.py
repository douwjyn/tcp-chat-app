# client.py
import socket
import threading
import colorama 

colorama.init()


HOST = '127.0.0.1'
PORT = 7878

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()

            if msg == "NAME":
                client.send(nickname.encode())
            else:
                print(colorama.Fore.YELLOW + f"\n{msg}" + colorama.Style.RESET_ALL)
        except:
            print("Connection closed.")
            exit()
def send():
    while True:
        msg = input()
        client.send("[{}]: {}".format(nickname, msg).encode())

threading.Thread(target=receive).start()
threading.Thread(target=send).start()
