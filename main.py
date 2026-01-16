from pyfiglet import Figlet
from .app import REXTApp
from .screens import WelcomeScreen

# Баннер (переопределяем в WelcomeScreen для красоты)
figlet = Figlet(font="slant")
banner_text = figlet.renderText("REXT")

# Патчим баннер в WelcomeScreen (простой способ)
WelcomeScreen.compose = lambda self: [
    *list(WelcomeScreen.compose(self))[:1],  # Старый код, но заменяем первую Label
    Label("[bold red]" + banner_text + "[/bold red]", id="banner")
] + list(WelcomeScreen.compose(self))[1:]

if __name__ == "__main__":
    REXTApp().run()
