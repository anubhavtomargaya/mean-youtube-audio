# sudo apt-get install libasound2-dev
# pip install pyalsaaudio
# from pyalsaaudio
import alsaaudio
mixer = alsaaudio.Mixer()
def control_volume(volume:str,step_size:int,mute:bool=False):
    value = mixer.getvolume()[0]
    
    if value > 100:
        value = 100
    mixer.setvolume(volume)
    value = mixer.getvolume()[0]
    return value