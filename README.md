# AlgoRythm
**AlgoRythm is a real-time audio visualizer with customizable features and Windows media integration to graphically display information about audio levels and media.**

Made using Python while utilizing performant programming techniques.

_CIS4930 - Performant Programming with Python - Summer 2021_

## Project Resources

Outline: https://docs.google.com/document/d/1MjfzGPgUQ3EDTRZ4OSIiPHjVnTdgo9IleFzqqXE-JPo

TestPyPI link: https://test.pypi.org/project/algorythm/

Project Repository link: https://github.com/cburrows1/AlgoRythm

## Installation instructions
- Install Python 3.8 or Later
- Manually install pyaudio (see section below)
- If on Windows enable Stereo mix: (other OS support coming soon)
  - Control panel -> Hardware and Sound -> Sound -> Recording -> Stereo Mix -> \*Right Click\* Enable
- If Stereo Mix does not appear under recording devices, user must download the device from RealTek. Link to download support video: https://youtu.be/Bd3moKLV5sE
- Download the wheel package from our release list
- Navigate to the directory where you just downloaded the package and install with `pip install <filename>.whl`

### PyAudio Installation Instructions
- Open a terminal window as administrator
- Install pipwin and pyaudio with:
```
pip install pipwin
pipwin install pyaudio
```

## Execution of program
- Run with `py -m algorythm`
- Changes to settings are saved to a file, _algorythm_settings_, in the main project directory.
- If no bars appear, even with Stereo Mix enabled, a USB DAC or audio device is likely interfering and bypassing RealTek. Unplug that device and connect to AUX instead.

