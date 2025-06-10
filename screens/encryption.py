<<<<<<< HEAD
from cryptography.fernet import Fernet
import os

# توليد المفتاح وحفظه في ملف
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("🔑 Clé Fernet générée et enregistrée dans 'secret.key'.")

# تحميل المفتاح من الملف
def load_key():
    if not os.path.exists("secret.key"):
        generate_key()
    with open("secret.key", "rb") as key_file:
        return key_file.read()

# تشفير البيانات
def encrypt_data(data, key=None):
    if key is None:
        key = load_key()
    f = Fernet(key)
    return f.encrypt(data)

# فك التشفير
def decrypt_data(token, key=None):
    if key is None:
        key = load_key()
    f = Fernet(key)
    return f.decrypt(token)
=======
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

KEY_PATH = "aes_key.key"

def generate_aes_key():
    key = os.urandom(32)  # 256 bits
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key

def load_aes_key():
    if not os.path.exists(KEY_PATH):
        return generate_aes_key()
    with open(KEY_PATH, "rb") as f:
        return f.read()

def encrypt_data(data: bytes, key: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    iv = encrypted_data[:16]
    actual_encrypted = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(actual_encrypted) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(decrypted_padded) + unpadder.finalize()
    return data
>>>>>>> a0790628e0c1cc7c660e0558170990d5bfaadcc4
