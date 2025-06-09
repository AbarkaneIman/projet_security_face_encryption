from kivymd.uix.screen import MDScreen
import re
from kivymd.toast import toast
import firebase_admin
from firebase_admin import credentials, firestore

# Charge le fichier JSON téléchargé (chemin relatif à ton script)
cred = credentials.Certificate("C:/Users/pc/Desktop/cyber_securite/projet_fin_module/faceencryption-firebase-adminsdk-fbsvc-e74221f523.json")

# Initialise Firebase Admin (à faire une seule fois dans toute l'application)
firebase_admin.initialize_app(cred)

# Crée une instance du client Firestore
db = firestore.client()

# Ensuite ton code qui utilise 'db' ici


db = firestore.client()

class SignUp(MDScreen):

    def is_valid_email(self, email):
        return email.endswith("@gmail.com")

    def is_strong_password(self, password):
        # Minimum 8 caractères, 1 majuscule, 1 minuscule, 1 chiffre, 1 caractère spécial
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

    def is_valid_name(self, name):
        return name.isalpha()

    def is_unique_cin(self, cin):
        users_ref = db.collection('utilisateurs')
        result = users_ref.where('cin', '==', cin).get()
        return len(result) == 0

    def sign_up(self):
        print("Sign Up button pressed")

        # Récupération des champs
        nom = self.ids.nom_field.text.strip()
        prenom = self.ids.prenom_field.text.strip()
        cin = self.ids.cin_field.text.strip()
        email = self.ids.email_signup_field.text.strip()
        password = self.ids.password_signup_field.text.strip()

        # Vérifier si tous les champs sont remplis
        if not all([nom, prenom, cin, email, password]):
            toast("Veuillez remplir tous les champs.")
            return

        # Vérification du nom et prénom
        if not self.is_valid_name(nom):
            toast("Le nom ne doit contenir que des lettres.")
            return

        if not self.is_valid_name(prenom):
            toast("Le prénom ne doit contenir que des lettres.")
            return

        # Vérification de l'email
        if not self.is_valid_email(email):
            toast("L'email doit se terminer par @gmail.com.")
            return

        # Vérification du mot de passe
        if not self.is_strong_password(password):
            toast("Mot de passe faible. Utilisez des majuscules, minuscules, chiffres et caractères spéciaux.")
            return

        # Vérification de l'unicité du CIN
        if not self.is_unique_cin(cin):
            toast("Ce CIN est déjà utilisé.")
            return

        # Tous les champs sont valides
        toast("Compte créé avec succès !")

        # → ici tu peux maintenant ajouter l'utilisateur à Firestore
        db.collection('utilisateurs').add({
            'nom': nom,
            'prenom': prenom,
            'cin': cin,
            'email': email,
            'password': password
        })

        print("Inscription réussie :", nom, prenom, cin, email)

        # ✅ Récupérer le screen 'home' et passer les infos
        home_screen = self.manager.get_screen('home')
        home_screen.set_user_info(nom, prenom)
        self.manager.current = 'home'  ## ✅ Rediriger vers l'écran d'accueil

    def on_text_click(self, *args):
        print("Texte cliqué !")
    
