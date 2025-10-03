"""config.py
This file is for initialize flask app and configuration file
"""

from flask import Flask
from flask_cors import CORS
import os, sys
import yaml

VERSION = "2.0"
NAME = f"WinVol-Network v.{VERSION}"


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):  # PyInstaller exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_exe_dir():
    if getattr(sys, "frozen", False):  # Running as EXE
        return os.path.dirname(sys.executable)
    else:  # Running as script
        return os.path.dirname(os.path.abspath(__file__))


def initialize_config_file():
    config_path = os.path.join(get_exe_dir(), "config.yaml")
    if not os.path.exists(config_path):
        # Create default one if file does not exist.
        with open(config_path, "w") as f:
            f.write("port: 5001")
    return config_path


template_folder = resource_path("templates")
static_folder = resource_path("static")


# instantiate the app
flaskapp = Flask(NAME, template_folder=template_folder, static_folder=static_folder)
flaskapp.config.from_object(__name__)

# enable CORS
CORS(flaskapp, resources={r"/*": {"origins": "*"}})


# Open the YAML file in read mode
config_path = initialize_config_file()
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

import app
