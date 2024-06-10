from machine import Pin
class Controls:
    def __init__(self, pin_up, pin_down, pin_left, pin_right):
        self.button_up = Pin(pin_up, Pin.IN, Pin.PULL_DOWN)
        self.button_down = Pin(pin_down, Pin.IN, Pin.PULL_DOWN)
        self.button_left = Pin(pin_left, Pin.IN, Pin.PULL_DOWN)
        self.button_right = Pin(pin_right, Pin.IN, Pin.PULL_DOWN)

