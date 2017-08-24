import pygame
import sys
from pygame.locals import *

pygame.init()
welcome_window = Rect(0, 0, 600, 800)
window_size = welcome_window.size
welcome_screen = pygame.display.set_mode(window_size)
window_width = window_size[0]
window_height = window_size[1]
start_button_up = "start.png"
start_button_down = "start_down.png"


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
            welcome_screen.blit(self.button_down,
                                (x - w / 2, y - h / 2))
        else:
            welcome_screen.blit(self.button_up,
                                (x - w / 2, y - h / 2))

    def rect(self):
        x, y = self.pos
        w, h = self.button_up.get_size()
        return Rect(x - w / 2, y - h / 2, w, h)


def get_click_button(click_x, click_y):
    for button in BUTTONS:
        rect = button.rect()
        print rect
        print click_x, click_y
        print button.button_up.get_size()
        if rect.collidepoint((click_x, click_y)):
            return button.name


welcome_button = Button(start_button_up, start_button_down, (window_width / 2, window_height / 2), 'welcome')
BUTTONS = []
BUTTONS.append(welcome_button)
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            click_x, click_y = event.pos
            clicked_button = get_click_button(click_x, click_y)
            if clicked_button == "welcome":
                print 'welcome'
                pygame.quit()
                execfile("game_board.py")
    welcome_button.render()
    pygame.display.update()