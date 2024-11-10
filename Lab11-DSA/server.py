import socket
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def verify_signature(public_key, signature, message):
    try:
        public_key.verify(signature, message, hashes.SHA256())
        return True
    except:
        return False

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)

    print("Server listening on port 5000...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")

        data = client_socket.recv(4096).decode()
        received_data = json.loads(data)

        public_key_pem = received_data['public_key'].encode()
        public_key = load_pem_public_key(public_key_pem)
        
        signature = bytes.fromhex(received_data['signature'])
        message = received_data['message'].encode()

        is_valid = verify_signature(public_key, signature, message)

        if is_valid:
            response = "Signature is valid."
        else:
            response = "Signature is invalid."

        client_socket.send(response.encode())
        client_socket.close()

if __name__ == "__main__":
    start_server()