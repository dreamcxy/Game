import pygame
from pygame.locals import *
from sys import exit

pygame.init()
window_size = Rect(0, 0, 800, 600)
screen = pygame.display.set_mode(window_size.size)

start_button_up = "start.png"
start_button_down = "start_down.png"

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GAINSBORO = (220, 220, 220)
WHITESMOKE = (245, 245, 245)
LIGHTGREY = (211, 211, 211)
GREEN = (0, 255, 0)


class Button(object):
    def __init__(self, button_up_image, button_down_image, pos, name):
        self.button_up = pygame.image.load(button_up_image).convert_alpha()
        self.button_down = pygame.image.load(button_down_image).convert_alpha()
        self.pos = pos
        self.name = name

    def is_over(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.pos
        w, h = self.button_up.get_size()
        in_x = x - w / 2 < point_x < x + w / 2
        in_y = y - h / 2 < point_y < y + h / 2
        return in_x and in_y

    def render(self):
        w, h = self.button_up.get_size()
        x, y = self.pos
        if self.is_over():
            screen.blit(self.button_down,
                        (x - w / 2, y - h / 2))
        else:
            screen.blit(self.button_up,
                        (x - w / 2, y - h / 2))

    def rect(self):
        x, y = self.pos
        w, h = self.button_up.get_size()
        return Rect(x - w / 2, y - h / 2, w, h)


def split_screen(surface_width, surface_height, surface_color, surface_pos):
    surface = pygame.Surface((surface_width, surface_height))
    surface.fill(surface_color)
    surface_rect = surface.get_rect()
    screen.blit(surface, surface_pos)
    return surface


def get_click_button(click_x, click_y):
    for button in BUTTONS:
        rect = button.rect()
        print rect
        print click_x, click_y
        print button.button_up.get_size()
        if rect.collidepoint((click_x, click_y)):
            return button.name


def show_text(font_obj, text, x, y):
    text_surface_obj = font_obj.render(text, True, GREEN, WHITE)
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (x, y)
    screen.blit(text_surface_obj, text_rect_obj)


def action_start(time):
    time = 0
    return time


TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER, 1000)
counts = 0
font_big_obj = pygame.font.Font("PAPYRUS.ttf", 48)
surface_width = 200
surface_height = 300
button_surface = split_screen(surface_width, surface_height, GAINSBORO, (0, 0))
time_surface = split_screen(
    surface_width, surface_height, WHITESMOKE, (0, 300))
game_surface = split_screen(800 - surface_width, 600, LIGHTGREY, (200, 0))

start_button = Button(start_button_up, start_button_down,
                      (100, 150), "start")

BUTTONS = []
BUTTONS.append(start_button)

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
        elif event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == TIMER:
            counts += 1
        elif event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            clicked_button = get_click_button(click_x, click_y)
            if clicked_button == "start":
                counts = action_start(counts)
        show_text(font_big_obj, str(counts), 100, 450)
    start_button.render()
    pygame.display.update()
