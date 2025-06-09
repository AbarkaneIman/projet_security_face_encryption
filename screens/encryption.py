from cryptography.fernet import Fernet
import os
KEY_PATH = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_PATH):
        generate_key()
    with open(KEY_PATH, "rb") as key_file:
        return key_file.read()

def encrypt_data(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(token: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(token)
