import os
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
    # 🎥 Ouvre la caméra par défaut (index 0)
    self.capture = cv2.VideoCapture(0)

    # 📦 Charge le classificateur en cascade de Haar pour la détection des visages
    self.face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    # 🖼️ Crée un widget Image Kivy pour afficher la vidéo
    self.img_widget = Image()
    
    # 🔄 Vide le conteneur camera_box pour ne pas empiler plusieurs widgets
    self.ids.camera_box.clear_widgets()
    
    # 📏 Définit la hauteur du conteneur pour l'image à 400dp
    self.ids.camera_box.height = "400dp"
    
    # ➕ Ajoute le widget d'image (où la vidéo sera affichée) au layout
    self.ids.camera_box.add_widget(self.img_widget)

    # 🎛️ Crée une rangée de boutons pour capturer et fermer la caméra
    controls = BoxLayout(size_hint_y=None, height="50dp", spacing=10, padding=10)

    # 🔘 Bouton pour capturer l'image, appelle capture_image() au clic
    capture_btn = MDRoundFlatButton(
        text="📸 Capturer", on_release=lambda x: self.capture_image())

    # 🔘 Bouton pour fermer la caméra, appelle close_camera() au clic
    close_btn = MDRoundFlatButton(
        text="Fermer", on_release=lambda x: self.close_camera())

    # ➕ Ajoute les deux boutons dans la boîte de contrôle
    controls.add_widget(capture_btn)
    controls.add_widget(close_btn)

    # ➕ Ajoute la boîte de contrôle sous le widget image dans le layout
    self.ids.camera_box.add_widget(controls)

    # 🔄 Démarre un timer pour actualiser l’image de la caméra 30 fois par seconde
    Clock.schedule_interval(self.update, 1.0 / 30.0)


    def update(self, dt):
    # 📸 Lire une image depuis la caméra (ret = succès, frame = image capturée)
        ret, frame = self.capture.read()
    
    # ✅ Si la capture est réussie
        if ret:
        # 🔄 Retourner verticalement l’image (car Kivy affiche l’image à l’envers)
            frame = cv2.flip(frame, 0)
        
        # 🌑 Convertir l’image couleur BGR en niveaux de gris (utile pour la détection de visages)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 🔍 Détecter les visages dans l’image en niveaux de gris
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,     # ➕ Zoom progressif pour la détection (plus petit = plus lent mais plus précis)
            minNeighbors=3,      # 📶 Filtre les faux positifs (plus grand = plus strict)
            minSize=(100, 100)   # 📏 Taille minimale d’un visage détecté
        )

        # 🟩 Dessiner un rectangle vert autour de chaque visage détecté
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 🎨 Convertir l’image en format RGB et en bytes pour l’afficher dans Kivy
        buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
        
        # 📦 Créer une texture Kivy à partir des dimensions de l’image
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        
        # 🖌️ Copier le buffer d’image dans la texture
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        
        # 🖼️ Mettre à jour le widget Image avec la nouvelle texture (donc la nouvelle frame)
        self.img_widget.texture = texture
    else:
        # ❌ Si la capture échoue, afficher un message d’erreur dans la console
        print("⚠️ Erreur lors de la capture de l'image.")

