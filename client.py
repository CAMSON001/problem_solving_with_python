import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad,unpad
from Cryptodome.Hash import SHA256
import os
import threading
import struct

# Configuration du client
server_ip = "172.16.2.40"  # Changez ceci si nécessaire
server_port = 8000
BLOCK_SIZE = 8

def generate_des_key():
    """Génère une clé secrète DES aléatoire."""
    return os.urandom(8)

def handle_server(client_sock,des_key):
    while True:
        #print(f"receiving")
        encrypted_message = receive_data(client_sock)
        #print(f"good")
        encrypted_digest = receive_data(client_sock)
        #print(f"cool")



        if not encrypted_message or not encrypted_digest:
            print("Connexion fermée par le client.")
            break

        try:
            decrypted_message = decrypt_des_ecb(encrypted_message, des_key)
            decrypted_digest = decrypt_des_ecb(encrypted_digest, des_key)
            # Vérification du digest
            hash_obj = SHA256.new(data=decrypted_message)
            calculated_digest = hash_obj.digest()

            if calculated_digest == decrypted_digest:
                print("🚀zheghost [*]:", decrypted_message.decode('utf-8'),"<--")
            else:
                print("authentication failure")

        except Exception as e:
            print(f"Erreur de déchiffrement : {e}")
            break

def encrypt_with_des(message, des_key):
    """Chiffre un message avec la clé DES."""
    cipher = DES.new(des_key, DES.MODE_ECB)
    return cipher.encrypt(pad(message, BLOCK_SIZE))

def encrypt_des_key(des_key, public_key):
    """Chiffre la clé DES avec la clé publique."""
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(des_key)

def decrypt_des_ecb(ciphertext, des_key):
    cipher = DES.new(des_key, DES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

def send_data(client_sock, data):
    """Envoie la taille des données suivie des données elles-mêmes."""
    data_length = len(data)
    client_sock.sendall(struct.pack('!I', data_length))  # Envoi de la taille
    client_sock.sendall(data)  # Envoi des données
def receive_data(client_sock):
    """Reçoit les données en fonction de la taille envoyée."""
    data_length_bytes = client_sock.recv(4)  # Taille de 4 octets pour un entier
    data_length = struct.unpack('!I', data_length_bytes)[0]  # Conversion de bytes à int
    data = b""
    while len(data) < data_length:
        packet = client_sock.recv(data_length - len(data))
        if not packet:
            break
        data += packet
    return data

def send_messages(client_sock, des_key):
    """Envoie continuellement des messages au serveur."""
    while True:
        message = input()
        if message.lower() == 'exit':
            break

        message_bytes = message.encode('utf-8')
        encrypted_message = encrypt_with_des(message_bytes, des_key)

        # Calcul et chiffrement du digest
        hash_obj = SHA256.new(data=message_bytes)
        digest = hash_obj.digest()
        encrypted_digest = encrypt_with_des(digest, des_key)

        # Envoi du message et du digest chiffrés
        send_data(client_sock,encrypted_message)
        send_data(client_sock,encrypted_digest)
        #print("Message et digest envoyés.")

def main():
    # Connexion au serveur
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((server_ip, server_port))
        print("Connecté au serveur.")
        welcome=client_sock.recv(1024)
        print(welcome.decode())
        # Réception de la clé publique du serveur
        public_key_data = client_sock.recv(2048)  # Réception de la clé publique
        public_key = RSA.import_key(public_key_data)
        print("Clé publique du serveur reçue.")

        # Génération de la clé secrète DES
        des_key = generate_des_key()
        print("Clé secrète DES générée :", des_key.hex())

        # Chiffrement de la clé secrète DES avec la clé publique du serveur
        encrypted_des_key = encrypt_des_key(des_key, public_key)
        #print(len(encrypted_des_key),encrypted_des_key.hex())
        client_sock.sendall(encrypted_des_key)
        print("Clé secrète DES envoyée au serveur.")
        server_thread = threading.Thread(target=handle_server, args=(client_sock,des_key))
        server_thread.start()
        # Envoi de messages
        send_messages(client_sock, des_key)

    print("Déconnexion du serveur.")

if __name__ == "__main__":
    main()