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
