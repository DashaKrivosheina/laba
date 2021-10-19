import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 4
X_SIZE = 1200
Y_SIZE = 900
screen = pygame.display.set_mode((X_SIZE, Y_SIZE))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
balls = [] #массив параметров шариков
N = 0 #количество очков

def new_ball():
    '''рисует новый шарик и возвращает его координаты и цвет'''
    x = randint(100, 800)
    y = randint(100, 500)
    r = randint(10, 90)
    Vx = randint(-5, 5)
    Vy = randint(-5, 5)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return [x, y, r], color, [Vx, Vy]

def mouse_xy(event):
    '''Возвращает координаты мыши'''
    X = event.pos[0]
    Y = event.pos[1]
    return X, Y
def draw_ball(params):
    '''
    Рисует шарик по его параметрам (цвет, x, y, r)
    '''
    color = params[1]
    (X, Y) = (params[0][0], params[0][1])
    r = params[0][2]
    circle(screen, color, (X, Y), r)

def move_ball(params, i):
    '''Двигает шарики'''
    (X, Y) = (params[0][0], params[0][1])
    (Vx, Vy) = (params[2][0], params[2][1])
    r = params[0][2]
    X += Vx
    Y += Vy

    if X>X_SIZE-r or X<r:
        Vx = -Vx

    if Y>Y_SIZE-r or Y<r:
        Vy = -Vy

    balls[i][0][0] = X
    balls[i][0][1] = Y
    balls[i][2][0] = Vx
    balls[i][2][1] = Vy




def check_click(xyr, xy):
    '''
    :param xyr: Тройка координат и радиуса шарика (x, y, r)
    :param xy: Пара координат мыши (x, y)
    :return: Возвращает True если попасть по шарику кликом и False если не попасть
    '''
    if (xy[0]-xyr[0])**2 + (xy[1]-xyr[1])**2 <= xyr[2]**2:
        return True
    else:
        return False
pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print(N)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            i = 0
            while i < len(balls):
                if check_click(balls[i][0], mouse_xy(event)):
                    N += 1
                    print(N)
                    balls.pop(i)
                i += 1
    
    p = str(N)
    f1 = pygame.font.Font(None, 46)
    text1 = f1.render('Счёт:', True, (180, 0, 0))
    text2 = f1.render(p , True, (180, 0, 0))
    screen.blit( text1, (10, 10))
    screen.blit( text2, (100, 10))
    
    if len(balls) < 10:
        balls.append(new_ball())
    pygame.display.update()
    screen.fill(BLACK)
    for i in range(len(balls)):
        move_ball(balls[i], i)
        draw_ball(balls[i])


pygame.quit()
