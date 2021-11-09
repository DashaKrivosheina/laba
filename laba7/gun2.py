import math
from random import choice
from pygame.draw import *
from random import randint
import pygame

FPS = 30

RED = (255, 100, 100)
BLUE = (140, 220, 250)
YELLOW = (255, 229, 120)
GREEN = (80, 220, 100)
MAGENTA = (218, 112, 214)
CYAN = (110, 250, 200)
PINK = (250, 140, 160)
PEACH = (255, 127, 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BODY = (230, 190, 138)
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, PINK, PEACH]

WIDTH = 800
HEIGHT = 600
WALL = 520

data = open('top_list.txt', 'r')
rating_old = data.read()
data.close()

class Ball:
    def __init__(self, screen: pygame.Surface, x=150, y=550):
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
        self.live = 120

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
        if self.y >= HEIGHT - self.r or self.y <= self.r:
            self.vy = -self.vy
        else:
            self.vy -= g
            self.vy -= k* self.vy
        self.live -= 1
            
    def draw(self):
        pygame.draw.circle(self.screen, self.color,(self.x, self.y), self.r)

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
class Laser:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса laser
        Args:
        x - начальное положение лазера по горизонтали
        y - начальное положение лазера по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.length = 20
        self.vx = 0
        self.vy = 0
        self.an = 1
        self.r = 3
        self.color = choice(GAME_COLORS)
        self.live = 500

    def move(self):
        """Переместить лазер по прошествии единицы времени.
        Метод описывает перемещение лазера за один кадр перерисовки.
        """
        self.x += self.vx
        self.y -= self.vy
        self.live -= 1

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y), (self.x + math.cos(self.an) * self.length, 
            self.y + math.sin(self.an) * self.length),
            5
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения лазера и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= obj.r ** 2:
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
        self.x = randint(100, 700)
        self.y = 550
        self.width = 5
        self.vx = 0
        self.vy = 0
        self.r = 20

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, targets, shards, lasers
        bullet += 1
        if bullet_type == 1:
            new_ball = Ball(self.screen, x=self.x, y=self.y)
            new_ball.r += 5
            if event.pos[0] == new_ball.x:
                self.an = math.pi/2
            else:
                self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
            balls.append(new_ball)
        if bullet_type == 2:
            new_laser = Laser(self.screen, x=self.x, y=self.y)
            if event.pos[0] == new_laser.x:
                self.an = math.pi/2
            else:
                self.an = math.atan2((event.pos[1]-new_laser.y), (event.pos[0]-new_laser.x))
            new_laser.an = self.an
            new_laser.vx = self.f2_power * math.cos(self.an)
            new_laser.vy = - self.f2_power * math.sin(self.an)
            new_laser.length = self.f2_power
            lasers.append(new_laser)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] == self.x:
                self.an = math.pi/2
            else:
                self.an = math.atan2((event.pos[1]-self.y) , (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        self.a = 20
        x2 = self.x - self.width*math.sin(self.an)
        y2 = self.y + self.width*math.cos(self.an)
        x1 = self.x + math.cos(self.an)*self.f2_power
        y1 = self.y + math.sin(self.an)*self.f2_power
        x3 = x2 + math.cos(self.an) * self.f2_power
        y3 = y2 + math.sin(self.an) * self.f2_power
        pygame.draw.rect(self.screen, BODY, (self.x - self.a/2, self.y - self.a/2,self.a, self.a))
        pygame.draw.polygon(self.screen, self.color,((self.x, self.y), (x1, y1), (x3, y3), (x2, y2)))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move(self):
        """Движение пушки"""
        if self.x < 10:
            self.vx = 0
            self.x = 10
        elif self.x > WIDTH-10:
            self.vx = 0
            self.x = WIDTH-10
        self.x += self.vx
        if self.y > HEIGHT-10:
            self.vy = 0
            self.y = HEIGHT-10
        elif self.y < WALL + 13:
            self.vy = 0
            self.y = WALL + 13
        self.y += self.vy

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
        if self.x >= WIDTH - self.r - 1 or self.x <= self.r:
            self.Vx = -self.Vx

        if self.y >= WALL - self.r - 1 or self.y <= self.r:
            self.Vy = -self.Vy
            
    def new_target(self):
        '''Инициализация новой цели'''
        x = self.x = randint(55, 750)
        y = self.y = randint(55, 470)
        r = self.r = randint(10, 50)
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
        self.x = randint(50, 750)
        self.y = randint(35, 485)
        self.R = randint (20, 35)
        self.Vx = randint(-20, 20)
        self.Vy = randint(-20, 20)
        self.color = YELLOW 
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
            self.Vx = -self.Vx'''
        if self.y >= WALL - self.R:
            self.Vy = -self.Vy

    def check_hit(self, obj):
        '''
        :return: Возвращает True если попасть по шарику и False если не попасть
        '''
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.R + obj.r)**2:
            return True
        else:
            return False
        
class Bomb(Ball):
    def __init__(self):
        """Инициализация дочернего класса"""
        Ball.__init__(self, screen)
        self.live = 1
    def new_bomb(self, gun):
        """Подстраиваем параметры"""
        self.x = gun.x
        self.y = 6
        self.vx = 0
        self.vy = randint(1,2)
        self.r = randint(3,5)
    def expmove(self, gun):
        """Движение бомбы: просто падает до столкновения с танком, а в конце взрывается"""
        self.live = not self.hittest(gun)
        if self.y+self.r >= HEIGHT:
            self.live = 0
        if self.live:
            self.color = BLACK
            self.move()
        else:
            self.new_bomb(gun1)     
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
lasers = []
shards = []
gun1 = Gun(screen)
gun2 = Gun(screen)
bomb = Bomb()
bomb.new_bomb(gun1)

for i in range(5):
    targets.append(Target())
score0 = 0
bullet_type = 1
finished = False
while not finished:
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, [0,  WALL], [WIDTH, WALL], 3)
    gun1.draw()
    gun2.draw()
    gun1.move()
    gun2.move()
    bomb.expmove(gun1)
    bomb.draw()
    star.draw_star()
    star.move_star()
    for target in targets:
        target.draw()
        target.move()
    for b in balls:
        if b.live<0: balls.remove(b)
        b.draw()
    for l in lasers:
        l.live -= 1
        if l.live > 0:
            l.draw()
        else:
            lasers.remove(l)
    score = score0
    star.life -= 1
    for target in targets:
        score += target.points
    """Вывод счетчика на экран"""
    text1 = f1.render('Score: ' + str(score), True, (0, 0, 0))
    screen.blit(text1, (10, 20))
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if (not pygame.key.get_pressed()[pygame.K_RIGHT]) and (not pygame.key.get_pressed()[pygame.K_LEFT]):
                gun1.vx = 0
            if (not pygame.key.get_pressed()[pygame.K_UP]) and (not pygame.key.get_pressed()[pygame.K_DOWN]):
                gun1.vy = 0
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                gun1.vx = 5
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                gun1.vx = -5
            if pygame.key.get_pressed()[pygame.K_UP]:
                gun1.vy = -5
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                gun1.vy = 5

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_1]:
                bullet_type = 1
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_2]:
                bullet_type = 2
                
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun1.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun1.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun1.targetting(event)
    if star.life<=0:
        star = Star()
    """Проверка столкновений"""
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
    for l in lasers:
        l.move()
        for target in targets:
            if target.hittest(i):
                target.hit()
                target.new_target()
    gun1.power_up()

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
