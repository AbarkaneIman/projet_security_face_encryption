from kivymd.uix.screen import MDScreen

class SignUp(MDScreen):
    def sign_in(self):
        print("Sign In button pressed")
        # Ajoute ici la logique pour naviguer vers l'écran de connexion

    def sign_up(self):
        print("Sign Up button pressed")
        # Ajoute ici la logique pour naviguer vers l'écran d'inscription

    def on_text_click(self, *args):
        print("Texte cliqué !")


