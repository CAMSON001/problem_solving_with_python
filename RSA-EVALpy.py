import random
from Cryptodome.Util import number
import time
import matplotlib.pyplot as plt

def generate_keypair(key_length):
    p = number.getPrime(key_length // 2)
    q = number.getPrime(key_length // 2)
    n = p * q
    φ_n = (p - 1) * (q - 1)
    
    e = 65537  # Common choice for e
    d = pow(e, -1, φ_n)  # Calculate d using the modular inverse

    return (e, n), (d, n)  # Public key and private key

def encrypt(plaintext, pubkey):
    e, n = pubkey
    m = int.from_bytes(plaintext.encode(), 'big')
    c = pow(m, e, n)
    return c

def decrypt(ciphertext, privkey):
    d, n = privkey
    m = pow(ciphertext, d, n)
    plaintext = m.to_bytes((m.bit_length() + 7) //8 , 'big').decode()
    return plaintext

# Key lengths to evaluate
key_lengths = [512, 1024, 2048,4096]
gen_times = []
enc_times = []
dec_times = []

for length in key_lengths:
    start_time = time.time()
    pubkey, privkey = generate_keypair(length)
    gen_time = time.time() - start_time
    gen_times.append(gen_time)
    
    plaintext = "Hello World! this is RSA"
    start_time = time.time()
    ciphertext = encrypt(plaintext, pubkey)
    enc_time = time.time() - start_time
    enc_times.append(enc_time)

    start_time = time.time()
    decrypted_text = decrypt(ciphertext, privkey)
    dec_time = time.time() - start_time
    dec_times.append(dec_time)

    print(f"Key Length: {length} bits")
    print(f"Key Generation Time: {gen_time:.6f} sec")
    print(f"Encryption Time: {enc_time:.6f} sec")
    print(f"Decryption Time: {dec_time:.6f} sec")
    print(f"Decrypted Text: {decrypted_text}\n")

# Plotting the results
plt.plot(key_lengths, gen_times, label="Key Generation Time", marker='')
""" plt.plot(key_lengths, enc_times, label="Encryption Time", marker='')
plt.plot(key_lengths, dec_times, label="Decryption Time", marker='') """
plt.xlabel("Key Size (bits)")
plt.ylabel("CPU Time (seconds)")
plt.title("RSA Performance Analysis")
plt.legend()
plt.grid(True)
plt.show()
