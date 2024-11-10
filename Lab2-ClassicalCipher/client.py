import asyncio
import websockets

async def test_ciphers():
    uri = "ws://localhost:8001"
    ciphers = ["caesar", "playfair", "hill", "vigenere", "rail_fence", "row_col"]
    test_message = "HELLO WORLD"

    async with websockets.connect(uri) as websocket:
        for cipher in ciphers:
            print(f"\nTesting {cipher.upper()} cipher:")
            await websocket.send(f"{cipher}:{test_message}")
            response = await websocket.recv()
            print(f"Original message: {test_message}")
            print(f"Server response: {response}")

            # Request the encrypted message from the server
            await websocket.send(f"get_encrypted")
            encrypted = await websocket.recv()
            print(f"Encrypted message: {encrypted}")

asyncio.get_event_loop().run_until_complete(test_ciphers())