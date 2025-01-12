import random

# Step 1: Select common parameters (prime p and base g)
def generate_prime_and_base():
    # For demonstration, we'll use small values for p and g.
    p = 23  # A prime number
    g = 5   # A primitive root modulo p
    return p, g

# Step 2: Generate private keys and compute public values
def generate_private_key():
    return random.randint(1, 20)  # Random private key between 1 and 20

def compute_public_value(private_key, g, p):
    return pow(g, private_key, p)  # g^private_key mod p

# Step 3: Exchange public values and compute shared secret keys
def compute_shared_secret(public_value, private_key, p):
    return pow(public_value, private_key, p)  # public_value^private_key mod p

# User A
p, g = generate_prime_and_base()
private_key_A = generate_private_key()
public_value_A = compute_public_value(private_key_A, g, p)

# User B
private_key_B = generate_private_key()
public_value_B = compute_public_value(private_key_B, g, p)

# Exchange public values
# User A computes the shared secret
shared_secret_A = compute_shared_secret(public_value_B, private_key_A, p)

# User B computes the shared secret
shared_secret_B = compute_shared_secret(public_value_A, private_key_B, p)

# Results
print(f"Common parameters: p = {p}, g = {g}")
print(f"User A's private key: {private_key_A}")
print(f"User A's public value: {public_value_A}")
print(f"User B's private key: {private_key_B}")
print(f"User B's public value: {public_value_B}")
print(f"User A's computed shared secret: {shared_secret_A}")
print(f"User B's computed shared secret: {shared_secret_B}")

# Verify that both shared secrets are equal
if shared_secret_A == shared_secret_B:
    print("Shared secret established successfully!")
else:
    print("Shared secret mismatch!")
