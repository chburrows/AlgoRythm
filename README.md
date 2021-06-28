# AlgoRythm
**AlgoRythm is a real-time audio visualizer with customizable features and Windows media integration to graphically display information about audio levels and media.**

Made using Python while utilizing performant programming techniques.

_CIS4930 - Performant Programming with Python - Summer 2021_

## Project Resources

Outline: https://docs.google.com/document/d/1MjfzGPgUQ3EDTRZ4OSIiPHjVnTdgo9IleFzqqXE-JPo

TestPyPI link: https://test.pypi.org/project/algorythm/0.1/

Project Repository link: https://github.com/cburrows1/AlgoRythm

## Installation instructions
- Required packages: pyaudio, numpy, scipy, pygame, pywin32
- Download PyAudio whl from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio corresponding to your python version
- install it with ```pip install <filename>.whl```
- If on Windows enable Stereo mix: (other OS support coming soon)
  - Control panel -> Hardware and Sound -> Sound -> Recording -> Stereo Mix -> \*Right Click\* Enable
- If Stereo Mix does not appear under recording devices, user must download the device from RealTek. Link to download support video: https://youtu.be/Bd3moKLV5sE
- If no bars appear, even with Stereo Mix enabled, a USB DAC or audio device is likely interfering and bypassing RealTek. Unplug that device and connect to AUX instead.

## Execution of program
- Run the program in Windows Powershell via ```python .\src\algorythm\graphics.py``` from the main project directory.
- Changes to settings are saved to a file, _algorythm_settings_, in the main project directory.
