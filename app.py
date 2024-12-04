import pythoncom
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from flask import Flask, request, render_template
from flask_cors import CORS


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


def set_volume(process_name, volume):
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == process_name:
            volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume_interface.SetMasterVolume(volume, None)


@app.template_filter()
def map_range(value):
    inMin = 0.0
    inMax = 1.0
    outMin = 0
    outMax = 100
    calculate = (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
    return round(calculate)


@app.route("/", methods=["GET", "POST"])
def audio():
    # Initialize COM
    pythoncom.CoInitialize()
    # Get all session first
    processes = []
    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process:
            audio = {}
            audio["name"] = session.Process.name()
            audio["volume"] = volume.GetMasterVolume()

            # prevent duplicate
            if not [
                process for process in processes if process["name"] == audio["name"]
            ]:
                processes.append(audio)
            # You can also use volume.GetVolumeRange() to get the volume range
            # volumes.append((session.Process.name(), volume.GetVolumeRange()))

    if request.method == "POST":
        post_data = {"name": request.form["name"], "volume": request.form["volume"]}
        print(post_data)
        set_volume(post_data["name"], float(post_data["volume"]))  # Setting new volume
        # Renew the session
        process = next((p for p in processes if p["name"] == post_data["name"]), None)
        if process:
            process["volume"] = float(post_data["volume"])

        return str(map_range(float(post_data["volume"])))
    else:
        return render_template("index.html", processes=processes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, use_reloader=True, debug=True)
