import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 1000, 700

win = pygame.display.set_mode((W, H))
pygame.display.set_caption('OSO GA EME')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()
black = (0, 0, 0)
white = (255, 255, 255)
menman = pygame.image.load(os.path.join('images', '1menu.png'))
btnb = (0, 217, 250)
btnb2 = (178, 229, 237)
btnr = (242, 82, 112)
btnr2 = (230, 135, 153)
btnl = (190, 255, 77)
btnl2 = (215, 247, 158)


clock = pygame.time.Clock()


class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')),
             pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.hitbox = (self.x + x, self.y +y, self.width - width, self.height - height)



    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))

        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 6, self.y +5, self.width - 38, self.height - 20)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x + 5, self.y +30, self.width - 10, self.height - 40)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x +5, self.y +30, self.width - 10, self.height - 40)

            if self.slideCount >= 85:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x + 20, self.y + 40, self.width - 30, self.height - 40)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 6, self.y + 5, self.width - 38, self.height - 15)
        pygame.draw.rect(win, (255,0,0),self.hitbox, 2)



class spike(object):
    img = pygame.image.load(os.path.join('images', 'spikeA.png'))
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4



    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        win.blit(self.img, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False



def updateFile():
    f = open('database.txt', 'r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('database.txt', 'w')
        file.write(str(score))
        file.close()

        return score

    return last
def button(txt,x,y,bw,bh,ca,cb,event=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + bw > mouse[0] > x and y + bh > mouse[1] > y:
        pygame.draw.rect(win, cb, (x, y, bw, bh))
        if click[0] == 1 and event != None:
            if event == 'go':
                game_loop()
            if event == 'quit':
                pygame.quit()
            if event == 'about':
                aboutscreen()
            if event == 'back':
                introscreen()
    else:
        pygame.draw.rect(win, ca, (x, y, bw, bh))
    smallfont = pygame.font.SysFont('comicsans', 20)
    TextSurf, TextRect = text_objects(txt, smallfont)
    TextRect.center = ((x+(bw/ 2)), (y+(bh/2)))
    win.blit(TextSurf, TextRect)

def introscreen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        x = (W * 0.2)
        y = (H * 0.3)
        win.fill(white)
        win.blit(menman, (x, y))
        largeFont = pygame.font.SysFont('comicsans', 120)
        TextSurf, TextRect = text_objects("Oso Ga Eme!!!", largeFont)
        TextRect.center = ((W / 2), (H / 4))
        win.blit(TextSurf, TextRect)
        button("START GAME", 650, 300, 150, 50, btnb, btnb2, 'go')
        button("QUIT", 650, 400, 150, 50, btnb, btnb2, 'quit')
        button("ABOUT", 650, 500, 150, 50, btnb, btnb2, 'about')

        pygame.display.update()
        clock.tick(15)

def aboutscreen():
    about = True
    while about:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        x = (W * 0.2)
        y = (H * 0.3)
        win.fill(white)
        largeFont = pygame.font.SysFont('comicsans', 40)
        TextSurf, TextRect = text_objects("This game was built by Nnamani Chijindu Ikenna", largeFont)
        TextRect.center = ((W / 2), (H / 2))
        win.blit(TextSurf, TextRect)
        button("BACK", 750, 600, 150, 50, btnb, btnb2, 'back')


        pygame.display.update()
        clock.tick(15)



def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 30
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = True
                runner.falling = False
                runner.sliding = False
                runner.jumpin = False

        win.blit(bg, (0, 0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()), 1, (255, 255, 255))
        currentScore = largeFont.render('Score: ' + str(score), 1, (255, 255, 255))
        win.blit(lastScore, (W / 2 - lastScore.get_width() / 2, 150))
        win.blit(currentScore, (W / 2 - currentScore.get_width() / 2, 240))
        pygame.display.update()
    score = 0


def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    text = largeFont.render('Score: ' + str(score), 1, (255, 255, 255))
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)

    win.blit(text, (700, 10))
    pygame.display.update()
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()



obstacles = []
def game_loop():
    pygame.time.set_timer(USEREVENT + 1, 500)
    pygame.time.set_timer(USEREVENT + 2,random.randrange(3000,6000))

    speed = 30
    global score
    score = 0

    run = True
    global runner
    runner = player(200, 480, 64, 64)


    pause = 0
    fallSpeed = 0

    while run:
        if pause > 0:
            pause += 1
            if pause > fallSpeed * 2:
                endScreen()

        score = speed // 10 - 3

        for obstacle in obstacles:
            if obstacle.collide(runner.hitbox):
                runner.falling = True

                if pause == 0:
                    pause = 1
                    fallSpeed = speed
            if obstacle.x < -64:
                obstacles.pop(obstacles.index(obstacle))
            else:
                obstacle.x -= 1.4

        global bgX
        bgX -= 1.4
        global bgX2
        bgX2 -= 1.4

        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == USEREVENT + 1:
                speed += 1

            if event.type == USEREVENT + 2:
                r = random.randrange(0, 2)
                if r == 0:
                    obstacles.append(spike(1010, 440, 64, 64))
                elif r == 1:
                    obstacles.append(spike(1010, 480, 64, 64))

        if runner.falling == False:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not (runner.jumping):
                    runner.jumping = True

            if keys[pygame.K_DOWN]:
                if not (runner.sliding):
                    runner.sliding = True

        clock.tick(speed)
        redrawWindow()
introscreen()
game_loop()
endScreen()