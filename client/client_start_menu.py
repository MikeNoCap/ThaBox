import socket
import select
import errno
from pynput import keyboard
import threading
<<<<<<< HEAD
import time

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from utils import clear



console: Console = Console()

# Sets variables used later on for use with sockets
HEADER: int = 64
PORT: int = 5050
FORMAT: str = 'utf-8'
DISCONNECT_MESSAGE: str = '!DISCONNECT'

clear()



# Prompts the user for the IP address
SERVER: str = console.input("Server IP:")

ADDR: set = (SERVER, PORT)

# Creates a connection to the server
client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def join(name: str) -> None:
    """
    Function of which sends data to the server to connect the user
    """
    name: bytes = name.encode(FORMAT)
    name_length: int = len(name)
    send_length: str = str(name_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(name)
    print(client.recv(1000).decode(FORMAT))


def send_message(message: str) -> None:
    """
    Function which will allow the user to send a message
    """
    message: bytes = message.encode(FORMAT)
    msg_length: int = len(message)
    msg_length: str = str(msg_length).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))
    client.send(msg_length)
    client.send(message)
    time.sleep(0.1)


# Prompts the user for their username
name: str = console.input("What is your name?: ")
join(name)

message = ''


def send_message_loop() -> None:
    """
    Send message loop function.
    """
    while True:
        print(message)
        send_message(console.input("Type something: "))
=======
import sys
from time import sleep

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)
>>>>>>> afdb1bf3afaa454138ea16895d0f3cd1baf1a19a

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

is_typing = False


def send_message() -> None:
    # Wait for user to input a message
    global is_typing
    is_typing = True


def receive_messages() -> None:
    global is_typing
    while True:
        sleep(0.1)
        while not is_typing:
            try:
                username_header = client_socket.recv(HEADER_LENGTH)

                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()

                # Convert header to int value
                username_length = int(username_header.decode('utf-8').strip())

                # Receive and decode username
                username = client_socket.recv(username_length).decode('utf-8')

                # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                # Print message
                print(f'{username} > {message}')

            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()

                # We just did not receive anything
                continue

            except Exception as e:
                # Any other exception - something happened, exit
                print('Reading error: '.format(str(e)))
                sys.exit()
        else:
            message = input(f'{my_username} > ')

            # If message is not empty - send it
            if message:

                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
            else:
                continue

            is_typing = False


def hotkeys():
    with keyboard.GlobalHotKeys({
            '/': send_message,
            '<ctrl>+q': exit}) as h:
        h.join()


receive_messages()
