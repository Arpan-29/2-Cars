import pygame
from random import randint
from math import floor

pygame.init()

screenWidth = 400
screenHeight = 600
win = pygame.display.set_mode((screenWidth, screenHeight))

font = pygame.font.SysFont("Times New Roman", 50)

class Car :
    def __init__(self, x, y, color) :
        self.x = x
        self.y = y
        self.lane = 0

        self.width = 40
        self.height = 60
        self.color = color

    def changelane(self) :
        self.lane = 1 - self.lane

    def show(self) :
        x = floor(self.x + self.lane * screenWidth // 4)
        y = floor(self.y)

        pygame.draw.rect(win, self.color, (x, y, self.width, self.height))
        pygame.draw.rect(win, WHITE, (x, y, self.width, self.height), 2)

class Obstacle :
    def __init__(self, x, y, shape, color, speed) :
        self.x = x
        self.y = y
        self.speed = speed

        self.shape = shape
        self.color = color
        self.a = screenWidth // 20

        self.blink = False

    def update(self) :
        self.y += self.speed

    def end(self) :
        return self.y > screenHeight + 100 

    def collide(self, car) :
        x = car.x + car.lane * screenWidth // 4
        d = (self.x - x)**2 + (self.y - car.y)**2
        if self.shape == 0 :
            if d < (self.a)**2 + 2 * car.width :
                return True

        if self.shape == 1 :
            check = (self.y > car.y) and (self.y < (car.y + car.height)) and (self.x > x) and (self.x < (x + car.width))
            if d <= 1.5 * (self.a**2) or check : 
                return True

        return False

    def miss(self, car) :
        return self.y > car.y 

    def show(self) :
        if self.blink :
            pygame.time.delay(200)

            if self.color == LIGHT_RED :
                self.color = DARK_RED
            elif self.color == DARK_RED :
                self.color = LIGHT_RED            
            elif self.color == LIGHT_BLUE :
                self.color = DARK_BLUE
            else :
                self.color = LIGHT_BLUE

        if self.shape == 0 :
            x = floor(self.x)
            y = floor(self.y)
            rad = floor(self.a)

            pygame.draw.circle(win, self.color, (x, y), rad)
            pygame.draw.circle(win, WHITE, (x, y), (rad), 2)
        else :
            x = floor(self.x - self.a + 2)
            y = floor(self.y - self.a + 2)
            a = floor(2 * self.a - 4)

            pygame.draw.rect(win, self.color, (x, y, a, a))
            pygame.draw.rect(win, WHITE, (x, y, a, a), 2) 

WHITE = (255,255,255)
LIGHT_BLUE = (50, 200, 240)
LIGHT_RED = (255, 50, 50)
LINE_COLOR = (50, 50, 200)
BG_COLOR = (20, 20, 150) 
DARK_BLUE = (0, 0, 255)
DARK_RED = (150, 0, 0)

car1 = Car(screenWidth // 8 - 20, screenHeight - 150, LIGHT_RED)
car2 = Car(screenWidth // 8 + screenWidth // 2 - 20, screenHeight - 150, LIGHT_BLUE)

squares = []
circles = []
score = 0
stop = False
blink_index = -1
blink_shape = 0

def draw(stop, Lscore, Rscore, Llanecounter, Rlanecounter, blink_index, blink_shape) :
    pygame.draw.line(win, LINE_COLOR, (screenWidth // 4, 0), (screenWidth // 4, screenHeight), 2)
    pygame.draw.line(win, LINE_COLOR, (screenWidth // 2, 0), (screenWidth // 2, screenHeight), 4)
    pygame.draw.line(win, LINE_COLOR, (3 * screenWidth // 4, 0), (3 * screenWidth // 4, screenHeight), 2)

    for i in range(len(circles) - 1, -1, -1) :
        c = circles[i]
        if not stop :
            c.update()
        
        c.show()
        
        if c.end() :
            circles.pop(i)

        if c.collide(car1) :
            circles.pop(i)
            Lscore += 1
        
        if c.collide(car2) :
            circles.pop(i)
            Rscore += 1

        if c.miss(car1) or c.miss(car2):
            stop = True
            blink_index = i
            blink_shape = 0

        if blink_index == i and c.shape == blink_shape :
            c.blink = True

    for i in range(len(squares) - 1, -1, -1) :
        s = squares[i]
        
        if not stop :
            s.update()
        
        s.show()
        
        if s.end() :
            squares.pop(i)

        if s.collide(car1) or s.collide(car2) :
            stop = True
            blink_index = i
            blink_shape = 1

        if blink_index == i and s.shape == blink_shape :
            s.blink = True

    keys = pygame.key.get_pressed() 

    if Llanecounter == 0 and keys[pygame.K_LEFT] :
        Llanecounter = 500
        car1.changelane()

    if Rlanecounter == 0 and keys[pygame.K_RIGHT] :
        Rlanecounter = 500
        car2.changelane()

    car1.show()
    car2.show()

    text = font.render(str(Lscore + Rscore), True, WHITE)
    win.blit(text, (screenWidth // 2 - 10, 10))

    return stop, Lscore, Rscore, Llanecounter, Rlanecounter, blink_index, blink_shape

startingspeed = 0.25
incrementspeed = 0.005
Lspeed = 0
Rspeed = 0
Lframecount = 0
Rframecount = 0
Lframechange = randint(1000, 2000)
Rframechange = randint(1000, 2000)
Lscore = 0
Rscore = 0
Llanecounter = 0
Rlanecounter = 0
prevscore = -1

run = True
while run :

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            run = False

    win.fill(BG_COLOR)

    stop, Lscore, Rscore, Llanecounter, Rlanecounter, blink_index, blink_shape = draw(stop, Lscore, Rscore, Llanecounter, Rlanecounter, blink_index, blink_shape)

    if Lframecount % Lframechange == 0 :
        Lframecount = 0
        Lframechange = randint(1000, 2000)
        Lspeed += incrementspeed

        w = 0
        if randint(0, 1) == 0 :
            w = screenWidth // 4
        
        shape = randint(0, 1)
        if shape == 0 :
            c = Obstacle(screenWidth // 8 + w, -100, 0, LIGHT_RED, startingspeed + Lspeed)
            circles.append(c)
        else :
            s = Obstacle(screenWidth // 8 + w, -100, 1, LIGHT_RED, startingspeed + Lspeed)
            squares.append(s)


    if Rframecount % Rframechange == 0 :
        Rframecount = 0
        Rframechange = randint(1000, 2000)
        Rspeed += incrementspeed

        w = 0
        if randint(0, 1) == 0 :
            w = screenWidth // 4

        shape = randint(0, 1)
        if shape == 0 :
            c  = Obstacle(screenWidth // 8 + screenWidth // 2 + w, -100, 0, LIGHT_BLUE, startingspeed + Rspeed)
            circles.append(c)
        else :
            s  = Obstacle(screenWidth // 8 + screenWidth // 2 + w, -100, 1, LIGHT_BLUE, startingspeed + Rspeed)
            squares.append(s)

    if Llanecounter > 0 :
        Llanecounter -= 1
    
    if Rlanecounter > 0 :
        Rlanecounter -= 1

    Lframecount += 1
    Rframecount += 1
    pygame.display.update()

pygame.quit()