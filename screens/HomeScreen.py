import os
import datetime
import cv2
import numpy as np  # <-- Important !
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from screens.encryption import generate_key, load_key, encrypt_data, decrypt_data
from screens.face_utils import get_face_encoding
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class HomeScreen(MDScreen):
    def set_user_info(self, nom, prenom, cin):
        self.ids.welcome_label.text = f", {nom} {prenom} !"
        # self.ids.cin_label.text = f"CIN : {cin}"

    def open_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.img_widget = Image()
        self.ids.camera_box.clear_widgets()
        self.ids.camera_box.height = "400dp"
        self.ids.camera_box.add_widget(self.img_widget)

        controls = BoxLayout(size_hint_y=None, height="50dp", spacing=10, padding=10)
        capture_btn = MDRoundFlatButton(text="📸 Capturer", on_release=self.capture_image)
        close_btn = MDRoundFlatButton(text="Fermer", on_release=self.close_camera)
        controls.add_widget(capture_btn)
        controls.add_widget(close_btn)
        self.ids.camera_box.add_widget(controls)

        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(100, 100))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.img_widget.texture = texture
        else:
            print("⚠️ Erreur lors de la capture de l'image.")

    def _capture_image_and_return(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            folder = "captures"
            os.makedirs(folder, exist_ok=True)
            image_path = os.path.join(folder, f"capture_{timestamp}.png")
            cv2.imwrite(image_path, frame)
            print(f"✅ Image enregistrée : {image_path}")
            return frame
        else:
            print("⚠️ Impossible de capturer l'image.")
            return None

    def capture_image(self, *args):
        captured_frame = self._capture_image_and_return()
        if captured_frame is not None:
            # Convertir en matrice RGBA
            matrix_rgba = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2RGBA)
            self.captured_matrix = matrix_rgba
            print("Matrice RGBA:", matrix_rgba.shape)

            # Transformer la matrice RGBA en tableau d'entiers 32 bits
            int_array = self.rgba_matrix_to_int_array(matrix_rgba)
            self.captured_int_array = int_array
            print("Tableau d'entiers (pixels RGBA) :", len(int_array))

            # Affichage complet (attention si image grande !)
            # print(int_array)
        
            # Affichage partiel plus pratique
            print("100 premiers pixels entiers RGBA :", int_array[:100])            

            # Afficher l'image (optionnel)
            img_to_show = cv2.cvtColor(matrix_rgba, cv2.COLOR_RGBA2BGR)
            cv2.imshow("Image Capturée RGBA", img_to_show)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.captured_frame = captured_frame
        self.close_camera()
        if captured_frame is not None:
                # ... [code existant]
            data_chiffree, cle, iv = self.chiffrer_tableau_aes(int_array)
            image_chiffree_hex =  data_chiffree.hex()[:len(int_array)]
            print("🔐 Données chiffrées (hex) :",image_chiffree_hex, "...")
            # Enregistrer dans un fichier texte
            with open("image_chiffree.txt", "w") as f:
                f.write(image_chiffree_hex)
            print("🔑 Clé AES (hex)           :", cle.hex())
            print("🧭 IV (hex)                :", iv.hex())

    def rgba_matrix_to_int_array(self, matrix_rgba):
    
    # Transforme une matrice (H, W, 4) RGBA en un tableau 1D d'entiers 32 bits,
    # chaque pixel codé en : (R << 24) | (G << 16) | (B << 8) | A
    # 


    # S'assurer que le type est uint8
        rgba = matrix_rgba.astype(np.uint8)

    # Séparer les canaux (avec astype uint32 pour éviter overflow)
        R = rgba[:, :, 0].astype(np.uint32)
        G = rgba[:, :, 1].astype(np.uint32)
        B = rgba[:, :, 2].astype(np.uint32)
        A = rgba[:, :, 3].astype(np.uint32)

    # Combiner les canaux en un entier 32 bits
        int_matrix = (R << 24) | (G << 16) | (B << 8) | A

    # Retourner aplati en 1D
        return int_matrix.flatten()

    def close_camera(self, *args):
        if hasattr(self, 'capture') and self.capture.isOpened():
            if hasattr(self, 'event'):
                self.event.cancel()
            self.capture.release()
            self.ids.camera_box.clear_widgets()
            print("📷 Caméra fermée.")

    def image_to_matrix(self, frame, gray_scale=True):
        if gray_scale:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            return frame
        
 

    def chiffrer_tableau_aes(self, tableau_entiers):
        # Convertir chaque entier NumPy en int natif avant to_bytes
        data_bytes = b''.join(int(entier).to_bytes(4, byteorder='big') for entier in tableau_entiers)

    # Étape 2 : générer une clé et un IV
        cle = get_random_bytes(32)  # AES-256 => 32 octets
        iv = get_random_bytes(16)   # IV pour le mode CBC

    # Étape 3 : chiffrer
        cipher = AES.new(cle, AES.MODE_CBC, iv)
        data_chiffree = cipher.encrypt(pad(data_bytes, AES.block_size))

        return data_chiffree, cle, iv



    # Fonction de chiffrement AES CBC
    def chiffrer_message_aes(message: bytes, key: bytes = None):
        if key is None:
            key = get_random_bytes(16)  # Clé AES 128 bits

        iv = get_random_bytes(16)  # Vecteur d'initialisation
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(message, AES.block_size))
    
        return ciphertext, key, iv
    

    def sauvegarder_chiffrement(ciphertext, cin):
       filename = f"{cin}.txt"
       with open(filename, "wb") as f:
           f.write(ciphertext)
       return filename
    
    def uploader_fichier_vers_storage(path_local, nom_fichier):
       bucket = storage.bucket()
       blob = bucket.blob(f"images_chiffrees/{nom_fichier}")
       blob.upload_from_filename(path_local)
       blob.make_public()
       return blob.public_url


def on_leave(self):
    self.close_camera()
  

def close_camera(self, *args):
    if hasattr(self, 'capture') and self.capture.isOpened():
        Clock.unschedule(self.update)
        self.capture.release()
        self.ids.camera_box.clear_widgets()
        print("📷 Caméra fermée.")
