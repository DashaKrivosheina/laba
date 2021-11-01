import math
from random import choice
from pygame.draw import *
from random import randint
import pygame

FPS = 30

RED = (255, 100, 100)
BLUE = (140, 220, 250)
YELLOW = (240, 240, 80)
GREEN = (90, 240, 100)
MAGENTA = (190, 100, 205)
CYAN = (110, 250, 200)
PINK = (250, 140, 160)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, PINK]

WIDTH = 800
HEIGHT = 600

data = open('top_list.txt', 'r')
rating_old = data.read()
data.close()

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x 
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 150

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        g = 0.7
        k = 0.02
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.r >= WIDTH or self.x <= self.r:
            self.vx = -self.vx
        if self.y > HEIGHT - self.r or self.y <= self.r:
            self.vy = -self.vy
        else:
            self.vy -= g
            self.vy -= k* self.vy
        self.live -= 1
            

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 200
        self.y = 450
        self.width = 5

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, x=self.x, y=self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-self.y) , (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        x2 = self.x - self.width*math.sin(self.an)
        y2 = self.y + self.width*math.cos(self.an)
        x1 = self.x + math.cos(self.an)*self.f2_power
        y1 = self.y + math.sin(self.an)*self.f2_power
        x3 = x2 + math.cos(self.an) * self.f2_power
        y3 = y2 + math.sin(self.an) * self.f2_power
        pygame.draw.polygon(self.screen, self.color,((self.x, self.y), (x1, y1), (x3, y3), (x2, y2)))
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    
    def __init__(self):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()
        
    def draw(self):
        '''
        Рисует шарик по его параметрам (цвет, x, y, r)
        '''
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r, 1)

    def move(self):
        '''Двигает шарики'''
        self.x += self.Vx
        self.y -= self.Vy
        if self.x>=WIDTH - self.r - 1 or self.x<=self.r:
            self.Vx = -self.Vx

        if self.y>=HEIGHT - self.r - 1 or self.y <= self.r:
            self.Vy = -self.Vy
            
    def new_target(self):
        '''Инициализация новой цели'''
        x = self.x = randint(300, 750)
        y = self.y = randint(300, 550)
        r = self.r = randint(2, 50)
        Vx = self.Vx = randint(-10, 10)
        Vy = self.Vy = randint(-10, 10)
        self.live = 1
        self.color = RED
            
    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

class Star:
    '''Новый тип мишени'''
    def __init__(self):
        self.x = randint(350, 750)
        self.y = randint(35, 550)
        self.R = randint (20, 35)
        self.Vx = randint(-20, 20)
        self.Vy = randint(-20, 20)
        self.color = GAME_COLORS[randint(0, 6)]
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
        '''if self.x + self.R >= WIDTH or self.x <= self.R:
            self.Vx = -self.Vx
        if self.y > HEIGHT - self.R or self.y <= self.R:
            self.Vy = -self.Vy'''

    def check_hit(self, obj):
        '''
        :return: Возвращает True если попасть по шарику и False если не попасть
        '''
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.R + obj.r)**2:
            return True
        else:
            return False
        
star = Star()
'''Заставка'''
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.font.init()
f1 = pygame.font.Font(None, 36)
text1 = f1.render('Введите имя игрока:', True, WHITE)
font = pygame.font.Font(None, 36)
input_box = pygame.Rect(300, 300, 140, 36)
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
    
bullet = 0
balls = []
targets = []

gun = Gun(screen)
for i in range(5):
    targets.append(Target())
score0 = 0   
finished = False
while not finished:
    screen.fill(WHITE)
    gun.draw()
    star.draw_star()
    star.move_star()
    for target in targets:
        target.draw()
    for b in balls:
        if b.live<0: balls.remove(b)
        b.draw()
    score = score0
    star.life -= 1
    for target in targets:
        score += target.points
    
    text1 = f1.render('Score: ' + str(score), True, (0, 0, 0))
    screen.blit(text1, (10, 50))
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    if star.life<=0:
        star = Star()
    for target in targets:
        target.move()
    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
        if star.check_hit(b):
            print('hit')
            score0 += 10
            star = Star()
    gun.power_up()

'''рэйтинг'''
rating = open('top_list.txt', 'w')
print(rating_old, file=rating)
print(name, score, file=rating)
rating.close()

rating = open('top_list.txt', 'r')
data = rating.readlines()
data = [line.rstrip() for line in data]
rating.close()

screen.fill(WHITE)
text = []
for line in data:
    text.append(f1.render(line, True, BLACK))
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
