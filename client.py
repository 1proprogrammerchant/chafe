import socket
import threading
SERVER_ADDRESS = (input("host please... "), 3337)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)
username = input("username please... ")
print("ready")
def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        if message.startswith('CHANGE\n'):
            new_content = message[7:]
            print(new_content)
message_thread = threading.Thread(target=receive_messages)
message_thread.start()
while True:
    message = input()
    client_socket.send(("%s: %s\n" % (username, message)).encode())
    if message == '/quit':
        client_socket.send("DISCONNECT\n".encode())
        break
client_socket.close()
