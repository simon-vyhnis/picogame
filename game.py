from time import sleep, time_ns
import random
import framebuf
D_WIDTH = 128
D_HEIGHT = 64
class Game:
    def __init__(self, display, mother_led, controls, sound):
        self.display = display
        self.mother_led = mother_led
        self.controls = controls
        self.sound = sound
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
# display is splitted to 4x4 segments, that can hold part of the snake or an apple
    def start(self):
        #initialization
        gameover = False
        snake = Snake(1, 4, 4)
        apple = self.get_new_apple(snake)
        speed_x = 0
        speed_y = 1
        #gameloop
        while not gameover:
            if self.controls.button_up.value() and speed_x != 0:
                speed_x = 0
                speed_y = -1
            if self.controls.button_down.value() and speed_x != 0:
                speed_x = 0
                speed_y = 1
            if self.controls.button_right.value() and speed_y != 0:
                speed_y = 0
                speed_x = 1
            if self.controls.button_left.value() and speed_y != 0:
                speed_y = 0
                speed_x = -1
            gameover = snake.move(speed_x, speed_y, apple)
            #check if apple was eaten
            if(apple.x == snake.path[len(snake.path)-1].x and apple.y == snake.path[len(snake.path)-1].y):
               apple = self.get_new_apple(snake)
            self.display.fill(1)
            snake.draw(self.display)
            #drawing apple
            self.display.fill_rect(apple.x*4+1, apple.y*4, 2, 4, 0)
            self.display.fill_rect(apple.x*4, apple.y*4+1, 4, 2, 0)
            self.display.show()
            sleep(0.5)
        #end of game
        self.display.text('Game over!', 15, 15, 0)
        self.display.text('Score:'+str(snake.length-3), 15, 30, 0)
        self.display.show()
        sleep(3)
        
    def get_new_apple(self, snake):
        out_of_snake = False
        new_x = 0
        new_y = 0
        #generate new apple pos and check if it is out of snake
        while not out_of_snake:
            new_x = random.randint(0, int(D_WIDTH/4)-1)
            new_y = random.randint(0, int(D_HEIGHT/4)-1)
            out_of_snake = True
            for part in snake.path:
                if(part.x == new_x and part.y == new_y):
                    out_of_snake = False
        return Point(new_x, new_y)
        
class Snake:
    def __init__(self, position, length, square_size):
        self.position = position
        self.length = length
        self.square_size = square_size
        self.path = []
        #generate default parts of the snake
        for i in range(length):
            self.path.append(Point(16-length/2+i,8))
    def move(self, speed_x, speed_y, apple):
        gameover = False
        new_part = Point(self.path[len(self.path)-1].x + speed_x, self.path[len(self.path)-1].y + speed_y)
        #if the snake moved into an apple make it longer
        if(apple.x == new_part.x and apple.y == new_part.y):
            self.path.append(new_part)
            self.length += 1
        else:
            #check if the snake stays inside the screen
            gameover = new_part.x >= 32 or new_part.x < 0 or new_part.y >= 16 or new_part.y < 0
            #move every part of the snake by one position in the array
            for i in range(len(self.path)-1):
                self.path[i] = self.path[i+1]
                #check if the snake does not crash into itself
                if new_part.x == self.path[i].x and new_part.y == self.path[i].y:
                    gameover = True
            #add a new part of snake to the array
            self.path[len(self.path)-1] = new_part
        return gameover
    def draw(self, display):
        #draw every part of the snake from the array
        for part in self.path:
            display.fill_rect(part.x*4, part.y*4, 4, 4, 0)
            print('x:'+str(part.x)+' y:'+str(part.y))


class CarGame(Game):
    def start(self):
        car = Car(8, 12)
        road = Road(40)
        gameover = False
        score = 0
        #gameloop
        while not gameover:
            self.display.fill(1)
            road.draw(self.display)
            car.draw(self.display)
            self.display.show()
            sleep(0.05)
            road.move()
            car.move(self.controls)
            if car.pos.x <= road.vertices[48] or car.pos.x > road.vertices[48]+34:
                gameover = True
            score += 0.05
        self.display.fill_rect(12, 12, 90, 35, 1) 
        self.display.text('Game over!', 15, 15, 0)
        self.display.text('Score:'+str(round(score)), 15, 30, 0)
        self.display.show()
        sleep(3)
        
class Car:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = Point(60,48)
        self.direction = 0
    def move(self, controls):
        self.direction = 0
        if(controls.button_right.value()):
            self.direction = 1
        if(controls.button_left.value()):
            self.direction = -1
        self.pos.x += self.direction
        
    def draw(self, display):
        if self.direction == -1:
            self.draw_left(display)
        elif self.direction == 0:
            self.draw_straight(display)
        elif self.direction == 1:
            self.draw_right(display)
            
    def draw_straight(self, display):
        #car body
        display.fill_rect(self.pos.x+1, self.pos.y, 6, 12, 0)
        #rearview mirror
        display.pixel(self.pos.x, self.pos.y+3, 0)
        display.pixel(self.pos.x+7, self.pos.y+3, 0)
        #glasses
        display.fill_rect(self.pos.x+2, self.pos.y+3, 4, 2, 1)
        display.fill_rect(self.pos.x+2, self.pos.y+9, 4, 2, 1)
        
    def draw_left(self, display):
        #car body
        for i in range(5):
            display.line(self.pos.x+4-i, self.pos.y+i, self.pos.x+13-i, self.pos.y+9+i, 0)
        for i in range(4):
            display.line(self.pos.x+4-i, self.pos.y+1+i, self.pos.x+12-i, self.pos.y+9+i, 0)
        #rearview mirror
        display.pixel(self.pos.x+6, self.pos.y, 0)
        display.pixel(self.pos.x, self.pos.y+6, 0)
        #glasses
        display.line(self.pos.x+2, self.pos.y+5, self.pos.x+5, self.pos.y+2, 1)
        display.line(self.pos.x+3, self.pos.y+5, self.pos.x+5, self.pos.y+3, 1)
        display.line(self.pos.x+8, self.pos.y+10, self.pos.x+10, self.pos.y+8, 1)
       
    def draw_right(self, display):
        #car body
        for i in range(5):
            display.line(self.pos.x+i, self.pos.y+8+i, self.pos.x+8+i, self.pos.y+i, 0)
        for i in range(4):
            display.line(self.pos.x+1+i, self.pos.y+8+i, self.pos.x+8+i, self.pos.y+1+i, 0)
        #rearview mirror
        display.pixel(self.pos.x+6, self.pos.y, 0)
        display.pixel(self.pos.x+12, self.pos.y+6, 0)
        #glasses
        display.line(self.pos.x+7, self.pos.y+2, self.pos.x+10, self.pos.y+5, 1)
        display.line(self.pos.x+7, self.pos.y+3, self.pos.x+9, self.pos.y+5, 1)
        display.line(self.pos.x+2, self.pos.y+8, self.pos.x+4, self.pos.y+10, 1)
        
class Road:
    def __init__(self, width):
        self.width = width
        self.vertices = []
        self.lines = 0
        self.curve_direction = 0
        self.curve_length = 0
        self.update_curve()
        for i in range(64):
            self.vertices.append(44)
    def move(self):
        self.update_curve()
        for i in reversed(range(len(self.vertices))):
            self.vertices[i] = self.vertices[i-1]
        self.vertices[0] = self.vertices[1]+self.curve_direction
        if(self.vertices[0]<=0):
            self.vertices[0] = 0
        elif(self.vertices[0]>=(128-self.width)):
            self.vertices[0] = (128-self.width)
        self.lines += 1
        if(self.lines >= 10):
            self.lines = 0
    def update_curve(self):
        self.curve_length -= 1
        if(self.curve_length <= 0):
            self.curve_direction = random.randint(-1, 1)
            self.curve_length = random.randint(10,18)
    def draw(self, display):
        for i in range(len(self.vertices)):
            display.pixel(self.vertices[i], i, 0)
            display.pixel(self.vertices[i]+self.width, i, 0)
            if((i%10 > self.lines and i%10 < self.lines+5) or i%10 < self.lines-5):
                display.pixel(self.vertices[i]+int(self.width/2), i, 0)
                
class DinoGame(Game):
    def start(self):
        #initialization
        gameover = False
        dino = Dino(Point(8, 48))
        cactuses = [Cactus(128), Cactus(128+64)]
        ground = Ground(6)
        cloud1 = Cloud(10)
        cloud2 = Cloud(110)
        last_frame = time_ns()
        score = 1
        #gameloop
        while not gameover:
            #moving
            dino.move(self.controls)
            for i in range(len(cactuses)):
                if cactuses[i].move():
                    cactuses[i] = Cactus()
                    score += 1
                print("cactus x:" + str(cactuses[i].pos) + " dino x:"+str(dino.pos.x)+" y:"+str(dino.pos.y))
                if cactuses[i].pos-10 < dino.pos.x and cactuses[i].pos+5 > dino.pos.x and dino.pos.y > 38:
                    print("gameover")
                    gameover = True
                        
            ground.move()
            cloud1.move()
            cloud2.move()
            #drawing
            self.display.fill(0)
            ground.draw(self.display)
            cloud1.draw(self.display)
            cloud2.draw(self.display)
            dino.draw(self.display)
            for cactus in cactuses:
                cactus.draw(self.display)
            self.display.invert(1)
            self.display.show()
            #count fps
            print("fps: "+str(1000000000/(time_ns()-last_frame)))
            last_frame = time_ns()
            
        self.display.fill_rect(12, 12, 90, 35, 0) 
        self.display.text('Game over!', 15, 15, 1)
        self.display.text('Score:'+str(round(score)), 15, 30, 1)
        self.display.show()
        sleep(3)
            

class Cactus:        
    def __init__(self, pos=random.randint(128, 140)):
        self.design = 0#random.randint(0,2)
        self.pos = pos
        
    def move(self):
        self.pos = self.pos-1
        if(self.pos < -10):
            return True
        return False
    
    def draw(self, display):
        if(self.design == 0):
            display.fill_rect(self.pos+2, 48, 1, 10, 1)
            display.fill_rect(self.pos, 49, 1, 4, 1)
            display.fill_rect(self.pos+4, 50, 1, 3, 1)
            display.fill_rect(self.pos, 52, 5, 1, 1)

class Ground:
    def __init__(self, height):
        self.height = height
        self.state = 0
        
    def move(self):
        self.state += 1
        if self.state > 2:
            self.state = 0
            
    def draw(self, display):
        display.line(0, 64-self.height, 128, 64-self.height, 1)
        for y in range(self.height):
            for x in range(128):
                if (y+x+self.state)%3:
                    display.pixel(x, 64-y, 1)
            

class Dino:
    def __init__(self, pos):
        self.pos = pos
        self.jump = 0
        self.leg_state = 0
    
    def move(self, controls):
        #proccess jump
        if controls.button_up.value() and self.jump == 0:
            self.jump = 21
        elif self.jump > 11:
            self.pos.y -= round(((self.jump-10)*self.jump+20)/70)
            self.jump -= 0.5
        elif self.jump > 0:
            self.pos.y += round(((self.jump+10)*self.jump+20)/70)
            self.jump -= 0.5
        #update leg state 
        self.leg_state += 1
        if self.leg_state > 4:
            self.leg_state = 0
    
    def draw(self, display):
        fb = framebuf.FrameBuffer(bytearray(
            b'\x00\x30\x60\xe0\xf0\xff\xfd\x7f\x2f\x0e\x00\x00\x00\x00\x03\x00\x03\x00\x00\x00'),
            10, 10, framebuf.MONO_VLSB)
        display.blit(fb, self.pos.x, self.pos.y)
        #leg animation
        if self.jump == 0:
            if self.leg_state%4 == 0:
                display.pixel(self.pos.x+4, self.pos.y+9, 0)
            elif self.leg_state%2 == 0:
                display.pixel(self.pos.x+6, self.pos.y+9, 0)
                
class Cloud:
    def __init__(self, pos):
        self.pos = Point(pos, random.randint(1, 6))
        
    def move(self):
        self.pos.x -= 1
        if self.pos.x < -15:
            self.pos.x = 128
            self.pos.y = random.randint(1, 6)
        
    def draw(self, display):
        fb = framebuf.FrameBuffer(bytearray(
            b'\x60\xf0\x90\x98\xbe\x92\x83\x81\x83\x8e\x98\x8c\x84\xdc\x70'),
            15, 8, framebuf.MONO_VLSB)
        display.blit(fb, self.pos.x, self.pos.y)
        

