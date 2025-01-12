import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, DES
from Cryptodome.Hash import SHA256
from Cryptodome.Util.Padding import unpad

from confClient import BLOCK_SIZE

# Adresse du serveur
HOST = '127.0.0.1'
PORT = 65432

# Démarrage du serveur
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print("Serveur en attente de connexion...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connexion établie avec {addr}")

            # Étape 1 : Recevoir la clé publique RSA du client
            public_key_pem = conn.recv(2048)
            public_key = RSA.import_key(public_key_pem)
            print("Clé publique reçue.")

            # Générer une clé DES de 8 octets (64 bits)
            des_key = b"8BYTEDES"  # Clé DES (8 octets)
            des_cipher = DES.new(des_key, DES.MODE_ECB)

            # Chiffrer la clé DES avec la clé publique RSA
            rsa_cipher = PKCS1_OAEP.new(public_key)
            encrypted_des_key = rsa_cipher.encrypt(des_key)
            conn.sendall(encrypted_des_key)
            print("Clé DES chiffrée envoyée au client.")
            while True :
                
                # Étape 2 : Recevoir les messages chiffrés du client
                encrypted_message1 = conn.recv(1024)
                print(f"Message brute recu {encrypted_message1}")
                encrypted_message2 = conn.recv(1024)
                print("Messages chiffrés reçus.")



                # Déchiffrer le premier message avec DES
                decrypted_message1 = des_cipher.decrypt(encrypted_message1)
                print(f"message recu decrypter : {decrypted_message1}")
                message = unpad(decrypted_message1, BLOCK_SIZE)
                message = unpad(message, BLOCK_SIZE)
                print(f"Message : {message}")
                print(f"Message 1 déchiffré : {message.decode("utf-8")}")


                # Hasher le message déchiffré avec SHA-256
                hash_message = SHA256.new(message).digest()



                # Déchiffrer le second message (hash) avec DES
                hash_decrypted_message = des_cipher.decrypt(encrypted_message2)
                hash_decrypted_message = unpad(hash_decrypted_message, BLOCK_SIZE)
                print(f"hash decripter : {hash_decrypted_message}")



                # Comparer le hash du message 1 avec le message 2 déchiffré
                if hash_message == hash_decrypted_message :
                    response = "Bien reçu"
                else:
                    response = "Erreur d'intégrité"

                # Envoyer la réponse au client
                conn.sendall(response.encode())
                print(f"Réponse envoyée : {response}")

if __name__ == "__main__":
    start_server()
