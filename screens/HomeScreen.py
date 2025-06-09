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
        # open camera
        self.capture = cv2.VideoCapture(0)

        # تحميل نموذج كشف الوجه
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # واجهة العرض
        self.img_widget = Image()
        self.ids.camera_box.clear_widgets()
        self.ids.camera_box.height = "400dp"
        self.ids.camera_box.add_widget(self.img_widget)

        # أزرار التحكم
        controls = BoxLayout(size_hint_y=None, height="50dp", spacing=10, padding=10)
        capture_btn = MDRoundFlatButton(
            text="📸 Capturer", on_release=lambda x: self.capture_image())
        close_btn = MDRoundFlatButton(
            text="Fermer", on_release=lambda x: self.close_camera())
        controls.add_widget(capture_btn)
        controls.add_widget(close_btn)
        self.ids.camera_box.add_widget(controls)

        # بدء التحديث المستمر للكاميرا
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        # قراءة الصورة من الكاميرا
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)  
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # كشف الوجه
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(100, 100)
            )

            # رسم مربعات على الوجوه
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # تحويل الصورة إلى Texture
            buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.img_widget.texture = texture
        else:
            print("⚠️ Erreur lors de la capture de l'image.")

    def capture_image(self):
     ret, frame = self.capture.read()
    if ret:
        frame = cv2.flip(frame, 1)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = "captures"
        os.makedirs(folder, exist_ok=True)
        image_path = os.path.join(folder, f"capture_{timestamp}.png")
        cv2.imwrite(image_path, frame)
        print(f"✅ Image enregistrée : {image_path}")

        # 🧠 Étape 1 : Extraire l'encodage du visage
        encoding = get_face_encoding(image_path)
        if encoding is not None:
            key = load_key()
            encrypted = encrypt_data(encoding.tobytes(), key)

            encrypted_path = os.path.join("captures", f"encoding_{timestamp}.enc")
            with open(encrypted_path, "wb") as f:
                f.write(encrypted)
            print(f"🔒 Empreinte faciale chiffrée enregistrée : {encrypted_path}")
        else:
            print("❌ Aucun visage détecté dans l'image.")
        
        # ✅ Retourne l'image capturée
        return frame
    else:
        print("⚠️ Erreur lors de la capture.")
        return None
    

    def encoder_image(self, image):
    if image is None:
        print("❌ Aucune image à encoder.")
        return

    # Enregistrer temporairement l'image pour traitement (ou faire l'encodage direct)
    temp_path = "captures/temp.png"
    cv2.imwrite(temp_path, image)

    encoding = get_face_encoding(temp_path)
    if encoding is not None:
        key = load_key()
        encrypted = encrypt_data(encoding.tobytes(), key)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        encrypted_path = os.path.join("captures", f"encoding_{timestamp}.enc")
        with open(encrypted_path, "wb") as f:
            f.write(encrypted)
        print(f"🔒 Encodage enregistré : {encrypted_path}")
    else:
        print("❌ Aucun visage détecté.")


    def close_camera(self):
        # إغلاق الكاميرا والتوقيف
        if hasattr(self, 'capture'):
            self.capture.release()
            Clock.unschedule(self.update)
            self.ids.camera_box.clear_widgets()
            self.ids.camera_box.height = 0
            print("📷 Caméra fermée.")

    def set_user_info(self, nom, prenom):
        self.ids.welcome_label.text = f"Bienvenue {prenom} {nom} !"
