import socket
import threading
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad,pad
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import struct

# Configuration du serveur
server_ip = "0.0.0.0"
server_port = 65430
BLOCK_SIZE = 8
PRIVATE_KEY_PATH = "private_key.pem"
PUBLIC_KEY_PATH = "public_key.pem"

def decrypt_des_ecb(ciphertext, des_key):
    cipher = DES.new(des_key, DES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
def encrypt_with_des(message, des_key):
    """Chiffre un message avec la clÃƒÂ© DES."""
    cipher = DES.new(des_key, DES.MODE_ECB)
    return cipher.encrypt(pad(message, BLOCK_SIZE))

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        return RSA.import_key(key_file.read())
def send_data(client_sock, data):
    """Envoie la taille des donnÃƒÂ©es suivie des donnÃƒÂ©es elles-mÃƒÂªmes."""
    data_length = len(data)
    client_sock.sendall(struct.pack('!I', data_length))  # Envoi de la taille
    client_sock.sendall(data)  # Envoi des donnÃƒÂ©es


def receive_data(client_sock):
    """ReÃƒÂ§oit les donnÃƒÂ©es en fonction de la taille envoyÃƒÂ©e."""
    data_length_bytes = client_sock.recv(4)  # Taille de 4 octets pour un entier
    data_length = struct.unpack('!I', data_length_bytes)[0]  # Conversion de bytes Ãƒ  int
    data = b""
    while len(data) < data_length:
        packet = client_sock.recv(data_length - len(data))
        if not packet:
            break
        data += packet
    return data


def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        return RSA.import_key(key_file.read())

def handle_client(client_sock, client_address,des_key):
    """
    print(f"Connexion acceptÃƒÂ©e de {client_address}")

    # Envoi de la clÃƒÂ© publique
    public_key = load_public_key()
    client_sock.sendall(public_key.export_key())

    # RÃƒÂ©ception de la clÃƒÂ© secrÃƒÂ¨te chiffrÃƒÂ©e par la clÃƒÂ© publique
    encrypted_des_key = client_sock.recv(1024)
    cipher_rsa = PKCS1_OAEP.new(load_private_key())
    des_key = cipher_rsa.decrypt(encrypted_des_key)
    print("ClÃƒÂ© secrÃƒÂ¨te DES reÃƒÂ§ue :", des_key.hex())
"""
    while True:
        #print(f"receiving")
        encrypted_message = receive_data(client_sock)
        #print(f"good")
        encrypted_digest = receive_data(client_sock)
        #print(f"cool")



        if not encrypted_message or not encrypted_digest:
            print("Connexion fermÃƒÂ©e par le client.")
            break

        try:
            decrypted_message = decrypt_des_ecb(encrypted_message, des_key)
            decrypted_digest = decrypt_des_ecb(encrypted_digest, des_key)
            # VÃƒÂ©rification du digest
            hash_obj = SHA256.new(data=decrypted_message)
            calculated_digest = hash_obj.digest()

            if calculated_digest == decrypted_digest:
                print("Ã°Å¸Å¡â‚¬Error4013 [*]:", decrypted_message.decode('utf-8'),"<--")
            else:
                print("authentication failure")

        except Exception as e:
            print(f"Erreur de dÃƒÂ©chiffrement : {e}")
            break

    client_sock.close()
    print(f"Connexion fermÃƒÂ©e avec {client_address}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((server_ip, server_port))
        server_sock.listen()
        print(f"Serveur Ãƒ  l'ÃƒÂ©coute sur {server_ip}:{server_port}")

        while True:
            client_sock, client_address = server_sock.accept()
            print(f"Connexion acceptÃƒÂ©e de {client_address}")
            welcome="~~~~~~~~~coolest students of madam lazaar's pratical work~~~~~~~~"
            print(welcome)
            client_sock.sendall(welcome.encode('utf-8'))

    # Envoi de la clÃƒÂ© publique
            public_key = load_public_key()
            client_sock.sendall(public_key.export_key())

    # RÃƒÂ©ception de la clÃƒÂ© secrÃƒÂ¨te chiffrÃƒÂ©e par la clÃƒÂ© publique
            encrypted_des_key = client_sock.recv(1024)
            cipher_rsa = PKCS1_OAEP.new(load_private_key())
            des_key = cipher_rsa.decrypt(encrypted_des_key)
            print("ClÃƒÂ© secrÃƒÂ¨te DES reÃƒÂ§ue :", des_key.hex())

            client_thread = threading.Thread(target=handle_client, args=(client_sock, client_address,des_key))
            client_thread.start()
            while True:
                message=input()
                if message.lower() == 'exit':
                    break

                message_bytes =message.encode('utf-8')
                encrypted_message = encrypt_with_des(message_bytes, des_key)

        # Calcul et chiffrement du digest
                hash_obj = SHA256.new(data=message_bytes)
                digest = hash_obj.digest()
                encrypted_digest = encrypt_with_des(digest, des_key)

        # Envoi du message et du digest chiffrÃƒÂ©s
                send_data(client_sock,encrypted_message)
                send_data(client_sock,encrypted_digest)
            #print("Message et digest envoyÃƒÂ©s.")




if __name__ == "__main__":
    
    start_server()
