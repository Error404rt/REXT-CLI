from textual.widgets import Static, Button, Label, Checkbox, DirectoryTree
from textual.screen import Screen
from textual import on
from .utils import check_updates
from .generator import generate_zip

update_message = check_updates()

class WelcomeScreen(Static):
    def compose(self):
        yield Label("[bold red]REXT[/bold red]", id="banner")  # Упростил баннер, pyfiglet в main
        yield Label("--------------------------------------------------")
        if update_message:
            yield Label(update_message)
            yield Label("")
        yield Label("")
        yield Button("🚀 CUSTOM", id="custom_btn", variant="primary")

class AppSelectionScreen(Static):
    def compose(self):
        yield Label("[bold yellow]Выберите приложение:[/bold yellow]")
        apps = ["YouTube", "YouTube Music", "Reddit", "X (Twitter)", "Telegram", "Instagram"]
        for app in apps:
            yield Button(app, id=f"app_{app.lower().replace(' ', '_').replace('(', '').replace(')', '')}", variant="success")

    @on(Button.Pressed)
    def select_app(self, event):
        self.app.selected_app = event.button.label.plain
        self.app.push_screen(IconTypeSelectionScreen())

class IconTypeSelectionScreen(Static):
    def compose(self):
        yield Label(f"[bold yellow]Выбрано: {self.app.selected_app}[/bold yellow]")
        yield Label("[bold green]Выберите типы (клик/Enter для ✔️):[/bold green]")
        yield Checkbox("Icon ❌", value=False, id="icon_cb")
        yield Checkbox("Header ❌", value=False, id="header_cb")
        yield Checkbox("Notification ❌", value=False, id="notification_cb")
        yield Label("")
        yield Button("📷 SELECT PNG", id="png_btn", variant="primary")

    @on(Checkbox.Changed)
    def update_label(self, event):
        emoji = "✔️" if event.checkbox.value else "❌"
        event.checkbox.label = f"{event.checkbox.label.split()[0]} {emoji}"

    @on(Button.Pressed, "#png_btn")
    def go_to_picker(self):
        selected = []
        if self.query_one("#icon_cb").value: selected.append("icon")
        if self.query_one("#header_cb").value: selected.append("header")
        if self.query_one("#notification_cb").value: selected.append("notification")
        if not selected:
            self.app.bell()
            self.notify("Выберите хотя бы один тип! ❌", severity="error")
            return
        self.app.selected_types = selected
        self.app.push_screen(FileSelectionScreen())

class FileSelectionScreen(Screen):
    def compose(self):
        yield Label("[bold magenta]Выберите PNG (стрелки + Enter):[/bold magenta]")
        start_path = os.path.expanduser("~/storage/shared")
        yield DirectoryTree(start_path, id="tree")

    @on(DirectoryTree.FileSelected)
    def on_selected(self, event):
        if str(event.path).lower().endswith('.png'):
            self.app.selected_image = str(event.path)
            self.app.push_screen(ProcessingScreen())
        else:
            self.app.bell()
            self.notify("Только .PNG! ❌", severity="error")

class ProcessingScreen(Static):
    def compose(self):
        yield Label("[bold blue]Генерация ZIP... ⏳[/bold blue]")

    def on_mount(self):
        self.run_worker(generate_zip, self.app)

class SuccessScreen(Static):
    def compose(self):
        yield Label("[bold green]В вашем хранилище успешно создан .zip ✔️[/bold green]")
        yield Label(f"Файл: Download/{self.app.zip_path}")
        yield Label("")
        yield Label("[bold red]⚠ Инструкция по применению иконок ⚠[/bold red]")
        yield Label("Используйте MT Manager для удобства.")
        yield Label("В полученном файле все структуры есть — поочерёдно вставляйте в папку внутри APK (в res/)")
        yield Label("")
        yield Label(self.app.instruction)
        yield Label("")
        yield Button("Назад в меню", id="back", variant="warning")

    @on(Button.Pressed)
    def go_back(self):
        self.app.pop_screen(multiple=3)
