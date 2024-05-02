from machine import I2C, Pin
from time import sleep
from controls import Controls
import ssd1306
from game import SnakeGame

mother_led = Pin(25, Pin.OUT)
mother_led.high()

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=200000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.poweron()
display.contrast(255)
display.fill(1)
display.text('Welcome to', 20, 10, 0)
display.text('picogame', 30, 30, 0)
display.show()
sleep(1)
mother_led.low()

#controls = Controls(1,2,15,1)
#menu = Menu(display, controls)
snakeGame = SnakeGame(display, mother_led, 0)
snakeGame.start()

#while True:
#controls.button_left.value() == 1:
#    game = menu.chooseGame()
#    game.start(display, mother_led, controls)