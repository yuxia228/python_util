# python_utili

DIY python_utility 

## bat_icon.pyw

taskbar(task tray)にbatteryの残量をサークルアイコンで表示するためのプログラム

<details><summary>詳細</summary>

### Requirement

pip3 install wxPython psutil opencv-python numpy pathlib2

#### For Ubuntu

apt install -y libgtk2.0-dev libgtk-3-dev \
               libjpeg-dev libtiff-dev \
               libsdl1.2-dev libgstreamer-plugins-base0.10-dev \
               libnotify-dev freeglut3 freeglut3-dev libsm-dev \
               libwebkitgtk-dev libwebkitgtk-3.0-dev

- wxPython アイコン表示
- psutil バッテリ残量取得
- opencv-python バッテリアイコン画像の生成
- numpy opencvで使用
- pathlib2 wxPythonのコンパイルに使用？

### Test

- Windows 10 64bit Python version 3.7.3
- Ubuntu 16.04 Mate 

</details>


