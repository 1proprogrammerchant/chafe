import socket
import threading
cur = "null: null\n"
clients = []
def sendstr(connection, message):
    try:
        connection.sendall(message.encode())
    except BrokenPipeError:
        print("client ", connection, " died")
        clients.remove(connection)
def handle_client(connection, client_address):
    global cur
    global clients
    clients.append(connection)
    print(f"Current clients connected: {clients}")
    while True:
        data = connection.recv(1024).decode()
        if not data or data == "DISCONNECT\n":
            print(f"Client {client_address} disconnected")
            sendstr(connection, "ACK\n")
            clients.remove(connection)
            print(f"Clients connected: {clients}")
            connection.close()
            break
        print(f"Received data from {client_address}: {data}")
        
        if data == "GET\n":
            print(f"Sending current value of 'cur' to {client_address}: {cur}")
            sendstr(connection, cur)
        elif data == "USRS\n":
            for i in clients:
                sendstr(connection, i.getpeername()[0])
            sendstr(connection, "\n")
        elif data.startswith("GET / HTTP"):
            sendstr(connection, """HTTP/1.0 405 Method Not Allowed
Server: Stupid
Allow: DISCONNECT
Connection: close
Content-Type: text/html; charset=utf-8

<html><body><t>
hi, this is not an html page, pls dont be htmling at me
</t></body></html>""")
        elif data == "ALIVEOK\n":
            print(client_address, " alive")
        else:
            if cur != data:
                cur = data
                print(f"Set current value of 'cur' to {client_address}: {cur}")
                for client in clients:
                    if client != connection:
                        sendstr(client, ("CHANGE\n%s" % cur))
            else:
                sendstr(connection, "OK\n")
    connection.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 3337)
sock.bind(server_address)
sock.listen(-1)
print(f"Server listening on {server_address}")


while True:
    print("Waiting for a client connection...")
    connection, client_address = sock.accept()
    print(f"Accepted connection from {client_address}")
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()
    for i in clients:
        if i != connection:
            sendstr(i, "ALIVEREQ\n")
