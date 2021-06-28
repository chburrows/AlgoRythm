# AlgoRythm
A real-time audio/music visualizer using Python and utilizing more performant techniques from Performant Programming with Python

Outline: https://docs.google.com/document/d/1MjfzGPgUQ3EDTRZ4OSIiPHjVnTdgo9IleFzqqXE-JPo

TestPyPI link: https://test.pypi.org/project/algorythm/0.1/

Project Repository link: https://github.com/cburrows1/AlgoRythm

## Installation instructions
- Required packages: pyaudio, numpy, scipy, pygame, pywin32
- Download PyAudio whl from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio corresponding to your python version
- install it with ```pip install <filename>.whl```
- If on windows enable Stereo mix: (other OS support coming soon)
  - Control panel -> Hardware and Sound -> Sound -> Recording -> Stereo Mix -> \*Right Click\* Enable
- If Stereo Mix does not appear under recording devices, user must download the device from RealTek. Link to download support video: https://youtu.be/Bd3moKLV5sE
- Download the wheel package from our release list
- Navigate to the directory where you just downloaded the package and install with `pip install <filename>.whl`
- Run with `py -m algorythm`