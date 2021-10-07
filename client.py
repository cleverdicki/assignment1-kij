import socket
import os
import sys
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

key = RSA.generate(2048)
with open('myPrivateKey.pem', 'wb') as f:
    f.write(key.export_key('PEM'))

with open('myPublicKey.pem', 'wb') as f:
    f.write(key.publickey().export_key('PEM'))

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


try:
    def check_file(file):
        while len(file) % 16 != 0:
            file = file + b'0'
        return file

    pubKey = RSA.import_key(open("myPublicKey.pem").read())
    session_key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(pubKey)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher = AES.new(session_key, AES.MODE_CBC, 'This is an IV456'.encode("utf8"))

    message = "plain_text.txt"
    filelocation = os.path.abspath(message)
    with open(filelocation, 'rb') as f:
        data = f.read()

    checked_data = check_file(data)
    ciphertext = cipher.encrypt(checked_data)
    # encrypted_data = cipher.encrypt(checked_data)

    with open("temp.bin", "wb") as f:
        [ f.write(x) for x in (enc_session_key, ciphertext) ]

    with open("temp.bin", "rb") as f:
        encrypted_data = f.read()

    client_socket.send(encrypted_data)
    sys.stdout.write('>> \n')
    sys.stdout.write(client_socket.recv(1024).decode())
    client_socket.close()

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)