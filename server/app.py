import pythoncom
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from flask import Flask, jsonify, request
from flask_cors import CORS


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


def set_volume(process_name, volume):
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == process_name:
            volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume_interface.SetMasterVolume(volume, None)


@app.route('/audio', methods=['GET', 'POST'])
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
            audio['name'] = session.Process.name()
            audio['volume'] = volume.GetMasterVolume()
            processes.append(audio)
            # You can also use volume.GetVolumeRange() to get the volume range
            # volumes.append((session.Process.name(), volume.GetVolumeRange()))

    # Request post mean volume changing
    if request.method == 'POST':
        post_data = request.get_json()
        set_volume(post_data['name'], float(post_data['volume'])) # Setting new volume
        # Renew the session
        for process in processes:
            if process['name'] == post_data['name']:
                process["volume"] = float(post_data['volume'])
        return jsonify(processes)
    else:
        return jsonify(processes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
