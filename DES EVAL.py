from Cryptodome.Cipher import DES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad

# Clé DES (8 octets = 64 bits)
key = b'12345678'  # La clé doit être exactement 8 octets pour DES

# Texte à chiffrer
plaintext = b"Ceci est un message secret."
print(f'Ceci est le text : {plaintext}')
# -------- Mode ECB --------
def des_ecb_encrypt(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(plaintext, DES.block_size)  # Ajouter du padding
    encrypted = cipher.encrypt(padded_text)
    return encrypted

def des_ecb_decrypt(encrypted, key):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(encrypted), DES.block_size)  # Supprimer le padding
    return decrypted

# -------- Mode CBC --------
def des_cbc_encrypt(plaintext, key):
    iv = get_random_bytes(DES.block_size)  # Génération d'un vecteur d'initialisation aléatoire
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_text = pad(plaintext, DES.block_size)
    encrypted = iv + cipher.encrypt(padded_text)  # Ajouter l'IV au début du message chiffré
    return encrypted

def des_cbc_decrypt(encrypted, key):
    iv = encrypted[:DES.block_size]  # Récupérer l'IV
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted[DES.block_size:]), DES.block_size)
    return decrypted

# -------- Test des Fonctions --------
# Chiffrement et déchiffrement en ECB
encrypted_ecb = des_ecb_encrypt(plaintext, key)
print("Chiffrement ECB:", encrypted_ecb)
decrypted_ecb = des_ecb_decrypt(encrypted_ecb, key)
print("Déchiffrement ECB:", decrypted_ecb)

# Chiffrement et déchiffrement en CBC
encrypted_cbc = des_cbc_encrypt(plaintext, key)
print("Chiffrement CBC:", encrypted_cbc)
decrypted_cbc = des_cbc_decrypt(encrypted_cbc, key)
print("Déchiffrement CBC:", decrypted_cbc)
