import os
import socket
from pyascon.ascon import ascon_decrypt, ascon_encrypt

# Generate random keys for User A to User B
key_a_to_b = os.environ.get('A_KEY')  # 16 bytes for Ascon-128
key_b_to_a = os.environ.get('B_KEY')
nonce = b'\x00' * 16  # 16 bytes of value 0
associated_data = b'CS645/745 Modern Cryptography: Secure Messaging'


def decrypt_message_from_b(ciphertexts):
    print("Encrypted message from User B: ", ciphertexts)
    return ascon_decrypt(key_b_to_a.encode(), nonce, associated_data, ciphertexts, "Ascon-128")


def encrypt_message_to_b(plaintext):
    return ascon_encrypt(key_a_to_b.encode(), nonce, associated_data, plaintext, "Ascon-128")


# Create a socket object
s = socket.socket()

# Define the port on which you want to listen
port = 12345

# Bind the socket to the address
s.bind(('0.0.0.0', port))

# Listen for incoming connections
s.listen(5)
print("UserA is listening for incoming connections...")

try:
    while True:
        # Accept a connection
        c, addr = s.accept()
        print('Got connection from', addr)

        try:
            while True:
                # Receive the length of the ciphertext
                ciphertext_length = int.from_bytes(c.recv(4), 'big')
                if ciphertext_length == 0:
                    # If the length is 0, the other side closed the connection
                    print('Connection closed by UserB.')
                    break

                # Receive ciphertext from UserB
                ciphertext = c.recv(ciphertext_length)
                if ciphertext == b'exit':
                    print('Connection closed by UserB.')
                    break

                # Decrypt the received ciphertext if the connection is still open
                if c.fileno() != -1:  # Check if the socket is still open
                    decrypted_message = decrypt_message_from_b(ciphertext)
                    print('Decrypted Message from UserB:', decrypted_message.decode())

                    # Get input from UserA
                    plaintext_message = input("UserA, enter your message: ")

                    if plaintext_message.lower() == 'exit':
                        # If UserA enters 'exit', close the connection
                        c.sendall(len(plaintext_message).to_bytes(4, 'big'))
                        c.sendall(plaintext_message.encode())
                        c.close()
                        print('Connection closed by UserA.')
                        break

                    # Encrypt the input message
                    encrypted_message = encrypt_message_to_b(plaintext_message.encode())

                    # Send the length of the encrypted message
                    c.sendall(len(encrypted_message).to_bytes(4, 'big'))

                    # Send the encrypted message to UserB
                    c.sendall(encrypted_message)

        except KeyboardInterrupt:
            print('Connection closed by UserA.')
            break

except KeyboardInterrupt:
    print('Server terminated by UserA.')

finally:
    s.close()
