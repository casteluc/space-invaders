import pygame
from pygame.locals import *

START, STOP = 0, 1
RIGHT, LEFT = 0, 1

class Ship():

    def __init__(self, size, x, y, speed):
        self.size = (size, size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill((0, 255, 0))
        self.x = x
        self.y = y
        self.speed = speed
    
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
    
class Bullet():

    def __init__(self, ship):
        self.size = (2, 20)
        self.surface = pygame.Surface(self.size)
        self.surface.fill((255, 255, 255))
        self.x = ship.x + (ship.size[0] / 2)
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
    
    def collided(self, ship):
        pass
    

    
