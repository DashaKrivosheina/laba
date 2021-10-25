import pygame
from pygame.draw import *
from random import choice
from random import randint
import math
pygame.init()

FPS = 20
X_SIZE = 1200
Y_SIZE = 900
screen = pygame.display.set_mode((X_SIZE, Y_SIZE))

WHITE = (255, 255, 255)
RED = (255, 100, 100)
BLUE = (140, 220, 250)
YELLOW = (240, 240, 80)
GREEN = (90, 240, 100)
MAGENTA = (190, 100, 205)
CYAN = (110, 250, 200)
PINK = (250, 140, 160)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, PINK]
balls = [] #массив параметров шариков
N = 0 #количество очков

data = open('rating.txt', 'r')
rating_old = data.read()
data.close()

class Ball:
    def __init__(self):
        self.x = randint(100, 1000)
        self.y = randint(100, 600)
        self.r = randint(10, 90)
        self.Vx = randint(-5, 5)
        self.Vy = randint(-5, 5)
        self.color = COLORS[randint(0, 6)]

    def draw_ball(self):
        '''
        Рисует шарик по его параметрам (цвет, x, y, r)
        '''
        circle(screen, self.color, (self.x, self.y), self.r)

    def move_ball(self):
        '''Двигает шарики'''
        self.x += self.Vx
        self.y += self.Vy

        if self.x>X_SIZE - self.r or self.x<self.r:
            self.Vx = -self.Vx

        if self.y>Y_SIZE - self.r or self.y < self.r:
            self.Vy = -self.Vy

    def check_click(self, X, Y):
        '''
        :param x,y: Пара координат мыши (X, Y)
        :return: Возвращает True если попасть по шарику кликом и False если не попасть
        '''
        if (X- self.x)**2 + (Y- self.y)**2 <= self.r**2:
            return True
        else:
            return False
class Star:
    def __init__(self):
        self.x = randint(100, 1100)
        self.y = randint(100, 800)
        self.R = randint (20, 35)
        self.Vx = randint(-20, 20)
        self.Vy = randint(-20, 20)
        self.color = COLORS[randint(0, 6)]
        self.life = randint (40, 150)

    def draw_star(self):
        '''
        Рисует звезду по ее параметрам (цвет, x, y, R)
        '''
        polygon( screen, self.color, [(self.x, self.y - self.R),
                                      (self.x - self.R*math.sin(1/5*math.pi), self.y + self.R*math.cos(1/5*math.pi)),
                                      (self.x + self.R*math.cos(math.pi/10), self.y - self.R*math.sin(math.pi/10)),
                                      (self.x - self.R*math.cos(math.pi/10), self.y - self.R*math.sin(math.pi/10)),
                                      (self.x + self.R*math.sin(1/5*math.pi),self.y + self.R*math.cos(1/5*math.pi))])
    def move_star(self):
        '''Двигает звезду'''
        self.x += self.Vx
        self.y += self.Vy

    def check_click(self, X, Y):
        '''
        :param x,y: Пара координат мыши (X, Y)
        :return: Возвращает True если попасть по шарику кликом и False если не попасть
        '''
        if (X- self.x)**2 + (Y- self.y)**2 <= (self.R*math.cos(2/5*math.pi)/math.cos(1/5*math.pi)+5)**2:
            return True
        else:
            return False
                 
                
def mouse_xy(event):
        '''Возвращает координаты мыши'''
        X = event.pos[0]
        Y = event.pos[1]
        return X, Y

star = Star()

'''начальный экран'''
clock = pygame.time.Clock()
pygame.font.init()
f3 = pygame.font.Font(None, 36)
text1 = f3.render('Введите имя игрока:', True, WHITE)
font = pygame.font.Font(None, 36)
input_box = pygame.Rect(500, 400, 140, 36)
color_inactive = pygame.Color('white')
color_active = pygame.Color('red')
color = color_inactive
active = False
text = ''
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False
            # Change the current color of the input box.
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    name = text
                    print(text)
                    text = ''
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    screen.fill((250, 200, 200))
    # Render the current text.
    txt_surface = font.render(text, True, color)
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    # Blit the text.
    screen.blit(text1, (10, 50))
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, color, input_box, 2)
    pygame.display.flip()
    clock.tick(30)

time = 0
game_time = 500



finished = False
while not finished:
    clock.tick(FPS)
    star.life -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print(N)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            X,Y = mouse_xy(event)
            for ball in balls:
                if ball.check_click(X, Y):
                    N += 1
                    balls.remove(ball)
            if star.check_click(X, Y):
                N += 10
                star = Star()
    if star.life <=0:
        star = Star()
    p = str(N)
    f1 = pygame.font.Font(None, 46)
    text1 = f1.render('Счёт:', True, (240, 60, 60))
    text2 = f1.render(p , True, (240, 60, 60))
    screen.blit( text1, (10, 10))
    screen.blit( text2, (100, 10))
    
    if len(balls) < 10:
        new_ball = Ball()
        balls.append(new_ball)
    pygame.display.update()
    screen.fill(WHITE)
    star.draw_star()
    star.move_star()
    time += 1
    if time > game_time:
        finished = True
        print('Total score:', N)

    for ball in balls:
        ball.move_ball()
        ball.draw_ball()
        
'''рэйтинг'''
rating = open('Rating.txt', 'w')
print(rating_old, file=rating)
print(name, N, file=rating)
rating.close()

rating = open('Rating.txt', 'r')
data = rating.readlines()
data = [line.rstrip() for line in data]
rating.close()

screen.fill(WHITE)
text = []
for line in data:
    text.append(f3.render(line, True, BLACK))
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    for i in range(len(text)):
        screen.blit(text[i], (10, 50 + 12*i))
    pygame.display.flip()
    
pygame.quit()
