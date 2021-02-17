import random
import pygame
import os

from pygame.locals import *


# TODO: Figure out how PyGame rect's work when it comes to collisions
class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc):
        super().__init__()
        self.image = pygame.image.load("assets/PlatformerTiles.png")
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc


class InvisibleBarrier(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc


class Enemy(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', img)).convert()
        self.surf = pygame.Surface((50, 80))  # TODO: Correct sizes
        self.rect = self.surf.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
        self.moving_right = True

    def move(self):
        if self.moving_right:
            self.rect.move_ip(5, 0)
        elif not self.moving_right:
            self.rect.move_ip(-5, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, right_bound):
        super().__init__()
        self.image = pygame.image.load("assets/player_character.png")
        self.surf = pygame.Surface((40, 75))  # TODO: Correct sizes
        self.rect = self.surf.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
        self.right_bound = right_bound

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < self.right_bound:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
