import subprocess
import sys

def check_updates():
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list", "--outdated"], capture_output=True, text=True)
        outdated = []
        for line in result.stdout.splitlines()[2:]:
            if line:
                package = line.split()[0]
                if package in ["textual", "pillow", "pyfiglet"]:
                    outdated.append(package)
        if outdated:
            return f"[bold yellow]⚠ Обновления доступны: {' '.join(outdated)}[/bold yellow]\n[italic]Запустите: pip install --upgrade textual pillow pyfiglet[/italic]"
        return None
    except:
        return None
