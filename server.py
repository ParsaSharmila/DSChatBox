#!/usr/bin/env python3
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM


def connections():
    while True:
        c, c_addrs = SERVER.accept()
        print("%s:%s has connected." % c_addrs)
        c.send(bytes("Welcome to the chat", "utf8"))
        dict_addresses[c] = c_addrs
        Thread(target=handle, args=(c,)).start()


def handle(c):

    name = c.recv(1024).decode("utf8")
    welcome = '%s if you want to quit, type {q}.' % name
    c.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    msg_broadcasting(bytes(msg, "utf8"))
    dict_clients[c] = name

    while True:
        msg = c.recv(1024)
        if msg != bytes("{q}", "utf8"):
            msg_broadcasting(msg, name + ": ")
        else:
            c.send(bytes("{q}", "utf8"))
            c.close()
            del dict_clients[c]
            msg_broadcasting(bytes("%s has left the chat." % name, "utf8"))
            break


def msg_broadcasting(msg, prefix=""):

    for sock in dict_clients:
        sock.send(bytes(prefix, "utf8") + msg)


dict_clients = {}
dict_addresses = {}

HOST = ''
PORT = 1234
ADDRS = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRS)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Server has started")
    THREAD = Thread(target=connections)
    THREAD.start()
    THREAD.join()
    SERVER.close()
