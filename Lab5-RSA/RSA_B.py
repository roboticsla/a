import asyncio
import websockets
from sympy import mod_inverse

# RSA key generation for B (Receiver)
p_B, q_B = 47, 59
n_B = p_B * q_B
phi_n_B = (p_B - 1) * (q_B - 1)
e_B = 19
d_B = mod_inverse(e_B, phi_n_B)
public_key_B = (e_B, n_B)
private_key_B = (d_B, n_B)

async def decrypt_and_verify(signed_and_encrypted_message, private_key_B, public_key_A):
    decrypted_and_verified_message = ''
    for encrypted_m in signed_and_encrypted_message.split():
        signed_m = pow(int(encrypted_m), private_key_B[0], private_key_B[1])
        original_m = pow(signed_m, public_key_A[0], public_key_A[1])
        decrypted_and_verified_message += chr(original_m)
    return decrypted_and_verified_message

async def receiver(websocket, path):
    # Send B's public key to A
    await websocket.send(f"{public_key_B[0]} {public_key_B[1]}")
    print("Public key sent to A.")

    # Receive the encrypted message and A's public key
    data = await websocket.recv()
    encrypted_message, e_A, n_A = data.split(';')
    public_key_A = (int(e_A), int(n_A))

    # Decrypt and verify the message
    decrypted_message = await decrypt_and_verify(encrypted_message, private_key_B, public_key_A)
    print(f"Decrypted and Verified Message: {decrypted_message}")

async def main():
    async with websockets.serve(receiver, "localhost", 12345):
        print("Server B listening on ws://localhost:12345")
        await asyncio.Future()  # Run forever

asyncio.run(main())
