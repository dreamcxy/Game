# -*- coding: UTF-8 -*-
'''
Created on 2016年11月29日

@author: 小峰峰
'''

import random
import sys
import time
import pygame
from pygame.locals import *


FPS = 30  # 帧率
WINDOWWIDTH = 640  # 窗口宽度
WINDOWHEIGHT = 480  # 窗口高度
FLASHSPEED = 500  # 闪动的速度（毫秒）
FLASHDELAY = 200  # 闪动的延时（毫秒）
BUTTONSIZE = 200  # 方块的大小
BUTTONGAPSIZE = 20  # 方块间距
TIMEOUT = 4  # 超时（秒） seconds before game over if no button is pushed.

# 定义几个颜色
# R G B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)

bgColor = BLACK  # 设置背景色 （黑色）

# 方块与窗口之间的间距
XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)


# 四个方块的Rect属性
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE,
                       YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE +
                      BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE,
                        YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)


# 主函数
def main():

    # 定义几个全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()  # 初始化pygame

    FPSCLOCK = pygame.time.Clock()  # 获得pygame时钟

    DISPLAYSURF = pygame.display.set_mode(
        (WINDOWWIDTH, WINDOWHEIGHT))  # 设置窗口大小

    pygame.display.set_caption('Simon')  # 设置标题

    BASICFONT = pygame.font.Font('PAPYRUS.ttf', 16)  # 设置字体及大小

    # 绘制提示信息
    infoSurf = BASICFONT.render(
        'Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # 加载音频文件
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    # Initialize some variables for a new game
    pattern = []  # 用来储存模板颜色的序列
    currentStep = 0  # 玩家下一步需要按的颜色
    lastClickTime = 0  # 玩家最后按下按钮的时间戳
    score = 0  # 分数

    # 当waitingForInput为False时，表示播放模板；为True时表示等待用户点击
    waitingForInput = False

    while True:  # 游戏主循环
        clickedButton = None  # 当前按下的按钮(YELLOW, RED, GREEN, or BLUE)

        DISPLAYSURF.fill(bgColor)  # 绘制背景色

        drawButtons()  # 绘制四个按钮

        # 绘制分数
        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)  # 绘制提示信息

        for event in pygame.event.get():  # 事件处理

            if event.type == MOUSEBUTTONUP:  # 处理鼠标点击事件

                mousex, mousey = event.pos  # 获得鼠标点击的像素位置

                clickedButton = getButtonClicked(
                    mousex, mousey)  # 根据像素位置获得点击的按钮

            elif event.type == KEYDOWN:  # 处理按键事件

                # Q为黄色；W为蓝色；A为红色；S为绿色；ESC键为退出
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        if not waitingForInput:  # 播放模板

            pygame.display.update()
            pygame.time.wait(1000)

            # 随机从四个颜色中选一个添加到pattern序列中
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))

            for button in pattern:  # 从序列中取出每一个颜色并闪动相应的按钮
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)

            # 等待用户点击
            waitingForInput = True

        else:
            # 等待玩家按按钮
            if clickedButton and clickedButton == pattern[currentStep]:
                # 如果按的是pattern序列中currentStep所指的按钮
                flashButtonAnimation(clickedButton)
                currentStep += 1  # currentStep往后移一位
                lastClickTime = time.time()  # 给lastClickTime赋值当前的时间

                if currentStep == len(pattern):
                    # 如果为pattern序列的最后一步
                    changeBackgroundAnimation()  # 播放背景闪动的动画，表示已经成功模仿完整个pattern序列
                    score += 1  # 分数加一分
                    waitingForInput = False  # 设置为播放模板状态
                    currentStep = 0  # 将currentStep退回最前面

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # 两个条件，按了错误的按钮或者超时

                # 超时是指，在根据序列模仿的过程中，按下两个按钮的时间间隔超过4秒

                gameOverAnimation()  # 播放游戏结束动画

                # 重置所有的变量
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        # 更新屏幕
        pygame.display.update()
        # 设置帧率
        FPSCLOCK.tick(FPS)


# 闪动按钮的动画
def flashButtonAnimation(color, animationSpeed=50):
    # 如果是红色按钮
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    # 如果是蓝色按钮
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    # 如果是红色按钮
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    # 如果是绿色按钮
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT

    origSurf = DISPLAYSURF.copy()  # 拷贝一份原来的Surface
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))  # 闪动的部分
    flashSurf = flashSurf.convert_alpha()  # 转变为有透明度的Surface
    r, g, b = flashColor

    sound.play()  # 播放音效

    for start, end, step in ((0, 255, 1), (255, 0, -1)):  # 通过改变 alpha值 透明度实现动画

        # 在循环中第一次是将透明度从0到255，step为1；第二次是从255到0，step为-1

        for alpha in range(start, end, animationSpeed * step):

            DISPLAYSURF.blit(origSurf, (0, 0))

            flashSurf.fill((r, g, b, alpha))

            DISPLAYSURF.blit(flashSurf, rectangle.topleft)

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    DISPLAYSURF.blit(origSurf, (0, 0))


# 绘制四个按钮
def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)


# 改变游戏背景的动画
def changeBackgroundAnimation(animationSpeed=40):

    global bgColor

    # 随机出一个新的颜色
    newBgColor = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))

    newBgSurf = newBgSurf.convert_alpha()

    r, g, b = newBgColor

    for alpha in range(0, 255, animationSpeed):  # 改变alpha值

        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))  # 设置透明度

        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons()  # 在新的背景上重绘四个按钮

        pygame.display.update()  # 更新屏幕

        FPSCLOCK.tick(FPS)  # 设置帧率

    bgColor = newBgColor  # 赋值新的背景色


# 游戏结束动画
def gameOverAnimation(color=WHITE, animationSpeed=50):

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()

    # 同时播放所有的四个音效
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()

    r, g, b = color

    for i in range(3):  # 闪动3次背景
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # 在循环中第一次是将透明度从0到255，step为1；第二次是从255到0，step为-1，依此下去
            for alpha in range(start, end, animationSpeed * step):
                # alpha 为透明度. 255为不透明, 0为透明
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


# 根据像素坐标获得点击的按钮
def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW
    elif BLUERECT.collidepoint((x, y)):
        return BLUE
    elif REDRECT.collidepoint((x, y)):
        return RED
    elif GREENRECT.collidepoint((x, y)):
        return GREEN
    return None


if __name__ == '__main__':
    main()
