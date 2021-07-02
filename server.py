from client import send
import socket
import threading


states = {}
names = {}
password = {}

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
LOGIN_MSG = "!LOGIN"
INFO_MSG = "!INFO"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)



def registrate_new_user(msg,conn,user_id):
    names[user_id] = "new_User"    
    name = msg.split(":")
    names[user_id] = name[1]
    password[user_id] = name[2]
    states[user_id] = "known_user"
    conn.send("Loggined".encode(FORMAT))

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")    
    user_id = addr
    states[user_id] = "unknown"
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            message_sended = False
            if  LOGIN_MSG in msg:
                registrate_new_user(msg,addr,conn,user_id)
                print(names[user_id],password[user_id])
            if msg == DISCONNECT_MSG:
                connected = False
                if states[user_id] == "unknown":
                    print(f"The User [{addr}] just disconnected.")
                else:
                    print(f"The User [{names[user_id]}] just disconnected.")
                break
            if msg == INFO_MSG:
                conn.send(f"  !LOGIN                   Comand to login\n  !DISCONNECT                   Command to disconnect from server\n serverIP:{SERVER}........".encode(FORMAT))
        if states[user_id] == "unknown":
            conn.send("Hey , you first time here. Type Login please".encode(FORMAT))
        if states[user_id] == "known_user":
            conn.send(f"sended".encode(FORMAT))
            print(f"{names[user_id]}-> {msg}")
    
    conn.close()


def start():
    server.listen()
    print(F"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f'[ACTIVATE CONNCTIONS] {threading.active_count() -1}')



print("[STARTING] server is starting...")
start()
