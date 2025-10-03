"""main.py
This is the main file for executable and will run WSGI production server.
If you want to run dev server just change it in __main__.
"""

from threading import Thread
from PIL import Image
import config
import app
import os, sys
import pystray
import webbrowser


def on_open(icon, item):
    webbrowser.open(f"http://{app.HOST}:{config.config['port']}")


def on_config(icon, item):
    config_path = config.initialize_config_file()
    os.startfile(config_path)


def on_exit(icon, item):
    icon.stop()
    sys.exit(0)


if __name__ == "__main__":
    Thread(target=app.run_prod_server, daemon=True).start()  # For production server
    # Thread(target=app.run_dev_server, daemon=True).start() # For development server
    image = Image.open(config.resource_path("icon.png"))
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
