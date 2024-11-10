import socket
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

def generate_keys():
    private_key = dsa.generate_private_key(key_size=1024)
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message):
    return private_key.sign(message, hashes.SHA256())

def send_to_server(public_key, signature, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    public_key_pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    ).decode()

    data = {
        'public_key': public_key_pem,
        'signature': signature.hex(),
        'message': message
    }

    print("Public Key is: ",data['public_key'])
    print("Signature is ", data['signature'])
    print("Message is ", data['message'])

    client_socket.send(json.dumps(data).encode())

    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    private_key, public_key = generate_keys()
    message = input("Enter a message to sign: ").encode()
    signature = sign_message(private_key, message)
    print("Signature = ", signature)
    send_to_server(public_key, signature, message.decode())