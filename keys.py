from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Générer une clé privée RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Extraire la clé publique à partir de la clé privée
public_key = private_key.public_key()

# Sauvegarder la clé privée dans un fichier (au format PEM)
with open("private_key.pem", "wb") as priv_file:
    priv_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  # Pas de mot de passe pour la clé
        )
    )

# Sauvegarder la clé publique dans un fichier (au format PEM)
with open("public_key.pem", "wb") as pub_file:
    pub_file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Clés générées et sauvegardées dans 'private_key.pem' et 'public_key.pem'.")