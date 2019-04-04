#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome!", "utf8"))
        dict_addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(c):  

    name = c.recv(1024).decode("utf8")
    welcome = '%s if you want to quit, type {quit} to exit.' % name
    c.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[c] = name

    while True:
        msg = c.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            c.send(bytes("{quit}", "utf8"))
            c.close()
            del clients[c]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):

    for sock in dict_clients:
        sock.send(bytes(prefix, "utf8") + msg)


dict_clients = {}
dict_addresses = {}

HOST = ''
PORT = 1234
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
