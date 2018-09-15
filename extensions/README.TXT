This directory contains various C extensions needed by EventGhost.

- cFunctions.pyd
    This extension contains different functions needed by the program core.

- _dxJoystick.pyd
    This extension is solely needed by the Joystick plugin to access the 
    hardware through Microsoft's Direct Input API.

- MceIr.dll
    This dll is used in the MceRemote plugin.

- RawInputHook.dll
    This dll is used in the RawInput plugin.

- TaskHook.dll
    This dll is used in the Task Monitor (Task) plugin

- WinUsbWrapper.dll
    This dll is used in the EventGhost core it is loaded in the Classes/WinUsb.py file

- VistaVolEvents.pyd
    This extension contains the various functions for handling sounds and sound related events when running Windows >= Vista 
