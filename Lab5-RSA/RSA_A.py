import asyncio
import websockets
from sympy import mod_inverse

# RSA key generation for A (Sender)
p_A, q_A = 61, 53
n_A = p_A * q_A
phi_n_A = (p_A - 1) * (q_A - 1)
e_A = 17
d_A = mod_inverse(e_A, phi_n_A)
public_key_A = (e_A, n_A)
private_key_A = (d_A, n_A)

async def sign_and_encrypt(message, private_key_A, public_key_B):
    signed_and_encrypted_message = ''
    for char in message:
        m = ord(char)
        signed_m = pow(m, private_key_A[0], private_key_A[1])
        encrypted_m = pow(signed_m, public_key_B[0], public_key_B[1])
        signed_and_encrypted_message += f'{encrypted_m} '
    return signed_and_encrypted_message.strip()

async def sender():
    uri = "ws://localhost:12345"
    async with websockets.connect(uri) as websocket:
        # Receive B's public key
        data = await websocket.recv()
        e_B, n_B = map(int, data.split())
        public_key_B = (e_B, n_B)

        # Message to be sent
        message = 'HELLOWORLDHOWAREYOU'

        # Sign and encrypt the message
        encrypted_message = await sign_and_encrypt(message, private_key_A, public_key_B)

        # Send the encrypted message and A's public key
        await websocket.send(f"{encrypted_message};{public_key_A[0]};{public_key_A[1]}")
        print("Message sent to B.")

asyncio.run(sender())
