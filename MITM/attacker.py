# mitm_server.py
import asyncio
import websockets

async def mitm_handler(client_ws, path):
    # Connect to the actual server
    async with websockets.connect("ws://localhost:8765") as server_ws:
        async def forward_client_to_server():
            async for message in client_ws:
                print(f"[MITM] Intercepted from Client: {message}")
                # Modify the message if needed
                modified_message = f"[MITM] {message}"
                await server_ws.send(modified_message)
                print(f"[MITM] Forwarded to Server: {modified_message}")

        async def forward_server_to_client():
            async for message in server_ws:
                print(f"[MITM] Intercepted from Server: {message}")
                # Forward the server's response to the client
                await client_ws.send(message)

        # Run both tasks concurrently
        await asyncio.gather(forward_client_to_server(), forward_server_to_client())

# Run the MITM server
start_mitm_server = websockets.serve(mitm_handler, "localhost", 5678)
print("[MITM] MITM Server listening on ws://localhost:5678")
asyncio.get_event_loop().run_until_complete(start_mitm_server)
asyncio.get_event_loop().run_forever()
