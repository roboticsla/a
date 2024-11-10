import asyncio
import websockets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Use a 32-byte (256-bit) key for AES
key = b'12345678901234567890123456789012'  # Use a 32-byte AES key for AES-256
iv = get_random_bytes(16)   # 16-byte IV for AES

def aes_encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

async def handle_client(websocket, path):
    print("Client connected")

    # The message to be encrypted and sent to the client
    message = b"Hello, Client! This is a secret message."

    # Encrypt the message using AES
    encrypted_message = aes_encrypt(message, key, iv)

    # Send the IV and the encrypted message to the client
    await websocket.send(iv + encrypted_message)  # Send IV + encrypted message
    print(f"Encrypted message sent to the client: {encrypted_message}")

async def start_server():
    async with websockets.serve(handle_client, "localhost", 65432):
        print("Server is listening on port 65432...")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(start_server())
