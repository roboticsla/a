import hmac
import hashlib

# Secret key for HMAC
key = b'secret_key'
# Data to hash
data = b"Hello, World!"

# Create an HMAC object using the SHA-512 hash algorithm
hmac_result = hmac.new(key, data, hashlib.sha512)

# Get the hexadecimal representation of the HMAC
hmac_digest = hmac_result.hexdigest()

print("HMAC with SHA-512:", hmac_digest)
