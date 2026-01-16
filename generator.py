import os
import shutil
import tempfile
from datetime import datetime
from PIL import Image, ImageDraw

DPI_SIZES = {
    'mdpi': 48,
    'hdpi': 72,
    'xhdpi': 96,
    'xxhdpi': 144,
    'xxxhdpi': 192,
}

def generate_zip(app_instance):
    img = Image.open(app_instance.selected_image).convert("RGBA")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_root = os.path.join(temp_dir, "REXT_pack")
        os.makedirs(zip_root)
        
        for typ in app_instance.selected_types:
            typ_dir = os.path.join(zip_root, typ)
            res_dir = os.path.join(typ_dir, "res")
            os.makedirs(res_dir)
            
            if typ == "icon":
                for dpi, size in DPI_SIZES.items():
                    mip_dir = os.path.join(res_dir, f"mipmap-{dpi}")
                    os.makedirs(mip_dir, exist_ok=True)
                    resized = img.resize((size, size), Image.LANCZOS)
                    resized.save(os.path.join(mip_dir, "ic_launcher.png"))
                    # Round
                    mask = Image.new("L", (size, size), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, size, size), fill=255)
                    round_img = Image.new("RGBA", (size, size), (0,0,0,0))
                    round_img.paste(resized, (0,0), mask)
                    round_img.save(os.path.join(mip_dir, "ic_launcher_round.png"))
            
            elif typ == "header":
                for dpi, size in DPI_SIZES.items():
                    draw_dir = os.path.join(res_dir, f"drawable-{dpi}")
                    os.makedirs(draw_dir, exist_ok=True)
                    resized = img.resize((size * 2, size), Image.LANCZOS)  # Шире для header
                    resized.save(os.path.join(draw_dir, "custom_header.png"))
            
            elif typ == "notification":
                for dpi, size in DPI_SIZES.items():
                    draw_dir = os.path.join(res_dir, f"drawable-{dpi}")
                    os.makedirs(draw_dir, exist_ok=True)
                    resized = img.resize((size, size), Image.LANCZOS)
                    resized.save(os.path.join(draw_dir, "ic_notification.png"))
                # Monochrome
                anydpi_dir = os.path.join(res_dir, "drawable-anydpi-v26")
                os.makedirs(anydpi_dir, exist_ok=True)
                gray = img.convert("L")
                mono = gray.point(lambda x: 0 if x < 128 else 255, "1")
                mono_img = Image.new("RGBA", img.size, (255,255,255,255))
                mono_img.putalpha(mono.convert("L"))
                mono_resized = mono_img.resize((192,192), Image.LANCZOS)
                mono_resized.save(os.path.join(anydpi_dir, "ic_notification_monochrome.png"))

        safe_app = app_instance.selected_app.replace(" ", "_").replace("(", "").replace(")", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        zip_name = f"{safe_app}_custom_{timestamp}.zip"
        download_path = os.path.expanduser("~/storage/shared/Download")
        os.makedirs(download_path, exist_ok=True)
        full_zip = os.path.join(download_path, zip_name)
        
        shutil.make_archive(zip_root, 'zip', zip_root)
        shutil.move(f"{zip_root}.zip", full_zip)
        
        app_instance.zip_path = zip_name
        
        # Инструкции
        base_instr = ("- Icon: замените в res/mipmap-*/ic_launcher*.png\n"
                      "- Header: замените custom_header.png в res/drawable-*\n"
                      "- Notification: замените ic_notification*.png в drawable-* и monochrome в anydpi-v26\n"
                      "MT Manager покажет оригиналы — заменяйте похожие по имени/размеру.")
        
        app_specific = {
            "YouTube": "YouTube/ReVanced: Header часто yt_branding или splash в drawable.",
            "YouTube Music": "YouTube Music: Аналогично YouTube.",
            "Reddit": "Reddit: Стандартно.",
            "X (Twitter)": "X: Notification часто stat_notify.",
            "Telegram": "Telegram: Стандартно.",
            "Instagram": "Instagram: Header/splash в drawable."
        }
        specific = app_specific.get(app_instance.selected_app, "")
        app_instance.instruction = f"{app_instance.selected_app}:\n{base_instr}\n{specific}" if specific else base_instr
