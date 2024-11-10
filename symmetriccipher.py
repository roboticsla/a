from Crypto.Cipher import DES
from Crypto.Util.Padding import *
from Crypto.Random import *


def encrypt_des(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded = pad(plaintext.encode(), DES.block_size)
    ciphertext = cipher.encrypt(padded)
    return ciphertext

def decrypt_des(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    decryptedtext = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return decryptedtext.decode()

key = get_random_bytes(8)
plaintext = "Hello world!"

ciphertext = encrypt_des(plaintext, key)
print("Encrypted DES : ", ciphertext)

decryptedtext = decrypt_des(ciphertext, key)
print("Decrypted DES : ", decryptedtext)


# AES encryption function
def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    padded_text = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return iv + ciphertext  # Prepend IV for use in decryption

# AES decryption function
def aes_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    return decrypted_text.decode()

key = get_random_bytes(16)  # AES key can be 16, 24, or 32 bytes
plaintext = "Hello, AES encryption!"

ciphertext = aes_encrypt(plaintext, key)
print("Encrypted:", ciphertext)

decrypted_text = aes_decrypt(ciphertext, key)
print("Decrypted:", decrypted_text)