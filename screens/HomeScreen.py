import os
import datetime
import cv2
import numpy as np
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

class HomeScreen(MDScreen):
    def set_user_info(self, nom, prenom, cin):
        self.ids.welcome_label.text = f", {nom} {prenom} !"
        # self.ids.cin_label.text = f"CIN : {cin}"
        self.cin = cin  # Stocker dans l’instance

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

            # Affichage partiel plus pratique
            print("100 premiers pixels entiers RGBA :", int_array[:100])            

            # Afficher l'image (optionnel)
            img_to_show = cv2.cvtColor(matrix_rgba, cv2.COLOR_RGBA2BGR)
            cv2.imshow("Image Capturée RGBA", img_to_show)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Chiffrement AES
            data_chiffree, cle, iv = self.chiffrer_tableau_aes(int_array)
            image_chiffree_hex = data_chiffree.hex()[:len(int_array)]
            print("🔐 Données chiffrées (hex) :", image_chiffree_hex, "...")
            
            # Enregistrer dans un fichier texte
            chemin_fichier = self.sauvegarder_chiffrement_hex(data_chiffree,  self.cin)
            print(f"Données chiffrées sauvegardées dans : {chemin_fichier}")
            print("🔑 Clé AES (hex)           :", cle.hex())
            print("🧭 IV (hex)                :", iv.hex())

        self.captured_frame = captured_frame
        self.close_camera()

    def rgba_matrix_to_int_array(self, matrix_rgba):
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

    def chiffrer_tableau_aes(self, tableau_entiers):
        # Convertir chaque entier NumPy en int natif avant to_bytes
        data_bytes = b''.join(int(entier).to_bytes(4, byteorder='big') for entier in tableau_entiers)

        # Générer une clé et un IV
        cle = get_random_bytes(32)  # AES-256 => 32 octets
        iv = get_random_bytes(16)   # IV pour le mode CBC

        # Chiffrer
        cipher = AES.new(cle, AES.MODE_CBC, iv)
        data_chiffree = cipher.encrypt(pad(data_bytes, AES.block_size))
        
        return data_chiffree, cle, iv

    def sauvegarder_chiffrement_hex(self, data_chiffree, cin):
        filename = f"{cin}.txt"
        with open(filename, "w") as f:
            f.write(data_chiffree.hex())
        return filename

    def on_leave(self):
        self.close_camera()
