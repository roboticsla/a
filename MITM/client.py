# client.py
import asyncio
import websockets

async def client():
    uri = "ws://localhost:5678"  # Connect to the MITM server
    async with websockets.connect(uri) as websocket:
        message = "Hello, Server!"
        print(f"[Client] Sending: {message}")
        await websocket.send(message)
        
        response = await websocket.recv()
        print(f"[Client] Received: {response}")

asyncio.get_event_loop().run_until_complete(client())
