import socket
import threading
SERVER_ADDRESS = ("masterxeon.hopto.org", 3337)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)
username = input("username please... ")
print("ready")
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except:
            client_socket.close()
            return
        if message.startswith('CHANGE\n'):
            new_content = message[7:]
            print(new_content)
        if message == "ALIVEREQ\n":
            client_socket.send("ALIVEOK\n".encode())
message_thread = threading.Thread(target=receive_messages)
message_thread.start()
while True:
    message = input()
    if message == '/quit':
        client_socket.send("DISCONNECT\n".encode())
        break
    client_socket.send(("%s: %s\n" % (username, message)).encode())
client_socket.close()
