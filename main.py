from kivy.lang import Builder
from kivymd.app import MDApp
from screens.WelcomeScreen import WelcomeScreen  # ✅ chemin corrigé
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
        Builder.load_file("screens/loginscreen.kv")  # ✅ Charger le fichier KV
        return LoginScreen()
    
        # Builder.load_file("screens/welcomescreen.kv")
        # Builder.load_file("screens/loginscreen.kv")  # si tu as aussi un fichier KV pour LoginScreen
        
        # sm = ScreenManager()
        # sm.add_widget(WelcomeScreen(name="welcome"))
        # sm.add_widget(LoginScreen(name="login"))
        # return sm

if __name__ == '__main__':
    MyApp().run()

