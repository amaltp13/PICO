from oled_1inch3 import OLED_1inch3
from machine import Pin
import time

oled = OLED_1inch3()
keyA = Pin(15, Pin.IN, Pin.PULL_UP)
keyB = Pin(17, Pin.IN, Pin.PULL_UP)

while True:
    oled.fill(oled.black)  # clear once per loop
    if keyA.value() == 0:
        oled.text("Button A pressed", 0, 20, oled.white)
    if keyB.value() == 0:
        oled.text("Button B pressed", 0, 40, oled.white)
    oled.show()
    time.sleep(0.1)
