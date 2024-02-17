import os
import socket
from pyascon.ascon import ascon_encrypt, ascon_decrypt, get_random_bytes


# Generate random keys for User B to User A
key_a_to_b = os.environ.get('A_KEY')  # 16 bytes for Ascon-128
key_b_to_a = os.environ.get('B_KEY')
nonce = b'\x00' * 16  # 16 bytes of value 0
associated_data = b'CS645/745 Modern Cryptography: Secure Messaging'


def decrypt_message_from_a(ciphertexts):
    return ascon_decrypt(key_a_to_b.encode(), nonce, associated_data, ciphertexts, "Ascon-128")


def encrypt_message_to_a(plaintext):
    return ascon_encrypt(key_b_to_a.encode(), nonce, associated_data, plaintext, "Ascon-128")


# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# Connect to UserA
s.connect(('127.0.0.1', port))

while True:
    # Get input from UserB
    plaintext_message = input("UserB, enter your message: ")

    # Encrypt the input message
    encrypted_message = encrypt_message_to_a(plaintext_message.encode())

    # Send the length of the encrypted message
    s.sendall(len(encrypted_message).to_bytes(4, 'big'))

    # Send the encrypted message to UserA
    s.sendall(encrypted_message)

    # Receive the length of the ciphertext
    ciphertext_length = int.from_bytes(s.recv(4), 'big')

    # Receive ciphertext from UserA
    ciphertext = s.recv(ciphertext_length)

    # Decrypt the received ciphertext
    decrypted_message = decrypt_message_from_a(ciphertext)
    print('Decrypted Message from UserA:', decrypted_message.decode())
