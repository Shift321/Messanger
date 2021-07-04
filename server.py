import socket

import threading
import sqlite3

msg_states = {}
states = {}
names = {}
password = {}
users = []

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
LOGIN_MSG = "!LOGIN"
INFO_MSG = "!INFO"
REGISTRATE_MSG = "!REGISTRATE"
INFO_TXT = f"      !LOGIN                        Comand to login\n      !DISCONNECT                   Command to disconnect from server\nUsers:{users}\nserverIP:{SERVER}........"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Users_data(login str, password str)""")

def login(login,password):
    pass


def registrate_new_user(msg,addr,conn,user_id):
    name = msg.split(":")
    sql_registrate = "SELECT * FROM Users_data WHERE login=?"    
    cursor.execute(sql_registrate,name(1))
    cursor_fetchall = cursor.fetchall()
    if cursor_fetchall == []:
        cursor.execute(f"""INSERT INTO Users_data VALUES("{name[1]}","{name[2]}")  """)
        states[user_id] = "known_user"
        conn.send("registrated".encode(FORMAT))
    else:
        conn.send(f"{name[1]} - this login alredy take. Try other.")


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
                conn.send("disconnecting...")
                break

        if states[user_id] == "unknown":
            conn.send("Hey , you first time here. Type Login please".encode(FORMAT))
        if states[user_id] == "known_user" and msg !=LOGIN_MSG:
            conn.send(f"sended".encode(FORMAT))
            print(f"{names[user_id]}-> {msg}")
            if msg == INFO_MSG:
                print(INFO_TXT)
    
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
