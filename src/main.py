import pygame, sys, time
import entities
from pygame.locals import *

pygame.init()

RIGHT, LEFT = 0, 1
START, STOP = 0, 1
screenSize = width, height = 800, 600
clock = pygame.time.Clock()
localTime = time.time()
space = pygame.image.load("C:\casteluc\coding\spaceInvaders\img\space.png")

# Creates the screen and its caption
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Space Invaders")

# Defines the entities variables
ship = entities.Ship(64, (width // 2), (height - 120), 5)
bullets = []
shipImg = pygame.image.load("C:\casteluc\coding\spaceInvaders\img\ship.png")

# Creates the enemies matrix
enemies = []
nRows, nColumns = 5, 8
enemiesX, enemiesY = 50, 50
enemySize = 40
for i in range(nRows):
    row = []
    for j in range(nColumns):
        row.append(entities.Enemy(64, enemiesX * 2 + (j * enemiesX * 1.5), enemiesY + (i * enemiesY), 1))
    enemies.append(row)
goingRight = True


# First fills the screen with black and then call the draw functions of
# all the entities in the game
def renderScreen():
    screen.blit(space, (0, 0))
    ship.draw(screen)
    # ship.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for i in range(nRows):
        for j in range(nColumns):
            enemy = enemies[i][j]
            if enemy.isAlive:
                enemy.draw(screen)
    pygame.display.update()

# Main loop
while True:
    # Defines the game FPS
    clock.tick(60)

    # Adds ammo to the ship in intervals of 1 second
    if time.time() - localTime >= 1:
        localTime = time.time()
        ship.hasAmmo = True

    # Checks for the events in a list of events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Checks if the right and left keys are pressed, if so, moves
    # the ship in the current direction
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT] and ship.x + 64 < width:
        ship.move(RIGHT)
    elif keys[K_LEFT] and ship.x > 0:
        ship.move(LEFT)
    if keys[K_SPACE] and ship.hasAmmo:
        bullets.append(entities.Bullet(ship))
        ship.hasAmmo = False
    
    # Checks which side the enemies must go (if they had hit the border)
    if enemies[0][nColumns - 1].x >= width - (enemiesX + enemySize):
        goingRight = False
    if enemies[0][0].x < enemiesX:
        goingRight = True

    # Moves all the enemies
    for i in range(nRows):
        for j in range(nColumns):
            enemy = enemies[i][j]
            if goingRight:
                enemy.move(RIGHT)
                enemy.previousDirection = enemy.direction
                enemy.direction = RIGHT
            else:
                enemy.move(LEFT)
                enemy.previousDirection = enemy.direction
                enemy.direction = LEFT
    
    # Moves the enemies down if their direction has changed
    if enemy.direction != enemy.previousDirection:
        for i in range(nRows):
            for j in range(nColumns):
                enemy = enemies[i][j]
                enemy.moveDown()
    
    # Moves each bullet and remove the ones which are of the screen
    for bullet in bullets:
        if bullet.inScreen:
            bullet.move()
        else:
            bullets.remove(bullet)
    
    # Checks for bullet collision with enemies
    # bullet.hasCollided is used to chech if the bullet has already collided
    # with an enemy ship, without the game would crash because the bullet could
    # collid with to enemies at the same time
    for bullet in bullets:
        for i in range(nRows):
            for j in range(nColumns):
                enemy = enemies[i][j]
                if bullet.collidedWith(enemy) and enemy.isAlive and bullet.hasCollided == False:
                    if not bullet.hasCollided:
                        bullets.remove(bullet)
                        bullet.hasCollided = True
                    enemy.isAlive = False

    renderScreen()