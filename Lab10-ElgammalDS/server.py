import asyncio
import websockets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha512
import json

# ElGamal keys (Pre-generated for simplicity)
elgamal_p = 23  # Prime number
elgamal_g = 5   # Generator
elgamal_private_key = 7  # Private key
elgamal_public_key = pow(elgamal_g, elgamal_private_key, elgamal_p)  # Public key

# AES key (Symmetric)
aes_key = b'sixteenbytekeyyy'  # AES-128 key (16 bytes)


def decrypt_message_aes(ciphertext, iv):
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return plaintext


def verify_elgamal_signature(message_hash, signature, public_key):
    r, s = signature
    if not (1 <= r < elgamal_p):
        return False

    v1 = pow(elgamal_g, message_hash, elgamal_p)
    v2 = (pow(public_key, r, elgamal_p) * pow(r, s, elgamal_p)) % elgamal_p
    return v1 == v2


async def server_handler(websocket, path):
    async for message in websocket:
        # Receive the data from the client
        data = json.loads(message)
        encrypted_message = bytes.fromhex(data["encrypted_message"])
        iv = bytes.fromhex(data["iv"])
        signature = data["signature"]
        client_public_key = data["public_key"]

        # Decrypt the message
        decrypted_message = decrypt_message_aes(encrypted_message, iv)
        print(f"Decrypted message: {decrypted_message}")

        # Verify the signature
        message_hash = int.from_bytes(sha512(decrypted_message.encode()).digest(), byteorder="big")
        is_valid = verify_elgamal_signature(message_hash, signature, client_public_key)

        if is_valid:
            print("Signature is valid. Message is authenticated.")
            await websocket.send("Message received and verified successfully.")
        else:
            print("Signature verification failed!")
            await websocket.send("Signature verification failed.")


start_server = websockets.serve(server_handler, "localhost", 12345)

print("Server started on ws://localhost:12345")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
