import socket
import time
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, DES
from Cryptodome.Hash import SHA256
from Cryptodome.Util.Padding import pad


HOST = '127.0.0.1'
PORT = 65432
BLOCK_SIZE = 8

def encrypt_des_ecb(message, des_key):
    cipher = DES.new(des_key, DES.MODE_ECB)
    padded_message = pad(message, BLOCK_SIZE)  # Ajouter du padding
    return cipher.encrypt(padded_message)

def start_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            print(f"Connecté au serveur {HOST}:{PORT}")

            key = RSA.generate(2048)
            public_key = key.publickey()
            private_key = key

            time.sleep(2)  # Pause pour éviter d'envoyer trop vite
            client_socket.sendall(public_key.export_key())
            print("Clé publique envoyée.")

            encrypted_des_key = client_socket.recv(2048)
            rsa_cipher = PKCS1_OAEP.new(private_key)
            des_key = rsa_cipher.decrypt(encrypted_des_key)
            print("Clé DES reçue et déchiffrée.")

            while True:
                message = input("Entrez le message à envoyer (ou 'exit' pour quitter) :").lower().strip()

                if message == 'exit':
                    print("Fermeture de la connexion.")
                    break

                # Encryptage du message
                padded_message = pad(message.encode(), BLOCK_SIZE)
                print(f"ceci est le mesage : {message.encode()}")
                print(f"ceci est le padded_mesage : {padded_message}")
                encrypted_message = encrypt_des_ecb(padded_message, des_key)  # Chiffrer le message avec padding
                print(f"ceci est le message encrypeter : {encrypted_message}")



                # Creation du hash du message
                hash_obj = SHA256.new(data=message.encode())
                message_digest = hash_obj.digest()
                print(f"ceci est le message hasher digest : {message_digest}")
                encrypted_digest = encrypt_des_ecb(message_digest, des_key)
                print(f"Ceci est l'encrypter du message hasher : {encrypted_digest}")



                #Envoi du message encrypter
                client_socket.sendall(encrypted_message)
                 #Envoi du hash du message encrypter
                client_socket.sendall(encrypted_digest)
                print("Message et digest envoyés.")

                response = client_socket.recv(1024).decode()
                print(f"Réponse du serveur : {response}")

    except ConnectionResetError:
        print("La connexion avec le serveur a été fermée.")
    except Exception as e:
        print(f"Erreur sur le client : {e}")

if __name__ == "__main__":
    start_client()
