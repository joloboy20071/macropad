import serial
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import time
from config.macropad_config import ADC1, ADC2, ADC3

def spotify_sound(volume_num):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == ADC1:
             volume.SetMasterVolume(volume_num, None)

def discord_sound(volume_num):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == ADC2:
             volume.SetMasterVolume(volume_num, None)

def chrome_sound(volume_num):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == ADC3:
             volume.SetMasterVolume(volume_num, None)

def open_serial():
    ser = serial.Serial('COM7', 115200)
    if not ser.isOpen():
        ser.open()
    print('com7 is open', ser.isOpen())
    return ser

max = 65000

def ADC(ser):
    while 1:
        lines = ser.readline().decode("utf-8")
        
        if lines.startswith("ADC1:"):
            adc = lines.replace("ADC1:", " ")
            adc = int(adc)
            try:
                volume_num = (abs(adc - max) / max)
                
                if volume_num > 0.99:
                    volume_num = 1
                    spotify_sound(volume_num)
                    
                if volume_num < 0.0088:
                    volume_num = 0
                    spotify_sound(volume_num)
                    
                elif not volume_num < 0.0088 or volume_num >  0.99:
                    spotify_sound(volume_num)
                       
            except ZeroDivisionError:
                pass
                 
    

        if lines.startswith("ADC2:"):
                adc = lines.replace("ADC2:", " ")
                adc = int(adc)
                try:
                    volume_num = (abs(adc - max) / max)
                    
                    if volume_num > 0.99:
                        volume_num = 1
                        discord_sound(volume_num)
                        
                    if volume_num < 0.0088:
                        volume_num = 0
                        discord_sound(volume_num)

                    elif not volume_num < 0.0088 or volume_num >  0.99:
                        discord_sound(volume_num)
                        
                        
                except ZeroDivisionError:
                    pass

        if lines.startswith("ADC3:"):
                adc = lines.replace("ADC3:", " ")
                adc = int(adc)
                volume_num = (abs(adc - max) / max)
                try:
                    volume_num = (abs(adc - max) / max)
                    
                    if volume_num > 0.99:
                        volume_num = 1
                        chrome_sound(volume_num)
                        
                    if volume_num < 0.0088:
                        volume_num = 0
                        chrome_sound(volume_num)

                    elif not volume_num < 0.0088 or volume_num >  0.99:
                        chrome_sound(volume_num)
                        
                        
                except ZeroDivisionError:
                    pass
                  
def main():
    time.sleep(10)
    print("----- Pi board has loaded -----")
    ADC(open_serial())
main()

