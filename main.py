from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.properties import StringProperty
import webbrowser, requests, os

try:
    from kivymd.app import MDApp
    from kivymd.uix.tab import MDTabsBase
    from kivymd.uix.boxlayout import MDBoxLayout
    KIVYMD=True
except Exception:
    from kivy.app import App as MDApp
    from kivy.uix.boxlayout import BoxLayout as MDBoxLayout
    KIVYMD=False

KV = r"""
MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Keystone RapidAlphaX"
        md_bg_color: app.theme_cls.primary_color

    MDTabs:
        id: tabs

        Tab:
            title: "Dashboard"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: app.status_text

        Tab:
            title: "Signals"
            MDBoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                padding: "16dp"
                MDTextField:
                    id: symbol
                    hint_text: "Symbol (BTC/USDT)"
                    text: "BTC/USDT"
                MDRaisedButton:
                    text: "Get Signal"
                    on_release: app.get_signal(symbol.text)
                MDLabel:
                    id: result
                    text: "…"

        Tab:
            title: "Vault"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Locked / unlocked bots appear here"

        Tab:
            title: "School"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Keystone Overlord School videos / content"

        Tab:
            title: "Library"
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Metal Book Library viewer"

        Tab:
            title: "Buy"
            MDBoxLayout:
                orientation: "vertical"
                MDRaisedButton:
                    text: "Open Stripe Checkout"
                    on_release: app.open_checkout()
"""

class KeystoneApp(MDApp):
    status_text = StringProperty("Connecting…")
    api_base = os.getenv("API_BASE","http://10.0.2.2:8000")
    stripe_link = os.getenv("STRIPE_CHECKOUT_LINK","https://buy.stripe.com/eVqbJ17GnclE7ZAb2ubII04")

    def build(self):
        if KIVYMD:
            self.theme_cls.primary_palette = "BlueGray"
            self.theme_cls.theme_style = "Dark"
        root = Builder.load_string(KV)
        Clock.schedule_once(lambda *_: self.check_health(),1)
        return root

    def check_health(self):
        try:
            r=requests.get(self.api_base+"/",timeout=5)
            self.status_text="API OK" if r.ok else f"API {r.status_code}"
        except Exception as e:
            self.status_text=f"API error: {e}"

    def open_checkout(self):
        webbrowser.open(self.stripe_link)

    def get_signal(self,sym):
        try:
            r=requests.get(f"{self.api_base}/finetune",params={"symbol":sym,"n":500,"test_fr":0.2},timeout=15)
            self.root.ids.result.text=r.text if r.ok else f"HTTP {r.status_code}: {r.text}"
        except Exception as e:
            self.root.ids.result.text=f"Error: {e}"

KeystoneApp().run()
