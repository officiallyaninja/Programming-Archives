import pygame
import math
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


def player():
    screen.blit(playerImg, (playerX, playerY))


# main game loop

running = True
while running:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player()
    playerX += math.sqrt(abs(100 - (playerY**2)))
    playerY += math.sqrt(abs(100 - (playerX**2)))
    pygame.display.update()