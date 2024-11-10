import socket
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from sympy import mod_inverse
from random import randint
import math

# ElGamal key generation
def elgamal_keygen(p, g):
    x = randint(1, p-2)  # Private key
    y = pow(g, x, p)     # Public key
    return (p, g, y), x  # (public_key, private_key)

# ElGamal signing
def elgamal_sign(p, g, x, message_hash):
    k = randint(1, p-2)
    while math.gcd(k, p-1) != 1:
        k = randint(1, p-2)
    r = pow(g, k, p)
    k_inv = mod_inverse(k, p-1)
    s = (k_inv * (message_hash - x * r)) % (p-1)
    return r, s

# AES-128 encryption
def aes_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv, ciphertext

# Hash the message with SHA-512
def hash_message(message):
    sha512 = hashlib.sha512()
    sha512.update(message)
    return int(sha512.hexdigest(), 16)

# Client side implementation
def client_program():
    # ElGamal parameters
    p = 7919  # A prime number
    g = 2     # A generator

    # Generate keys
    public_key, private_key = elgamal_keygen(p, g)
    
    # Input message to be sent
    message = input("Enter your message: ").encode()
    
    # Hash the message using SHA-512
    message_hash = hash_message(message)
    print('Hashed Message: ', message_hash)
    # Sign the message hash using ElGamal
    r, s = elgamal_sign(p, g, private_key, message_hash)
    
    # Encrypt the message using AES-128
    aes_key = os.urandom(16)  # AES-128 key
    iv, encrypted_message = aes_encrypt(aes_key, message)
    print('Encyrpted Message: ', encrypted_message)
    # Combine digital signature and encrypted message
    data_to_send = {
        'signature': (r, s),
        'encrypted_message': encrypted_message,
        'iv': iv
    }
    
    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))
    
    # Send AES key, encrypted message, and digital signature
    client_socket.sendall(f'{aes_key.hex()}|{data_to_send["iv"].hex()}|{data_to_send["encrypted_message"].hex()}|{data_to_send["signature"]}'.encode())

    client_socket.close()

if __name__ == '__main__':
    client_program()
