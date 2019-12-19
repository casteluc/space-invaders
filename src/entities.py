import pygame
from pygame.locals import *

FRIEND, ENEMY = 0, 1
UP, DOWN = 1, -1
START, STOP = 0, 1
RIGHT, LEFT = 0, 1

shipImg = pygame.image.load("C:\casteluc\coding\spaceInvaders\img\ship.png")
enemyImg = pygame.image.load("C:\casteluc\coding\spaceInvaders\img\enemy.png")

class Ship():
    def __init__(self, size, x, y, speed):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.hasAmmo = False
        self.isAlive = True
        self.hitBox = (self.x + 7, self.y + 5, 50, 54)

    # Moves the ship and updates its hitbox
    def move(self, direction):
        if direction == RIGHT:
            self.x += self.speed
        else:
            self.x -= self.speed
        self.hitBox = (self.x + 7, self.y + 5, 50, 54)

    # Draws the ship in the screen
    def draw(self, screen):
        screen.blit(shipImg, (self.x, self.y))  

class Enemy(Ship):
    def __init__(self, size, x, y, speed):
        super().__init__(size, x, y, speed)
        self.direction = RIGHT
        self.previousDirection = LEFT
        self.hitBox = (self.x + 3, self.y + 8, 57, 45)

    # Move the enemy ship and updates its hitbox
    def move(self, direction):
        if direction == RIGHT:
            self.x += self.speed
        elif direction == LEFT:
            self.x -= self.speed
        elif direction == DOWN:
            self.y += 10
        self.hitBox = (self.x + 3, self.y + 8, 57, 45)
        
    # Draw enemy on screen
    def draw(self, screen):
        screen.blit(enemyImg, (self.x, self.y))

class Bullet():
    def __init__(self, ship, direction, shooter):
        self.size = (2, 20)
        self.surface = pygame.Surface(self.size)
        self.surface.fill((255, 255, 255))
        self.x = ship.x + (32)
        self.y = ship.y
        self.speed = 5
        self.inScreen = True
        self.hasCollided = False
        self.direction = direction
        self.shooter = shooter
        if self.shooter == ENEMY:
            self.surface.fill((255, 0, 0))

    # Moves the bullet and checks if its of the screen
    def move(self):
        if self.y + 10 > 0 or self.y + 10 > 600:
            self.y -= self.speed * self.direction
        else:
            self.inScreen = False
    
    # Draws the bullet in the screen
    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))
    
    # Checks if the bullet collided with an enemy. Returns True 
    # if it collided and False if not
    def collidedWith(self, ship):
        onWidth = self.x < ship.hitBox[0] + ship.hitBox[2] - 1 and self.x > ship.hitBox[0] - 2
        onHeight = self.y < ship.hitBox[1] + ship.hitBox[3] and self.y + 20 > ship.hitBox[1]
        if onWidth and onHeight:
            return True
        else:
            return False