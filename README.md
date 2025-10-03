# Remote Windows Volume Control

<p align="center">
  <img src=".media/logo.webp" alt="Project's Logo"/>
</p>

This program lets you remotely control your Windows PC’s audio volume from any device on the same network.

<sup><sub>_Now, I don't need to get out of bed just to decrease the volume. 💤_</sub></sup>

### Demo

![Screenshot](.media/Screenshot.webp)

![Recording](.media/record.gif)

### Installation

#### Run as python file
1. Clone or download this repository
2. Run _setup.bat_ to install virtual environtment and install dependencies. _(or do it manually)_
3. Run _run.bat_ to run the program.

#### Run as .exe
Go to release page and download .exe and install as normal program.

#### Build your own .exe
1. Clone or download this repository
2. Run _setup.bat_ to install virtual environtment and install dependencies. _(or do it manually)_
3. Open terminal and use this
`
pyinstaller --onefile --noconsole --icon=icon.ico --name="Remote Windows Volume Control v.1.9" --clean --upx-dir C:\upx-5.0.2-win64 main.py
`

### License

Remote Windows Volume Control is released under the [MIT license](./LICENSE).
