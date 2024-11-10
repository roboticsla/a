import numpy as np
import asyncio
import websockets

def caesar_cipher(message: str, shift: int) -> str:
    result = ""
    for char in message:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
            result += chr(shifted)
        else:
            result += char
    return result

def playfair_cipher(message: str, key: str = "VITCHENNAI") -> str:
    print("Playfair Cipher's Keyword is ", key)
    def create_matrix(key):
        seen = set()
        key = "".join([x for x in key.upper() if x.isalpha() and not (x in seen or seen.add(x))])
        key += "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        key = "".join(dict.fromkeys(key))
        return [list(key[i:i+5]) for i in range(0, 25, 5)]

    def find_position(matrix, letter):
        for i, row in enumerate(matrix):
            if letter in row:
                return i, row.index(letter)
        return None  # Return None if the letter is not found

    def prepare_message(message):
        message = ''.join(char.upper() for char in message if char.isalpha()).replace("J", "I")
        prepared = []
        i = 0
        while i < len(message):
            if i == len(message) - 1 or message[i] == message[i+1]:
                prepared.extend([message[i], 'X'])
                i += 1
            else:
                prepared.extend([message[i], message[i+1]])
                i += 2
        return ''.join(prepared)

    matrix = create_matrix(key)
    message = prepare_message(message)

    result = ""
    for i in range(0, len(message), 2):
        a, b = message[i], message[i+1]
        pos_a = find_position(matrix, a)
        pos_b = find_position(matrix, b)
        
        if pos_a is None or pos_b is None:
            result += a + b  # If a character is not found, keep it unchanged
            continue
        
        row_a, col_a = pos_a
        row_b, col_b = pos_b

        if row_a == row_b:
            result += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            result += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            result += matrix[row_a][col_b] + matrix[row_b][col_a]

    return result

def hill_cipher(message: str) -> str:
    key = np.array([[3, 3], [2, 5]])

    message = message.upper()
    message_nums = [ord(char) - 65 for char in message if char.isalpha()]

    if len(message_nums) % 2 != 0:
        message_nums.append(0)

    result_nums = []
    for i in range(0, len(message_nums), 2):
        block = np.array(message_nums[i : i + 2])
        encrypted_block = np.dot(key, block) % 26
        result_nums.extend(encrypted_block)

    return "".join([chr(num + 65) for num in result_nums])

def vigenere_cipher(message: str, keyword: str) -> str:
    result = ""
    keyword = keyword.upper()
    print("Vigenere Cipher's Keyword is ", keyword)
    keyword_length = len(keyword)
    keyword_as_int = [ord(i) for i in keyword]

    for i, char in enumerate(message):
        if char.isalpha():
            if char.isupper():
                result += chr(
                    (ord(char) + keyword_as_int[i % keyword_length] - 130) % 26 + 65
                )
            else:
                result += chr(
                    (ord(char) + keyword_as_int[i % keyword_length] - 162) % 26 + 97
                )
        else:
            result += char

    return result

def rail_fence_cipher(message: str, rails: int) -> str:
    fence = [["\n" for _ in range(len(message))] for _ in range(rails)]
    rail = 0
    direction = 1

    for i, char in enumerate(message):
        fence[rail][i] = char
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    return "".join(char for rail in fence for char in rail if char != "\n")

def row_col_transposition_cipher(message: str, key: str) -> str:
    print("Row Col Cipher's Keyword is ", key)
    message = "".join(char.upper() for char in message if char.isalnum())
    key = key.upper()

    num_columns = len(key)

    if len(message) % num_columns != 0:
        message += "X" * (num_columns - (len(message) % num_columns))

    num_rows = len(message) // num_columns
    grid = [message[i : i + num_columns] for i in range(0, len(message), num_columns)]

    sorted_columns = sorted(range(num_columns), key=lambda i: key[i])

    return "".join(
        grid[row][col] for col in sorted_columns for row in range(num_rows)
    ).upper()

async def handler(websocket, path):
    async for message in websocket:
        messages = message.split(":")
        if len(messages) != 2:
            await websocket.send("Invalid message format")
            continue
        cipher, message = messages[0], messages[1]
        response = ""

        match cipher:
            case "caesar":
                shift = 5
                response = caesar_cipher(message, shift).upper()
            case "playfair":
                response = playfair_cipher(message).upper()
            case "hill":
                response = hill_cipher(message).upper()
            case "vigenere":
                keyword = "VITCHENNAI"
                response = vigenere_cipher(message, keyword).upper()
            case "rail_fence":
                rails = 3
                response = rail_fence_cipher(message, rails).upper()
            case "row_col":
                key = "VITCHENNAI"
                response = row_col_transposition_cipher(message, key).upper()
            case _:
                response = "Invalid cipher"

        await websocket.send(response)
        print(f"Type of Cipher: {cipher}\nPlain Text: {message}\nEncrypted Text: {response}\n")

async def main():
    server = await websockets.serve(handler, "localhost", 8001)
    print("Server started on ws://localhost:8001")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())