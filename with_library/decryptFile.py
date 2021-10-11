from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

file_in = open("encrypted_file", "rb")

private_key = RSA.import_key(open("myPrivateKey.pem").read())

enc_session_key, ciphertext = \
   [ file_in.read(x) for x in (private_key.size_in_bytes(), -1) ]

# Decrypt the session key with the private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_CBC)
data = cipher_aes.decrypt(ciphertext)
print(data)