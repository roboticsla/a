import socket
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sympy import mod_inverse

# ElGamal verification
def elgamal_verify(p, g, y, message_hash, r, s):
    if not (1 < r < p):
        return False
    lhs = pow(y, r, p) * pow(r, s, p) % p
    rhs = pow(g, message_hash, p)
    return lhs == rhs

# AES-128 decryption
def aes_decrypt(key, iv, ciphertext):
    cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, iv=bytes.fromhex(iv))
    return unpad(cipher.decrypt(bytes.fromhex(ciphertext)), AES.block_size)

# Server side implementation
def server_program():
    # ElGamal parameters
    p = 7919  # A prime number
    g = 2     # A generator
    y = 1234  # public key
    
    # Start the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    
    print("Server is listening...")
    
    conn, address = server_socket.accept()
    print(f"Connection from {address}")
    
    # Receive the data
    data = conn.recv(4096).decode()
    print("Recieved Data is: ", data)
    aes_key, iv, encrypted_message, signature = data.split('|')
    
    # Extract signature
    r, s = eval(signature)
    print("r,s values are: ", r, " ", s)
    # Decrypt the message using AES-128
    decrypted_message = aes_decrypt(aes_key, iv, encrypted_message)
    print("Decrypted Message is: ", decrypted_message)
    # Hash the decrypted message with SHA-512
    message_hash = int(hashlib.sha512(decrypted_message).hexdigest(), 16)
    
    # Verify the digital signature
    if elgamal_verify(p, g, y, message_hash, r, s):
        print("Signature is valid. Message:", decrypted_message.decode())
    else:
        print("Signature is invalid.")
    
    conn.close()

if __name__ == '__main__':
    server_program()
