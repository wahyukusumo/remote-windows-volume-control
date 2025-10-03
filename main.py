"""main.py
This is the main file for executable
"""

from threading import Thread
from PIL import Image
import config
import app
import os, sys
import pystray
import webbrowser


def get_exe_dir():
    if getattr(sys, "frozen", False):  # Running as EXE
        return os.path.dirname(sys.executable)
    else:  # Running as script
        return os.path.dirname(os.path.abspath(__file__))


def on_open(icon, item):
    webbrowser.open(f"http://{app.HOST}:{config.config['port']}")


def on_config(icon, item):
    config_path = os.path.join(get_exe_dir(), "config.yaml")
    if not os.path.exists(config_path):
        # Create default one if file does not exist.
        with open(config_path, "w") as f:
            f.write("port: 5001")
    os.startfile(config_path)


def on_exit(icon, item):
    icon.stop()
    sys.exit(0)


if __name__ == "__main__":
    Thread(target=app.run_prod_server, daemon=True).start()
    image = Image.open("icon.png")
    icon = pystray.Icon(
        __name__,
        image,
        menu=pystray.Menu(
            pystray.MenuItem("Open", on_open),
            pystray.MenuItem("Edit configuration", on_config),
            pystray.MenuItem("Exit", on_exit),
        ),
    )
    icon.run()
