from machine import PWM, Pin
from time import sleep
class Sound:
    def __init__(self, pin):
        self.pin = pin
    def play_tone(self, freq, duration):
        self.start_tone(freq)
        sleep(duration)
        self.stop_tone()
    def start_tone(self, freq):
        self.buzzer = PWM(Pin(self.pin))
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(1000)
    def stop_tone(self):
        self.buzzer.duty_u16(1)
        self.buzzer = Pin(self.pin, Pin.IN)
        
        
        
