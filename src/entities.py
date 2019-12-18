import pygame
from pygame.locals import *

START, STOP = 0, 1
RIGHT, LEFT = 0, 1

class Ship():

    def __init__(self, size, x, y, speed):
        self.size = size
        self.surface = pygame.Surface((size, size))
        self.surface.fill((255, 255, 255))
        self.x = x
        self.y = y
        self.speed = speed
        self.hasAmmo = False
    
    # Adds ammo to the ship
    def getAmmo(self, num):
        self.ammo += num

    # Moves the ship according to its speed
    def move(self, direction):
        if direction == RIGHT:
            self.x += self.speed
        else:
            self.x -= self.speed

    # Draws the ship in the screen
    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))
    
        

class Enemy(Ship):
    def __init__(self, size, x, y, speed):
        super().__init__(size, x, y, speed)
        self.surface.fill((255, 0, 0))
        self.isAlive = True
        self.direction = RIGHT
        self.previousDirection = LEFT

    # Moves the enemy ship down
    def moveDown(self):
        self.y += 3

class Bullet():

    def __init__(self, ship):
        self.size = (2, 20)
        self.surface = pygame.Surface(self.size)
        self.surface.fill((255, 255, 255))
        self.x = ship.x + (ship.size // 2)
        self.y = ship.y
        self.speed = 15
        self.inScreen = True

    # Moves the bullet and checks if its of the screen
    def move(self):
        if self.y + 10 > 0:
            self.y -= self.speed
        else:
            self.inScreen = False
    
    # Draws the bullet in the screen
    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))
    
    # Checks if the bullet collided with an enemy. Returns True 
    # if it collided and False if not
    def collidedWith(self, enemy):
        onWidth = self.x < enemy.x + enemy.size - 1 and self.x > enemy.x - 2
        onHeight = self.y < enemy.y + enemy.size and self.y + 20 > enemy.y
        if onWidth and onHeight:
            return True
        else:
            return False