import socket
import os
import sys
from Crypto.Cipher import AES
import hashlib

password = b'mypassword'
key = hashlib.sha256(password).digest()
mode = AES.MODE_CBC
IV = 'This is an IV456'

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    def check_file(file):
        while len(file) % 16 != 0:
            file = file + b'0'
        return file
    
    cipher = AES.new(key, mode, IV)

    message = "plain_text.txt"
    filelocation = os.path.abspath(message)
    with open(filelocation, 'rb') as f:
        data = f.read()

    checked_data = check_file(data)
    encrypted_data = cipher.encrypt(checked_data)

    print(encrypted_data)

    client_socket.send(encrypted_data)
    sys.stdout.write('>> \n')
    sys.stdout.write(client_socket.recv(1024).decode())
    client_socket.close()

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)