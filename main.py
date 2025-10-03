from threading import Thread
from PIL import Image
import app
import sys
import pystray
import webbrowser


def on_open(icon, item):
    webbrowser.open(f"http://{app.HOST}:{app.PORT}")


def on_exit(icon, item):
    icon.stop()
    sys.exit(0)


if __name__ == "__main__":
    Thread(target=app.run_prod_server, daemon=True).start()
    image = Image.open("icon.png")
    icon = pystray.Icon(
        app.NAME,
        image,
        menu=pystray.Menu(
            pystray.MenuItem("Open", on_open), pystray.MenuItem("Exit", on_exit)
        ),
    )
    print("Starting tray icon...")
    icon.run()
    print("Tray stopped!")

# pyinstaller --onefile --noconsole --add-data 'templates:templates' --add-data 'static:static' --icon=icon.ico --name="Remote Windows Volume Control v.1.9" --clean --upx-dir C:\upx-5.0.2-win64 main.py
# pyinstaller --onefile --add-data 'templates:templates' --add-data 'static:static' normal_flaskapp.py
