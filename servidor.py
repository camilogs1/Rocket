from socket import AF_INET, SO_REUSEADDR, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Establece el manejo de los clientes entrantes"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s se ha conectado." % client_address)
        client.send(bytes("¡Bienvenidos a Rocket! ¡Ahora escribe tu nombre y pulsa enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Toma el socket del cliente como argumento.
    """Maneja una sola conexión de cliente."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = '¡Bienvenido %s! Si alguna vez quieres salir, escribe quit para salir.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s ¡Se ha unido al chat!" % name
    print(name)
    user = '¡El usuario %s! Está en linea.' % name
    client.send(bytes(user, "utf8"))
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s ha dejado el chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix es para identificar el nombre.
    """Emite un mensaje a todos los clientes"""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = '172.20.10.10' # IP del servidor
PORT = 55555
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
SERVER.listen(100)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Esperando la conexión...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()