import hashlib
import timeit

def calculate_mac(message, algorithm):
    """
    Calculate the MAC (Message Authentication Code) using the specified hash algorithm.
    
    Args:
        message (bytes): The message to be hashed.
        algorithm (str): The hash algorithm to use ('sha256' or 'sha384').
    
    Returns:
        bytes: The calculated MAC.
    """
    if algorithm == 'sha256':
        return hashlib.sha256(message).digest()
    elif algorithm == 'sha384':
        return hashlib.sha384(message).digest()
    else:
        raise ValueError("Invalid algorithm. Use 'sha256' or 'sha384'.")

def test_mac_time(message_sizes, iterations=10):
    """
    Measure the time consumption for calculating MACs using different hash algorithms and message sizes.
    
    Args:
        message_sizes (list): A list of message sizes (in bits) to test.
        iterations (int): The number of times to run each test (for averaging).
    """
    print("Message Size (bits),SHA-256 Time (ms),SHA-384 Time (ms)")
    for size in message_sizes:
        message = b"HelloYashJainThisisasampletesting12345HelloYashJainThisisasampletesting12345HelloYashJainThisisasampletesting12345" * (size // 8)  # Convert bits to bytes
        
        sha256_time = timeit.timeit(lambda: calculate_mac(message, 'sha256'), number=iterations) * 1000 / iterations
        sha384_time = timeit.timeit(lambda: calculate_mac(message, 'sha384'), number=iterations) * 1000 / iterations
        
        print(f"{size},{sha256_time:.2f},{sha384_time:.2f}")

# Example usage
message_sizes = [128, 256, 512, 1024, 2048, 4096]
test_mac_time(message_sizes)