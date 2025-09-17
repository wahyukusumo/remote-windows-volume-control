import pythoncom
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from flask import Flask, request, render_template
from flask_cors import CORS

VERSION = 1.8

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


def get_master_volume() -> float:
    """Get current main audio output volume

    Returns:
        current volume in float
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    return volume.GetMasterVolumeLevelScalar()


def set_master_volume(volume: float) -> None:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = interface.QueryInterface(IAudioEndpointVolume)
    volume_interface.SetMasterVolumeLevelScalar(float(volume), None)


def set_program_volume(program_name: str, volume: float) -> None:
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == program_name:
            volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume_interface.SetMasterVolume(float(volume), None)


def get_programs_volume() -> dict:
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


@app.template_filter()
def percentify(value: float) -> int:
    return round(value * 100)


@app.route("/", methods=["GET", "POST"])
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
        return render_template("index.html", processes=processes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, use_reloader=True, debug=True)

    # print(get_master_volume())
    # set_master_volume(0.77)
    # print(get_master_volume())

    # programs = get_programs_volume()
    # for program in programs:
    #     print(f'{program['name']}: {percentify(program["volume"])}')
