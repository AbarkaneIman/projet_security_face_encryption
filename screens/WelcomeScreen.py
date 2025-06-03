from kivymd.uix.screen import MDScreen

class WelcomeScreen(MDScreen):
    def sign_in(self):
        print("Sign In button pressed")
        # Ajoute ici la logique pour naviguer vers l'écran de connexion
        self.manager.current = "login"  # change l'écran vers LoginScreen

    def sign_up(self):
        print("Sign Up button pressed")
        # Ajoute ici la logique pour naviguer vers l'écran d'inscription
