import hashlib

# Sample data to hash
data = "Hello, World!"

# Create a SHA-512 hash object
sha512_hash = hashlib.sha512()

# Update the hash object with the bytes of the data
sha512_hash.update(data.encode())

# Get the hexadecimal representation of the hash
hash_result = sha512_hash.hexdigest()

print("SHA-512 Hash:", hash_result)
