from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual import on
from .screens import WelcomeScreen, AppSelectionScreen

class REXTApp(App):
    CSS = """
    Screen { align: center middle; }
    Button { width: 60; height: 7; margin: 2; }
    Checkbox { margin: 1 0; }
    """

    def __init__(self):
        super().__init__()
        self.selected_app = None
        self.selected_types = []
        self.selected_image = None
        self.zip_path = None
        self.instruction = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield WelcomeScreen()
        yield Footer()

    @on(Button.Pressed, "#custom_btn")
    def go_to_apps(self):
        self.push_screen(AppSelectionScreen())
