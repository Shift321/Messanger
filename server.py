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
INFO_MSG = "!INFO"
REGISTRATE_MSG = "!REGISTRATE"
INFO_TXT = f"      !DISCONNECT                   Command to disconnect from server\nserverIP:{SERVER}........"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
connect_db = sqlite3.connect("database.db")
cursor = connect_db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Users_data(addr str,login str, password str)""")



def registrate_new_user(conn,addr,msg):
    data = msg.split(":")
    sql_registrate = "SELECT * FROM Users_data WHERE login=?"    
    cursor.execute(sql_registrate,data[1])
    cursor_fetchall = cursor.fetchall()
    if cursor_fetchall == []:
        cursor.execute(f"""INSERT INTO Users_data VALUES("{addr}","{data[1]}","{data[2]}")  """)
        connect_db.commit()
        states[addr] = "known_user"
        conn.send("registrated".encode(FORMAT))
    else:
        conn.send(f"{data[1]} - this login alredy take. Try other.".encode(FORMAT))

def check_user(conn,addr):
        sql_check_addr = "SELECT * FROM Users_data WHERE addr=?"
        cursor_check_addr = cursor.fetchall(sql_check_addr,addr)
        if cursor.fetchall == []:
            conn.send("you are not registrated".encode(FORMAT))
        ы


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")     
    check_user(conn,addr)
    conn.send("write your login and password".encode(FORMAT))
    states[addr] = "unknown"
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            check_user(conn,addr,msg)
            if msg == DISCONNECT_MSG:
                connected = False
                if states[addr] == "unknown":
                    print(f"The User [{addr}] just disconnected.")
                else:
                    print(f"The User [{names[addr]}] just disconnected.")
                conn.send("disconnecting...")
                break

        if states[addr] == "unknown":
            conn.send("Hey , you first time here. Type Login please".encode(FORMAT))
        if states[addr] == "known_user":
            conn.send(f"sended".encode(FORMAT))
            print(f"{addr}-> {msg}")
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
