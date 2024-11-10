import random
import websockets
import asyncio

def encrypt(m, p, g, h):
    y = random.randint(1, p - 2)
    c1 = pow(g, y, p)
    s = pow(h, y, p)
    c2 = (m * s) % p
    return c1, c2

async def main():
    uri = "ws://localhost:65432"
    
    async with websockets.connect(uri) as websocket:
        print(f"Connected to server at {uri}")
        
        # Receive public key from server
        data = await websocket.recv()
        p, g, h = map(int, data.split(','))
        print(f"Received public key: (p={p}, g={g}, h={h})")
        
        while True:
            m = int(input("Enter a message (integer) to encrypt (or 0 to quit): "))
            
            if m == 0:
                break
            
            c1, c2 = encrypt(m, p, g, h)
            print(f"Encrypted message: ({c1}, {c2})")
            
            # Send encrypted message to server
            await websocket.send(f"{c1},{c2}")

# Run the client
asyncio.run(main())
