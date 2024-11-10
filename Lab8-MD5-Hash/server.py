import asyncio
import hashlib
import hmac
import websockets
import json

async def compute_md5_hash(message):
    """Compute MD5 hash of the given message."""
    md5_hash = hashlib.md5(message.encode()).hexdigest()
    return md5_hash

async def compute_mac(message, secret_key):
    """Compute the Message Authentication Code (MAC) using MD5."""
    # Encode the message and secret key
    message_bytes = message.encode()
    secret_key_bytes = secret_key.encode()

    # Create HMAC object with MD5 as the hash function
    mac = hmac.new(secret_key_bytes, message_bytes, hashlib.md5).hexdigest()
    return mac

async def handle_connection(websocket, path):
    print(f"New connection: {path}")
    async for message in websocket:
        try:
            # Parse the incoming message as JSON
            data = json.loads(message)
            action = data.get('action')
            message_content = data.get('message')
            secret_key = data.get('secret_key', '')

            print(f"Received message: {data}")

            if action == 'md5_hash':
                result = await compute_md5_hash(message_content)
                print(f"Computed MD5 hash for '{message_content}': {result}")
            elif action == 'mac':
                result = await compute_mac(message_content, secret_key)
                print(f"Computed MAC for '{message_content}' with key '{secret_key}': {result}")
            else:
                result = 'Unknown action'
                print(f"Unknown action received: {action}")

            # Send the result back to the client
            response = {
                'action': action,
                'result': result
            }
            await websocket.send(json.dumps(response))
            print(f"Sent response: {response}")

        except Exception as e:
            # Handle any errors that occur
            error_response = {
                'error': str(e)
            }
            await websocket.send(json.dumps(error_response))
            print(f"Error occurred: {e}")

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server is running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
