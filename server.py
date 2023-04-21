import socket
import threading

cur = "Hello, world!\n"
clients = []
def handle_client(connection, client_address):
    global cur
    while True:
        data = connection.recv(1024).decode()
        if not data or data == "DISCONNECT\n":
            print(f"Client {client_address} disconnected")
            break
        print(f"Received data from {client_address}: {data}")
        
        if data == "GET\n":
            print(f"Sending current value of 'cur' to {client_address}: {cur}")
            connection.sendall(cur.encode())
        else:
            if cur != data:
                cur = data
                print(f"Set current value of 'cur' to {client_address}: {cur}")
                for client in clients:
                    if client != connection:
                        client.sendall(("CHANGE\n%s" % cur).encode())
            else:
                connection.sendall("OK\n".encode())
    connection.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 3337)
sock.bind(server_address)
sock.listen(5)
print(f"Server listening on {server_address}")


while True:
    print("Waiting for a client connection...")
    connection, client_address = sock.accept()
    print(f"Accepted connection from {client_address}")
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()