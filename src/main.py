import pygame, sys, time, random
import entities
from pygame.locals import *

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

FRIEND, ENEMY = 0, 1
UP, DOWN = 1, -1
RIGHT, LEFT = 0, 1
START, STOP = 0, 1

# Starts clock and stores the current time
clock = pygame.time.Clock()
localTime = time.time()

# Loads all the game sounds
shipShooting = pygame.mixer.Sound("C:\casteluc\coding\spaceInvaders\sounds\shipShooting.wav")
enemyShooting = pygame.mixer.Sound("C:\casteluc\coding\spaceInvaders\sounds\enemyShooting.wav")
gameOverVoice = pygame.mixer.Sound("C:\casteluc\coding\spaceInvaders\sounds\gameOver.wav")
explosionSound = pygame.mixer.Sound("C:\casteluc\coding\spaceInvaders\sounds\explosion.wav")

# Loads and plays music infinetly 
pygame.mixer.music.load("C:\casteluc\coding\spaceInvaders\sounds\music.wav")
pygame.mixer.music.play(-1)

# Creates the screen and its caption
screenSize = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Space Invaders")
space = pygame.image.load("C:\casteluc\coding\spaceInvaders\img\space.png")


# Defines the entities variables
ship = entities.Ship(64, (WIDTH // 2), (HEIGHT - 120), 5)
bullets = []
score = 0

# Creates the enemies matrix
enemies = []
nRows, nColumns = 5, 8
enemiesX, enemiesY = 50, 50
enemySize = 40
for i in range(nRows):
    row = []
    for j in range(nColumns):
        # Enemies on the first and second rows have 2 lives
        if i <= 1:
            row.append(entities.Enemy(64, enemiesX * 2 + (j * enemiesX * 1.5), enemiesY + (i * enemiesY), 1, 2))
        # Enemies after the second row have only 1 life
        else:
            row.append(entities.Enemy(64, enemiesX * 2 + (j * enemiesX * 1.5), enemiesY + (i * enemiesY), 1, 1))
    enemies.append(row)
goingRight = True

def gameOver():
    # Brief time sleep before showing the game over screen
    time.sleep(2)

    # Making text 1 "GAME OVER"
    font = pygame.font.Font('freesansbold.ttf', 72) 
    text = font.render('GAME OVER', True, (255, 255, 255)) 
    textRect = text.get_rect()
    textRect.center = (WIDTH/2, HEIGHT/2)

    # Stops the music and says "game over"
    pygame.mixer.music.stop()
    gameOverVoice.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # Renderizing the screen
        screen.fill((0, 0, 0))
        screen.blit(text, textRect)
        pygame.display.update()

# Defines the enemy shooting actions
def enemyShoot():
    # Picks the enemies that are in the last row of the matriz
    enemyFront = [None] * nColumns
    for i in range(nRows):
        for j in range(nColumns):
            enemy = enemies[i][j]
            if enemy.life > 0:
                enemyFront[j] = enemy
    
    # Checks if there were any empty columns, if so, these ones
    # are removed from the enemy front
    cleanEnemyFront = []
    for enemy in enemyFront:
        if enemy != None:
            cleanEnemyFront.append(enemy)

    # Checks if there are still enemies alive and makes a random enemy of
    # the enemy front shoot
    if len(cleanEnemyFront) > 0:
        shootingEnemy = random.randint(0, len(cleanEnemyFront) - 1)
        bullets.append(entities.Bullet(cleanEnemyFront[shootingEnemy], DOWN, ENEMY))
        enemyShooting.play()
    else:
        gameOver()
        
# First fills the screen with black and then call the draw functions of
# all the entities in the game
def renderScreen():
    screen.blit(space, (0, 0))
    ship.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for i in range(nRows):
        for j in range(nColumns):
            enemy = enemies[i][j]
            if enemy.life > 0:
                enemy.draw(screen)
    screen.blit(text, textRect)
    pygame.display.update()

# Main loop
time.sleep(1)
while True:
    # Defines the game FPS
    clock.tick(60)

    # Adds ammo to the ship in intervals of 1 second
    if time.time() - localTime >= 1:
        localTime = time.time()
        ship.hasAmmo = True
        enemyShoot()
        enemyShoot()

    # Checks for the events in a list of events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Checks if the right and left keys are pressed, if so, moves
    # the ship in the current direction
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT] and ship.hitBox[0] + 64 < WIDTH:
        ship.move(RIGHT)
    elif keys[K_LEFT] and ship.hitBox[0] > 0:
        ship.move(LEFT)
    if keys[K_SPACE] and ship.hasAmmo:
        bullets.append(entities.Bullet(ship, UP, FRIEND))
        shipShooting.play()
        ship.hasAmmo = False
    
    # Checks which side the enemies must go (if they had hit the border)
    if enemies[0][nColumns - 1].x >= WIDTH - (enemiesX + enemySize):
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
                enemy.move(DOWN)
    
    # Moves each bullet and remove the ones which are of the screen
    for bullet in bullets:
        if bullet.inScreen:
            bullet.move()
        else:
            bullets.remove(bullet)

    # Checks for bullet collision with enemies
    # bullet.hasCollided is used to check if the bullet has already collided
    # with an enemy ship, without the game would crash because the bullet could
    # collid with to enemies at the same time. In the else is checked if any 
    # bullet has collided with the player ship
    for bullet in bullets:
        if bullet.shooter == FRIEND:
            for i in range(nRows):
                for j in range(nColumns):
                    enemy = enemies[i][j]
                    if bullet.collidedWith(enemy) and enemy.life > 0 and bullet.hasCollided == False:
                        if not bullet.hasCollided:
                            bullets.remove(bullet)
                            bullet.hasCollided = True
                            score += 10
                        enemy.life -= 1
                        explosionSound.play()
        else:
            if bullet.collidedWith(ship):
                ship.isAlive = False
                explosionSound.play()
                gameOver()

    # Loads and configures the score text
    font = pygame.font.Font('freesansbold.ttf', 20) 
    text = font.render('Score: %d' % score, True, (255, 255, 255)) 
    textRect = text.get_rect()
    textRect.center = (60, 20)

    renderScreen()