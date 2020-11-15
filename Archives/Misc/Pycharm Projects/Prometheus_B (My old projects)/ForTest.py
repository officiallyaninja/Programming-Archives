import pygame
import random
pos = [0, 0]
inc = 0
choice = 0
i = 0
freq = 10000


# initializing pygame
pygame.init()

# creating the  game window
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 400
playerY = 500


def player(x, y):
    screen.blit(playerImg, (x, y))


# main game loop

running = True
while running:
    x = random.randint(0, 3)
    if x == 0:
        pos[0] += 1
    elif x == 1:
        pos[0] += -1
    elif x == 2:
        pos[1] += 1
    elif x == 3:
        pos[1] += -1
    if pos == [0, 0]:
        inc += 1
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player(playerX, playerY)
    pygame.display.update()
