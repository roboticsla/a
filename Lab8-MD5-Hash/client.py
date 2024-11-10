import asyncio
import websockets
import json

async def send_message():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Sending a request to compute MD5 hash
        request = {
            'action': 'md5_hash',
            'message': 'Hello, World!'
        }
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        print(f"MD5 Hash Response: {response}")

        # Sending a request to compute MAC
        request = {
            'action': 'mac',
            'message': 'Hello, World!',
            'secret_key': 'supersecretkey'
        }
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        print(f"MAC Response: {response}")

asyncio.run(send_message())
