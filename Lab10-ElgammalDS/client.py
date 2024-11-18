import asyncio
import websockets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha512
import random
import json

# ElGamal keys (Pre-generated for simplicity)
elgamal_p = 23  # Prime number
elgamal_g = 5   # Generator
elgamal_private_key = 7  # Private key
elgamal_public_key = pow(elgamal_g, elgamal_private_key, elgamal_p)  # Public key

# AES key (Symmetric)
aes_key = b'sixteenbytekeyyy'  # AES-128 key (16 bytes)


def encrypt_message_aes(message):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return iv, ciphertext


def sign_elgamal(message_hash):
    # Generate k and ensure it's invertible modulo (elgamal_p - 1)
    while True:
        k = random.randint(1, elgamal_p - 2)
        try:
            k_inverse = pow(k, -1, elgamal_p - 1)  # Inverse of k modulo (elgamal_p - 1)
            break  # Exit the loop if k is invertible
        except ValueError:
            continue  # If k is not invertible, try again

    r = pow(elgamal_g, k, elgamal_p)
    s = (k_inverse * (message_hash - elgamal_private_key * r)) % (elgamal_p - 1)
    return r, s


async def client_handler():
    uri = "ws://localhost:12345"

    async with websockets.connect(uri) as websocket:
        # Input message from the user
        message = input("Enter a message (> 256 bits): ")

        # Encrypt the message
        iv, encrypted_message = encrypt_message_aes(message)

        # Hash the message
        message_hash = int.from_bytes(sha512(message.encode()).digest(), byteorder="big")

        # Sign the message hash using ElGamal
        signature = sign_elgamal(message_hash)

        # Prepare data to send
        data = {
            "encrypted_message": encrypted_message.hex(),
            "iv": iv.hex(),
            "signature": signature,
            "public_key": elgamal_public_key,
        }

        # Send data to the server
        await websocket.send(json.dumps(data))

        # Wait for server response
        response = await websocket.recv()
        print(f"Server response: {response}")


if __name__ == "__main__":
    asyncio.run(client_handler())  # Use asyncio.run() in place of deprecated get_event_loop()
