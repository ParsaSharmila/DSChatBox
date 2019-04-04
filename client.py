#!/usr/bin/env python3
"""client script"""
import tkinter
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM


def receive_message():
    while True:
        try:
            msg = socket.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def receive_file():
    while True:
        rfile = open("received_history.txt", "ab")
        file_data = socket.recv(1024)
        rfile.write(file_data)


def send_message(event=None):
    msg = my_message.get()
    my_message.set("")
    socket.send(bytes(msg, "utf8"))
    if msg == "{q}":
        socket.close()
        top.quit()


def close_window(event=None):
    my_message.set("{q}")
    send_message()


top = tkinter.Tk()
top.title("Chat Box")

messages_frame = tkinter.Frame(top)
my_message = tkinter.StringVar()
my_message.set("Messages can be written here")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=20, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

message_box = tkinter.Entry(top, textvariable=my_message)
message_box.bind("<Return>", send_message)
message_box.pack()
button_send = tkinter.Button(top, text="Send Message", command=send_message)
button_send.pack()

top.protocol("WM_DELETE_WINDOW", close_window)

HOST = input('Enter server host: ')
PORT = input('Enter server port: ')
if not PORT:
    PORT = 1234
else:
    PORT = int(PORT)

ADDRESS = (HOST, PORT)

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(ADDRESS)

thread = Thread(target=receive_message)
thread.start()
receivefile_thread = Thread(target=receive_file)
receivefile_thread.start()
tkinter.mainloop() 



