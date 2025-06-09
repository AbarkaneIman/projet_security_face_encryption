from kivy.lang import Builder
from kivymd.app import MDApp
from screens.HomeScreen import HomeScreen
from screens.WelcomeScreen import WelcomeScreen  # ✅ chemin corrigé
from screens.SignUp import SignUp  # ✅ chemin corrigé
from screens.LoginScreen import LoginScreen  # ✅ chemin corrigé
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

Window.size = (340, 620)  # Pour test sur PC

from kivy.core.text import LabelBase

LabelBase.register(
    name="EduQLDHand",
    fn_regular="assets/fonts/EduQLDHand-VariableFont_wght.ttf"
)


class MyApp(MDApp):
    def build(self):
        # Builder.load_file("screens/signup.kv")  # ✅ Charger le fichier KV
        # return SignUp()
    
        Builder.load_file("screens/welcomescreen.kv")
        Builder.load_file("screens/loginscreen.kv")  # si tu as aussi un fichier KV pour LoginScreen
        Builder.load_file("screens/signup.kv")
        Builder.load_file("screens/HomeScreen.kv")
        
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignUp(name="signup"))
        sm.add_widget(HomeScreen(name="home"))
        return sm

if __name__ == '__main__':
    MyApp().run()

