import screen_brightness_control as sbc
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Audio settings using PyCaw to control system volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

def set_volume(value):
    """Sets the system volume."""
    volume.SetMasterVolumeLevelScalar(value / 100, None)

def set_brightness(value):
    """Sets the screen brightness."""
    sbc.set_brightness(int(value))
