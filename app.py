"""app.py
This file is for flask routes also function for changing volume
"""

import pythoncom
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from flask import request, render_template
import config

DEBUG = True
HOST = "0.0.0.0"
PORT = config.config["port"]
APP = config.flaskapp


def get_master_volume() -> float:
    """Get current main audio device volume
    return: current volume (float)
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    return volume.GetMasterVolumeLevelScalar()


def set_master_volume(volume: float) -> None:
    """Set main device audio volume
    args: volume (float)
    return: None
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = interface.QueryInterface(IAudioEndpointVolume)
    volume_interface.SetMasterVolumeLevelScalar(float(volume), None)


def set_program_volume(program_name: str, volume: float) -> None:
    """Change program volume by name
    args: program name (str), new volume (float)
    return: None
    """
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == program_name:
            volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume_interface.SetMasterVolume(float(volume), None)


def get_programs_volume() -> list:
    """Get list of volumes of active processes/programs.
    return: list of dictionary with key name & volume
    """
    programs = []
    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process:
            audio = {}
            audio["name"] = session.Process.name()
            audio["volume"] = volume.GetMasterVolume()

            # prevent duplicate
            if not [
                program
                for program in programs
                if program["name"] == session.Process.name()
            ]:
                programs.append(
                    {"name": session.Process.name(), "volume": volume.GetMasterVolume()}
                )
            # You can also use volume.GetVolumeRange() to get the volume range
            # volumes.append((session.Process.name(), volume.GetVolumeRange()))

    return programs


@APP.template_filter()
def percentify(value: float) -> int:
    return round(value * 100)


@APP.route("/", methods=["GET", "POST"])
def audio():
    pythoncom.CoInitialize()
    master_volume = [{"name": "Master", "volume": get_master_volume()}]
    programs = get_programs_volume()
    processes = master_volume + programs

    if request.method == "POST":
        program_name = request.form["name"]
        program_volume = float(request.form["volume"])

        if program_name == "Master":
            set_master_volume(program_volume)
        else:
            set_program_volume(program_name, program_volume)

        # Find current program object in processes list
        program = next((p for p in processes if p["name"] == program_name), None)

        # If program exist, replace old volume to new volume
        # This affect original processes since we use next() function
        if program:
            program["volume"] = program_volume

        return str(percentify(program_volume))
    else:
        return render_template(
            "index.html", processes=processes, version=config.VERSION
        )


def run_prod_server():
    from waitress import serve

    print(config.NAME)
    print(f"🚀 {config.NAME} is running at http://{HOST}:{PORT}")
    serve(APP, host=HOST, port=PORT)


def run_dev_server():
    APP.run(host=HOST, port=PORT, use_reloader=True, debug=DEBUG)


# if __name__ == "__main__":
#     run_prod_server()

# run_dev_server()

# print(get_master_volume())
# set_master_volume(0.77)
# print(get_master_volume())

# programs = get_programs_volume()
# for program in programs:
#     print(f'{program['name']}: {percentify(program["volume"])}')
