# actual_server.py
import asyncio
import websockets

async def server_handler(websocket, path):
    async for message in websocket:
        print(f"[Server] Received from MITM: {message}")
        response = f"Server received: {message}"
        await websocket.send(response)

start_server = websockets.serve(server_handler, "localhost", 8765)

print("[Server] Server listening on ws://localhost:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
