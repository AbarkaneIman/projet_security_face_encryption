import face_recognition
<<<<<<< HEAD

def get_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) > 0:
        encoding = face_recognition.face_encodings(image, face_locations)[0]
        return encoding
    else:
        return None
=======
from screens.encryption import encrypt_data, decrypt_data, load_aes_key

key = load_aes_key()

def get_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        return None
    return encodings[0]

def save_encrypted_encoding(encoding, filename):
    data = encoding.tobytes()  # تحويل numpy array ل bytes
    encrypted_data = encrypt_data(data, key)
    with open(filename, "wb") as f:
        f.write(encrypted_data)
    print(f"🔒 Empreinte faciale chiffrée enregistrée : {filename}")

def load_decrypted_encoding(filename):
    with open(filename, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_data(encrypted_data, key)
    # نرجعو numpy array من bytes
    import numpy as np
    encoding = np.frombuffer(decrypted_data, dtype=float)
    return encoding

def compare_faces(known_encoding, unknown_encoding):
    # face_recognition.compare_faces expects a list of known encodings
    results = face_recognition.compare_faces([known_encoding], unknown_encoding)
    return results[0]
>>>>>>> a0790628e0c1cc7c660e0558170990d5bfaadcc4
