from time import sleep
D_WIDTH = 128
D_HEIGHT = 64
class Game:
    def __init__(self, display, mother_led, controls):
        self.display = display
        self.mother_led = mother_led
        self.controls = controls
    def start():
         raise NotImplementedError("Please Implement this method")
        
class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)        
    def from_number(self, number):
        x = number%16
        y = (number-x)/16
    def to_number(self, x, y):
        return y*16+x
        
class SnakeGame(Game):
# display is splitted to 4x4 segments, that can hold part of snake or star
    def start(self):
        gameover = False
        snake = Snake(1, 4, 4)
        star = -1
        while not gameover:
            self.display.fill(1)
            snake.draw(self.display)
            gameover = snake.move(1,0)
            print(gameover)
            self.display.show()
            sleep(0.5)
        self.display.text('Game over!', 15, 15, 0)
        self.display.text('Score:'+str(snake.length), 15, 30, 0)
        self.display.show()
class Snake:
    def __init__(self, position, length, square_size):
        self.position = position
        self.length = length
        self.square_size = square_size
        self.path = []
        for i in range(length):
            self.path.append(Point(16-length/2+i,8))
    def move(self, speed_x, speed_y):
        new_part = Point(self.path[len(self.path)-1].x + 1, self.path[len(self.path)-1].y)
        gameover = new_part.x > 32 or new_part.x < 1 or new_part.y > 16 or new_part.y < 1 
        for i in range(len(self.path)-1):
            self.path[i] = self.path[i+1]
            if new_part.x == self.path[i].x and new_part.y == self.path[i].y:
                gameover = True
        self.path[len(self.path)-1] = new_part
        return gameover
    def draw(self, display):
        for part in self.path:
            display.fill_rect(part.x*4, part.y*4, 4, 4, 0)
            print('x:'+str(part.x)+' y:'+str(part.y))


