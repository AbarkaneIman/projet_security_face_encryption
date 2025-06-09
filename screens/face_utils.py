import face_recognition

def get_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    if face_locations:
        encoding = face_recognition.face_encodings(image, face_locations)[0]
        return encoding
    return None
