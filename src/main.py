import pygame, sys
import entities
from pygame.locals import *

pygame.init()

RIGHT, LEFT = 0, 1
START, STOP = 0, 1
screenSize = width, height = 800, 600
clock = pygame.time.Clock()

# Creates the screen and its caption
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Space Invaders")

# Defines the entities variables
ship = entities.Ship(20, (width // 2), (height - 120), 5)
bullets = []

enemies = []
nRows, nColumns = 3, 10
enemiesX, enemiesY = 50, 60
for i in range(nColumns):
    for j in range (nRows):
        enemies.append(entities.Enemy(20, enemiesX + (i * 40), enemiesY + (j * 40), 1))

# First fills the screen with black and then call the draw functions of
# all the entities in the game
def renderScreen():
    screen.fill((0, 0, 0))
    ship.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    pygame.display.update()

# Main loop
while True:
    # Defines the game FPS
    clock.tick(60)

    # Checks for the events in a list of events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        # Creates a new bullet when the player press space
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                bullets.append(entities.Bullet(ship))

    # Checks if the right and left keys are pressed, if so, moves
    # the ship in the current direction
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        ship.move(RIGHT)
    elif keys[K_LEFT]:
        ship.move(LEFT)
    
    goingRight = True
    if enemies[nColumns - 1].x >= width - enemiesX + 20:
        goingRight = False
    for enemy in enemies:
        if goingRight:
            enemy.move(RIGHT)
        else:
            enemy.move(LEFT)
    
    # Moves each bullet and remove the ones which are of the screen
    for bullet in bullets:
        if bullet.inScreen:
            bullet.move()
        else:
            bullets.remove(bullet)
    
    for bullet in bullets:
        for enemy in enemies:
            if bullet.collidedWith(enemy):
                enemies.remove(enemy)

    renderScreen()

