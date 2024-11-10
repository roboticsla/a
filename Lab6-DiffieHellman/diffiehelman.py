import random

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if p % 2 != 0 and is_prime(p):
            return p

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def diffie_hellman_key_exchange(p, g, users):
    # Implement the Diffie-Hellman key exchange protocol for multiple users
    private_keys = {user: random.randint(1, p - 1) for user in users}
    public_keys = {user: pow(g, private_keys[user], p) for user in users}

    shared_keys = {}
    for user1 in users:
        for user2 in users:
            if user1 != user2:
                shared_key = pow(public_keys[user2], private_keys[user1], p)
                shared_keys[(user1, user2)] = shared_key

    return shared_keys

p = generate_prime(5)
g = random.randint(2, p - 1)
users = ['Alice', 'Bob', 'Charlie']
shared_keys = diffie_hellman_key_exchange(p, g, users)

print(f"Prime number (p): {p}")
print(f"Generator (g): {g}")
print("Shared keys:")
for (user1, user2), key in shared_keys.items():
    print(f"{user1} and {user2} shared key: {key}")