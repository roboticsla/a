import random
import websockets
import asyncio

def is_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

def generate_keys(bits):
    p = generate_prime(bits)
    g = random.randint(2, p - 1)
    x = random.randint(1, p - 2)
    h = pow(g, x, p)
    return p, g, x, h

def decrypt(c1, c2, x, p):
    s = pow(c1, x, p)
    m = (c2 * pow(s, p - 2, p)) % p
    return m

async def handle_client(websocket, path):
    # Generate keys
    p, g, x, h = generate_keys(256)
    print(f"Public key: (p={p}, g={g}, h={h})")
    
    # Send public key to client
    await websocket.send(f"{p},{g},{h}")
    
    while True:
        # Receive encrypted message from client
        data = await websocket.recv()
        c1, c2 = map(int, data.split(','))
        print(f"Received encrypted message: ({c1}, {c2})")
        
        # Decrypt message
        m = decrypt(c1, c2, x, p)
        print(f"Decrypted message: {m}")

# Start WebSocket server
async def main():
    server = await websockets.serve(handle_client, "localhost", 65432)
    print("WebSocket server started at ws://localhost:65432")
    await server.wait_closed()

asyncio.run(main())
