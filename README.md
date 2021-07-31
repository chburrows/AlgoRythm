# AlgoRythm
**AlgoRythm is a real-time audio visualizer with customizable features and Windows media integration to graphically display information about audio levels and media.**

Made using Python while utilizing performant programming techniques.

_CIS4930 - Performant Programming with Python - UF Summer 2021_

## Project Resources

Outline: https://docs.google.com/document/d/1MjfzGPgUQ3EDTRZ4OSIiPHjVnTdgo9IleFzqqXE-JPo

TestPyPI link: https://test.pypi.org/project/algorythm/

Project Repository link: https://github.com/cburrows1/AlgoRythm

## Installation instructions
- Install Python 3.8 or Later
- Manually install pyaudio (see section below)
- On Windows enable Stereo mix (or skip this step and Algorythm will visualize your default input device):
  - Control panel -> Hardware and Sound -> Sound -> Recording -> Stereo Mix -> \*Right Click\* Enable
  - If Stereo Mix does not appear under recording devices, follow the Driver Installation Instructions below
- Run `pip install algorythm`
- OR
  - Download the latest wheel package from our [release list](https://github.com/cburrows1/AlgoRythm/releases)
  - Navigate to the downloaded package and install with `pip install <filename>.whl`

### PyAudio Installation Instructions
- Download PyAudio whl from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio corresponding to your python version
- Navigate to download directory
- Install it with ```pip install <filename>.whl```

### Realtek Stereo Mix Driver Installation Instructions
- Check that it isn't disabled by right clicking, then select "Show Disabled Devices"
- If it shows up, then enable it. Otherwise it is necessary to download the driver from Realtek:
- Download the driver executable (64 bit) from [Realtek](https://www.realtek.com/en/agree-to-download?downloadid=4842c7ef60f190fdf91711cf682f2192) or a [Much Faster Mirror](https://www.lo4d.com/get-file/realtek-high-definition-audio-driver/800c666f4ee6f0464099fbfb5ecba476/)
- Run the executable and follow the installation instructions
- Restart computer and continue with the Algorythm installation instructions above

## Execution of program
- Run with `python -m algorythm`
- Changes to settings are saved to a file, _algorythm_settings_, in the current working directory.
- If no bars appear, even with Stereo Mix enabled, a USB DAC or audio device is likely interfering and bypassing RealTek. Unplug that device and connect to AUX instead. Restart Algorythm.
