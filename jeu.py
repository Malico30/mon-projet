from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import math

# Variables du jeu
money = 100
niventreprise1 = 0
jour = 0
addmoney = 100

# Fonctions de calcul
def calcul_cout(niveau):
    return round((niveau + 1) * addmoney + math.exp((niveau + 1)/5) * 100, 0)

def calcul_revenu(niveau):
    return 100 if niveau == 0 else round((niveau * addmoney) + (niveau * (addmoney / math.exp(niveau))), 0)

# Interface principale
class TycoonLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        # Labels
        self.label_jour = Label(text=f"📅 Jour : {jour}", font_size=24)
        self.label_money = Label(text=f"💰 Argent : {int(money)} $", font_size=24)
        self.label_niv = Label(text=f"🏢 Niveau entreprise : {niventreprise1}", font_size=24)
        self.label_prix = Label(text=f"💰 Prix : {int(calcul_cout(niventreprise1))}", font_size=24)
        self.label_revenu = Label(text=f"📈 Revenu quotidien : {int(calcul_revenu(niventreprise1))} $", font_size=20)
        self.label_message = Label(text="", color=(1,0,0,1), font_size=20)
        self.progress = ProgressBar(max=calcul_cout(niventreprise1), value=min(money, calcul_cout(niventreprise1)))

        # Bouton améliorer
        self.btn_upgrade = Button(text="Améliorer l'entreprise", size_hint=(1, 0.2))
        self.btn_upgrade.bind(on_press=self.ameliorer)

        # Ajout des widgets
        for w in [self.label_jour, self.label_money, self.label_niv, self.label_prix,
                  self.label_revenu, self.progress, self.label_message, self.btn_upgrade]:
            self.add_widget(w)

        # Lancement de l'automatisation des jours
        Clock.schedule_interval(self.jour_auto, 1)  # toutes les 10s

    def update_affichage(self):
        prix_suivant = int(calcul_cout(niventreprise1))
        revenu_jour = int(calcul_revenu(niventreprise1))

        self.label_jour.text = f"📅 Jour : {jour}"
        self.label_money.text = f"💰 Argent : {int(money)} $"
        self.label_niv.text = f"🏢 Niveau entreprise : {niventreprise1}"
        self.label_prix.text = f"💰 Prix : {prix_suivant}"
        self.label_revenu.text = f"📈 Revenu quotidien : {revenu_jour} $"
        self.progress.max = prix_suivant
        self.progress.value = min(money, prix_suivant)
        self.label_message.text = ""

    def ameliorer(self, instance):
        global money, niventreprise1, jour
        cout = calcul_cout(niventreprise1)
        if money >= cout:
            niventreprise1 += 1
            money -= cout
            jour += 1
            self.ajouter_revenu()
        else:
            self.label_message.text = f"❌ Pas assez d'argent pour {cout} $"
        self.update_affichage()

    def jour_auto(self, dt):
        global jour
        jour += 1
        self.ajouter_revenu()
        self.update_affichage()

    def ajouter_revenu(self):
        global money
        money += calcul_revenu(niventreprise1)

# Application
class TycoonApp(App):
    def build(self):
        return TycoonLayout()

if __name__ == "__main__":
    TycoonApp().run()
