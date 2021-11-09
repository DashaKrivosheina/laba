import math
from random import randint as rnd
from random import choice

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [YELLOW, MAGENTA, CYAN, WHITE]

WIDTH = 800
HEIGHT = 600


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
        self.live = 60

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= 1
        self.x += self.vx
        self.y -= self.vy
        if self.y + self.r >= HEIGHT:
            self.vx = 0.8*self.vx
            self.vy = -0.9*self.vy
            self.y = HEIGHT - self.r
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx
            self.x = WIDTH - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r

    def draw(self):
        """Отрисовывает мяч"""
        border = self.r+1
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            border
        )
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
        if ((self.x-obj.x)**2+(self.y-obj.y)**2)**0.5 > self.r + obj.r or self.live <= 0:
            return False
        else:
            return True

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
        """ Конструктор класса gun
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 10
        self.y = HEIGHT-20
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
            new_ball.r += 2
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
        if event: #не переписла
            if event.pos[0] == self.x:
                self.an = math.pi/2
            else:
                self.an = math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = BLACK

    def draw(self):
        """Отрисовывает пушку"""
        angle = math.cos(self.an)
        if self.an < 0:
            angle = -angle
        pygame.draw.line(
            self.screen,
            BLACK,
            (self.x, self.y), (self.x-self.f2_power * angle, 
            self.y-self.f2_power * abs(math.sin(self.an))),
            7
        )
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y), (self.x-self.f2_power * angle, 
            self.y-self.f2_power * abs(math.sin(self.an))),
            5
        )
        pygame.draw.rect(self.screen, 
            BLACK, (self.x-10, self.y, 20, 10))
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y+15),
            5
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x-10, self.y+15),
            5
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x+10, self.y+15),
            5
        )
        
    
    def power_up(self):
        """Определяет силу выстрела"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
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
        elif self.y < 7*HEIGHT/8:
            self.vy = 0
            self.y = 7*HEIGHT/8
        self.y += self.vy

class Target:
    def __init__(self, screen, x = 600, y = 300, r = 10, vx = 0, vy = 0):
        """ Конструктор класса target

        Args:
        x - начальное положение мишени по горизонтали
        y - начальное положение мишени по вертикали
        r - радиус мишени
        vx - скорость мишени по горизонтали
        vy - скорость мишени по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = choice(GAME_COLORS)
        self.points = 0
        self.live = 1

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(10, 30)
        vx = self.vx = rnd(-10, 10)
        vy = self.vy = rnd(-10, 10)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """Отрисовывает мишень"""
        border = self.r+1
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            border
        )
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
    def move(self):
        """Переместить мишени по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.y + self.r >= HEIGHT:
            self.vy = -self.vy
            self.y = HEIGHT - self.r
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx
            self.x = WIDTH - self.r
        if self.y - self.r <= 0:
            self.vy = -self.vy
            self.y = self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r

class Blinker:
    def __init__(self, screen, x = 0, y = 0, dx = 10, dy = 10, live =40):
        """ Конструктор класса blinker
        
        Args:
        x - начальное положение мишени по горизонтали
        y - начальное положение мишени по вертикали
        dx - размер мишени по горизонтали
        dy - размер мишени по вертикали
        dt - время жизни мишени 
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = dx
        self.vy = dy
        self.color = choice(GAME_COLORS)
        self.r = min(dx, dy)
        self.points = 0
        self.live = live

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(10, WIDTH-40)
        y = self.y = rnd(10, HEIGHT-40)
        dx = self.dx = rnd(5, 20)
        dy = self.dy = rnd(5, 20)
        live = self.live = rnd(80, 120)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points  
    
    def draw(self):
        """Отрисовка цели"""
        if self.live%40>20:
            pygame.draw.rect(self.screen, 
            BLACK, (self.x-self.dx-1, self.y-self.dy-1, 2*self.dx+2, 2*self.dy+2))
            pygame.draw.rect(self.screen, 
            self.color, (self.x-self.dx, self.y-self.dy, 2*self.dx, 2*self.dy))

    def move(self):
        """Функция уменьшает оставшееся время жизни исчезающего объекта или заменяет его на новый,
         если время истекло"""
        if self.live<=0:
            self.new_target()
        else:
            self.live-=1

class Bomb(Ball):
    def __init__(self):
        """Инициализация дочернего класса"""
        Ball.__init__(self, screen)
        self.live = 1
    def new_bomb(self, gun):
        """Подстраиваем параметры"""
        self.x = gun.x
        self.y = 0
        self.vx = 0
        self.vy = rnd(1,3)
        self.r = rnd(1,5)
    def expmove(self, gun):
        """Движение бомбы: просто падает до столкновения с танком, а в конце взрывается"""
        self.live = not self.hittest(gun)
        if self.y+self.r >= HEIGHT:
            self.live = 0
        if self.live:
            self.color = BLACK
            self.move()
        else:
            for i in range(100):
                shard = Ball(self.screen)
                shard.x = self.x
                shard.y = self.y
                shard.vx = rnd(-50, 50)
                shard.vy = rnd(-50, 50)
                shard.r = rnd(1, 3)
                shard.color = YELLOW
                shard.live = 30
                shards.append(shard)
            self.new_bomb(gun)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
lasers = []
shards = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
bomb = Bomb()
bomb.new_bomb(gun)
# Массив целей можно создавать и в цикле, но для демонстрации работы тут только два
targets.append(Blinker(screen))
targets.append(Blinker(screen))
targets.append(Target(screen))
targets.append(Target(screen))
for i in targets:
    i.new_target()
finished = False
score = 5
attempt = 0
bullet_type = 1

while not finished:
    # Отрисовка всего
    screen.fill(BLUE)
    pygame.draw.rect(screen, 
            GREEN, (0, 7*HEIGHT/8, WIDTH, HEIGHT/8))
    gun.move()
    gun.draw()
    bomb.expmove(gun)
    score = score - bomb.hittest(gun)
    bomb.draw()
    for i in shards:
        if i.live<0:
            shards.remove(i)
        else:
            i.move()
            i.draw()
            i.live -= 1
    for i in targets:
        i.move()
        i.draw()
    for b in balls:
        b.live -= 1
        if b.live > 0 or (abs(b.vx)>0.01 and abs(b.vy)>0.01):
            b.draw()
        else:
            balls.remove(b)
    for l in lasers:
        l.live -= 1
        if l.live > 0:
            l.draw()
        else:
            lasers.remove(l)
    
    # Вывод счетчиков на экран
    font=pygame.font.Font(None, 36)
    scorevalue="score = "+str(score)
    scoreboard=font.render(scorevalue, True, BLACK)
    screen.blit(scoreboard, (10, 50))
    attemptvalue="attempt = "+str(attempt)
    attemptboard=font.render(attemptvalue, True, BLACK)
    screen.blit(attemptboard, (10, 10))
    pygame.display.update()
    clock.tick(FPS)

    # Управление
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if (not pygame.key.get_pressed()[pygame.K_RIGHT]) and (not pygame.key.get_pressed()[pygame.K_LEFT]):
                gun.vx = 0
            if (not pygame.key.get_pressed()[pygame.K_UP]) and (not pygame.key.get_pressed()[pygame.K_DOWN]):
                gun.vy = 0
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                gun.vx = 5
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                gun.vx = -5
            if pygame.key.get_pressed()[pygame.K_UP]:
                gun.vy = -5
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                gun.vy = 5

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_1]:
                bullet_type = 1
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_2]:
                bullet_type = 2

        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            attempt += 1
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    # Проверка столкновений
    for b in balls:
        b.move()
        for i in targets:
            if b.hittest(i):
                i.hit()
                score += 6 - attempt
                attempt = 0
                i.new_target()
    for l in lasers:
        l.move()
        for i in targets:
            if l.hittest(i):
                i.hit()
                score += 6 - attempt
                attempt = 0
                i.new_target()
    gun.power_up()

    if score < 0:
        screen.fill(BLACK)
        font=pygame.font.Font(None, 72)
        scorevalue="Game Over"
        scoreboard=font.render(scorevalue, True, GREEN)
        screen.blit(scoreboard, (250, 250))
        finished = True
        pygame.display.update()
        pygame.time.delay(2000)

pygame.quit()
