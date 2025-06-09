import datetime
import cv2
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRoundFlatButton

class HomeScreen(MDScreen):
    def open_camera(self):
        # Ouvrir la caméra (webcam)
        self.capture = cv2.VideoCapture(0)

        # Créer un widget Image pour afficher le flux vidéo
        self.img_widget = Image()
        self.ids.camera_box.clear_widgets()
        self.ids.camera_box.height = "400dp"
        self.ids.camera_box.add_widget(self.img_widget)

        # Créer les boutons "Capturer" et "Fermer"
        controls = BoxLayout(size_hint_y=None, height="50dp", spacing=10, padding=10)
        capture_btn = MDRoundFlatButton(text=" Capturer", on_release=lambda x: self.capture_image())
        close_btn = MDRoundFlatButton(text=" Fermer", on_release=lambda x: self.close_camera())
        controls.add_widget(capture_btn)
        controls.add_widget(close_btn)
        self.ids.camera_box.add_widget(controls)

        # Lancer la mise à jour de l'image en continu (30 images/sec)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        # Lire une image depuis la caméra
        ret, frame = self.capture.read()
        if ret:
            # Retourner l'image verticalement (effet miroir)
            frame = cv2.flip(frame, -1)

            # Convertir l'image en format Texture pour Kivy
            buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.img_widget.texture = texture
        else:
            print("⚠️ Erreur lors de la capture de l'image.")

    def capture_image(self):
        # Prendre une photo et l’enregistrer avec un nom unique
        ret, frame = self.capture.read()
        if ret:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captured_{timestamp}.png"
            cv2.imwrite(filename, frame)
            print(f"✅ Image enregistrée : {filename}")

    def close_camera(self):
        # Fermer la caméra proprement
        if hasattr(self, 'capture'):
            self.capture.release()
            Clock.unschedule(self.update)
            self.ids.camera_box.clear_widgets()
            self.ids.camera_box.height = 0
            print("📷 Caméra fermée.")

    def set_user_info(self, nom, prenom):
        self.ids.welcome_label.text = f"Bienvenue {prenom} {nom} !"
