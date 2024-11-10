def hex_to_text(file_path):
    try:
        with open(file_path, 'r') as file:
            hex_data = file.read().strip()

        # Convert hex to bytes
        byte_data = bytes.fromhex(hex_data)

        try:
            # Attempt decoding as UTF-8
            text = byte_data.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to latin-1 if UTF-8 fails
            text = byte_data.decode('latin-1')

        return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
file_path = "CipherData.txt"
text_data = hex_to_text(file_path)

if text_data:
    print("Converted Text:")
    print(text_data)
