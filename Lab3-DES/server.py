import asyncio
import websockets
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Use the same key for both server and client
key = b'12345678'  # Fixed 8-byte key
iv = get_random_bytes(8)  # Initialization Vector

def des_encrypt(plaintext, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext, DES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

async def handle_client(websocket, path):
    print("Client connected")

    # The message to be encrypted and sent to the client
    message = b"Hello, Client! This is a secret message."

    # Encrypt the message using DES
    encrypted_message = des_encrypt(message, key, iv)

    # Send the encrypted message and the IV to the client
    await websocket.send(iv + encrypted_message)  # Send IV + encrypted message
    print(f"Encrypted message sent to the client: {encrypted_message}")

async def start_server():
    async with websockets.serve(handle_client, "localhost", 65432):
        print("Server is listening on port 65432...")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(start_server())
