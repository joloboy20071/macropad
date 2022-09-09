import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import analogio

print("---Pico Pad Keyboard---")


adc1 = analogio.AnalogIn(board.A2)
adc2 = analogio.AnalogIn(board.A1)
adc3 = analogio.AnalogIn(board.A0)

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

pins = (
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
)

MEDIA = 1
KEY = 2

keymap = {
    (0): (KEY, [Keycode.F13]),
    (1): (KEY, [Keycode.F16]),
    (2): (KEY, [Keycode.F19]),
    (3): (KEY, [Keycode.F14]),
    (4): (KEY, [Keycode.F17]),
    (5): (KEY, [Keycode.F20]),
    (6): (KEY, [Keycode.F15]),
    (7): (KEY, [Keycode.F18]),
    (8): (KEY, [Keycode.F21]),
    (9): (MEDIA, ConsumerControlCode.SCAN_PREVIOUS_TRACK),
    (10): (MEDIA, ConsumerControlCode.PLAY_PAUSE),
    (11): (MEDIA, ConsumerControlCode.SCAN_NEXT_TRACK),  # plus key
    
}

switches = []
for i in range(len(pins)):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)


switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while True:
    print(f"ADC1: {adc1.value}")
    print(f"ADC2: {adc2.value}")
    print(f"ADC3: {adc3.value}")
    
    time.sleep(0.04)
    
    for button in range(12):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                        print(keymap[button][1])
                    else:
                        cc.send(keymap[button][1])
                except ValueError:  # deals with six key limit
                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])

                except ValueError:
                    pass
                switch_state[button] = 0

    time.sleep(0.01) 

