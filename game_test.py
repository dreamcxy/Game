import pygame
import random
from pygame.locals import *
from sys import exit
from math import sqrt

window = Rect(0, 0, 600, 800)
window_width = window.size[0]
window_height = window.size[1]
pygame.init()
screen = pygame.display.set_mode(window.size)

Magenta = (255, 0, 255)
Yellow = (255, 255, 0)
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)
CHANGESPEED = pygame.USEREVENT + 2
pygame.time.set_timer(CHANGESPEED, 3000)
BORNNUM = pygame.USEREVENT + 3
pygame.time.set_timer(BORNNUM, 8000)
init_speed = [1, 1]
born_num = 1


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.radius = 10
        self.pos = [100, 200]
        self.circle = pygame.draw.circle(screen, Yellow, self.pos, self.radius, 0)
        pygame.display.flip()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def update(self, mouse_pos):
        self.pos = mouse_pos
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        if mouse_y < self.radius:
            mouse_y = self.radius
        elif mouse_y > window.size[1] - self.radius:
            mouse_y = window.size[1] - self.radius
        elif mouse_x < self.radius:
            mouse_x = self.radius
        elif mouse_x > window.size[0] - self.radius:
            mouse_x = window.size[0] - self.radius
        screen.fill((0, 0, 0))
        self.circle = pygame.draw.circle(screen, Yellow, mouse_pos, self.radius, 0)


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Enemy1, self).__init__()
        self.radius = 10
        self.pos = pos
        self.appear = True
        self.speed = init_speed
        print self.speed
        self.circle = pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)
        pygame.display.flip()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def disappear(self):
        self.appear = False

    def auto_move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)

    def draw(self):
        pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)
        pygame.display.flip()


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Enemy2, self).__init__()
        self.radius = 10
        self.pos = pos
        self.appear = True
        self.speed = init_speed
        self.circle = pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)
        pygame.display.flip()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def disappear(self):
        self.appear = False

    def auto_move(self):
        self.pos[0] -= self.speed[0]
        self.pos[1] += self.speed[1]
        pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)

    def draw(self):
        pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)
        pygame.display.flip()


class Enemy3(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Enemy3, self).__init__()
        self.radius = 10
        self.pos = pos
        self.appear = True
        self.speed = init_speed
        self.circle = pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)
        pygame.display.flip()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def disappear(self):
        self.appear = False

    def auto_move(self):
        self.pos[0] -= self.speed[0]
        self.pos[1] -= self.speed[1]
        pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)

    def draw(self):
        pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)
        pygame.display.flip()


class Enemy4(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Enemy4, self).__init__()
        self.radius = 10
        self.pos = pos
        self.appear = True
        self.speed = init_speed
        self.circle = pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)
        pygame.display.flip()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def disappear(self):
        self.appear = False

    def auto_move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] -= self.speed[1]
        pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)

    def draw(self):
        pygame.draw.circle(screen, Magenta, self.pos, self.radius, 0)
        pygame.display.flip()


class Feature1(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Feature1, self).__init__()
        self.radius = 10
        self.pos = pos
        self.appear = True
        self.speed = init_speed
        self.circle = pygame.draw.circle(screen, ())


def distance(pos1, pos2):
    return sqrt(pow((pos1[0] - pos2[0]), 2) + pow((pos1[1] - pos2[1]), 2))


def judge_collide(player, enemy):
    player_pos = player.get_pos()
    player_radius = player.get_radius()
    enemy_pos = enemy.get_pos()
    enemy_raidus = enemy.get_radius()
    if distance(player_pos, enemy_pos) <= abs(player_radius + enemy_raidus):
        return True
    return False


def out_border(enemy):
    enemy_pos = enemy.get_pos()
    if enemy_pos[0] > window_width or enemy_pos[1] > window_height:
        return True
    return False


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


def add_speed():
    if init_speed[0] <= 9:
        init_speed[0] += 1
        init_speed[1] += 1


def update_born_num():
    global born_num
    if born_num <= 5:
        born_num += 2


def random_a():
    x = 0
    y = random.randint(0, window_height)
    return [x, y]


def random_b():
    y = 0
    x = random.randint(0, window_width)
    return [x, y]


def random_c():
    x = window_width
    y = random.randint(0, window_height)
    return [x, y]


def random_d():
    x = random.randint(0, window_width)
    y = window_height
    return [x, y]


def random_born():
    situation = random.randint(0, 3)
    for case in Switch(situation):
        if case(0):
            return random_a()
            break
        if case(1):
            return random_b()
            break
        if case(2):
            return random_c()
            break
        if case(3):
            return random_d()
            break
        if case():
            return False


enemies = pygame.sprite.Group()
player = Player()
while True:
    for enemy in enemies:
        if enemy.appear:
            enemy.auto_move()
            enemy.draw()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            mouse_pos = mouse_x, mouse_y
        elif event.type == ADDENEMY:
            for i in range(0, born_num):
                born_place = random_born()
                x = born_place[0]
                y = born_place[1]
                if x <= window_width / 2 and y <= window_height / 2:
                    new_enemy = Enemy1(born_place)
                elif x >= window_width / 2 and y <= window_height / 2:
                    new_enemy = Enemy2(born_place)
                elif x >= window_width / 2 and y >= window_height / 2:
                    new_enemy = Enemy3(born_place)
                else:
                    new_enemy = Enemy4(born_place)
                enemies.add(new_enemy)
        elif event.type == CHANGESPEED:
            add_speed()
        elif event.type == BORNNUM:
            update_born_num()
    player.update(mouse_pos)
    for enemy in enemies:
        if judge_collide(player, enemy) or out_border(enemy):
            # print 'col'
            enemy.disappear()
            enemies.remove(enemy)

    pygame.display.update()
