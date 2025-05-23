# server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 7878

clients = []
nicknames = []

def handle(conn, addr):
    while True:
        try:
            msg = conn.recv(1024)
            broadcast(msg, conn)
        except:
            index = clients.index(conn)
            nickname = nicknames[index]

            print(f"[-] {addr} : {nickname} disconnected")
            broadcast("{} disconnected.".format(nickname).encode(), conn)

            clients.remove(conn)
            nicknames.remove(nickname)
            conn.close()
            break

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        conn.send('NAME'.encode());

        nickname = conn.recv(1024).decode()    

        print("Connected with {} \nNickname: {}".format(str(addr), nickname))

        clients.append(conn)
        nicknames.append(nickname)

        broadcast("{} joined the server!".format(nickname).encode(), conn)
        conn.send('Connected to server!'.encode());

        threading.Thread(target=handle, args=(conn, addr)).start()

if __name__ == '__main__':
    main()
