# Remote Windows Volume Control

This web app allows you to control the audio volume of your Windows PC through other devices on the same network.
Now, I don't need to get out of bed just to decrease the volume.

![Screenshot](.media/Screenshot.png)

![Recording](.media/record.gif)

## How To Use

1. Fork/Clone
1. Open folder in cmd and do this command to install server-side Flask app:

    ```sh
    remote-windows-volume-control> cd server
    remote-windows-volume-control> python3 -m venv .venv
    remote-windows-volume-control> .venv\Scripts\activate
    (.venv) remote-windows-volume-control> pip install -r requirements.txt
    ```

1. Open client/src/App.vue file and change path to your IPv4 Address. (type ipconfig in cmd to check IPv4 Address)
1. Open another cmd and do this command to install client-side Vue app:

    ```sh
    remote-windows-volume-control>  cd client
    remote-windows-volume-control>  npm install
    remote-windows-volume-control>  npm run dev
    ```
    Navigate to [http://your-IPv4-Address:5173](http://your-IPv4-Address:5173) for dev build.

1. If app working as intended:

    ```sh
    remote-windows-volume-control> npm run build
    remote-windows-volume-control> npm run preview
    ```

    Navigate to [http://your-IPv4-Address:4173](http://your-IPv4-Address:4173) for preview build.

