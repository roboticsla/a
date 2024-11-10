import asyncio
import websockets
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Same key as the server
key = b'12345678901234567890123456789012'  # Use a 32-byte AES key for AES-256

def aes_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded_plaintext = cipher.decrypt(ciphertext)
    decrypted_plaintext = unpad(decrypted_padded_plaintext, AES.block_size)
    return decrypted_plaintext

async def start_client():
    uri = "ws://localhost:65432"
    async with websockets.connect(uri) as websocket:
        print("Connected to the server")

        # Receive the data from the server
        data = await websocket.recv()

        # Extract the IV and the encrypted message
        iv = data[:16]  # The first 16 bytes are the IV for AES
        encrypted_message = data[16:]  # The rest is the encrypted message

        # Decrypt the message using AES
        decrypted_message = aes_decrypt(encrypted_message, key, iv)

        print(f"Decrypted message from the server: {decrypted_message.decode()}")

if __name__ == "__main__":
    asyncio.run(start_client())
