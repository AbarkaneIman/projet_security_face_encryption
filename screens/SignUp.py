from kivymd.uix.screen import MDScreen
import re
from kivymd.toast import toast
import firebase_admin
from firebase_admin import credentials, firestore
import firebase_admin
from firebase_admin import credentials, storage


# Initialise Firebase Admin (une seule fois)
cred = credentials.Certificate(
    r"C:/Users/pc/Desktop/cyber_securite/projet_fin_module/faceencryption-firebase-adminsdk-fbsvc-b0016d8a90.json"
)
firebase_admin.initialize_app(cred)

# Client Firestore
db = firestore.client()


class SignUp(MDScreen):
    def is_valid_email(self, email):
        return email.endswith("@gmail.com")

    def is_strong_password(self, password):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return bool(re.match(pattern, password))

    def is_valid_name(self, name):
        return name.isalpha()

    def is_unique_cin(self, cin):
        users_ref = db.collection('utilisateurs')
        result = users_ref.where('cin', '==', cin).get()
        return len(result) == 0

    def sign_up(self):
        print("Sign Up button pressed")

        nom = self.ids.nom_field.text.strip()
        prenom = self.ids.prenom_field.text.strip()
        cin = self.ids.cin_field.text.strip()
        email = self.ids.email_signup_field.text.strip()
        password = self.ids.password_signup_field.text.strip()

        if not all([nom, prenom, cin, email, password]):
            toast("Veuillez remplir tous les champs.")
            return

        if not self.is_valid_name(nom):
            toast("Le nom ne doit contenir que des lettres.")
            return

        if not self.is_valid_name(prenom):
            toast("Le prénom ne doit contenir que des lettres.")
            return

        if not self.is_valid_email(email):
            toast("L'email doit se terminer par @gmail.com.")
            return

        if not self.is_strong_password(password):
            toast("Mot de passe faible. Utilisez majuscules, minuscules, chiffres et caractères spéciaux.")
            return

        if not self.is_unique_cin(cin):
            toast("Ce CIN est déjà utilisé.")
            return

        # Ajouter l'utilisateur à Firestore
        db.collection('utilisateurs').add({
            'nom': nom,
            'prenom': prenom,
            'cin': cin,
            'email': email,
            'password': password,
            'url_image_chiffree': ""
        })

        # Stocker les infos dans user_data
        # user_data.nom = nom
        # user_data.prenom = prenom
        # user_data.cin = cin

        toast("Compte créé avec succès !")
        self.go_to_home(nom, prenom, cin)

    def go_to_home(self, nom, prenom, cin):
        home_screen = self.manager.get_screen("home")
        home_screen.set_user_info(nom, prenom, cin)
        self.manager.current = "home"

    def on_text_click(self, *args):
        print("Texte cliqué !")
