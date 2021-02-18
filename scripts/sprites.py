import random
import pygame
import os

from pygame.locals import *
from settings import *

vec = pygame.math.Vector2


# TODO: Figure out how PyGame rect's work when it comes to collisions
class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'GroundTile.png')).convert()
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.pos = vec((xloc, yloc))


class InvisibleBarrier(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect()
        self.pos = vec((xloc, yloc))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'GothicEnemy0{0}.png'.format(img))).convert()
        self.surf = pygame.Surface((50, 80))  # TODO: Correct sizes
        self.rect = self.surf.get_rect()

        self.pos = vec((xloc, yloc))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.moving_right = True

    def move(self):
        self.acc = vec(0, 0)
        if self.moving_right:
            self.rect.move_ip(5, 0)
        elif not self.moving_right:
            self.rect.move_ip(-5, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc):
        super().__init__()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec((xloc, yloc))

        self.image = pygame.image.load(os.path.join('assets', 'Wizard.png')).convert()
        self.surf = pygame.Surface((40, 75))  # TODO: Correct sizes
        self.rect = self.surf.get_rect()

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH

        self.rect.midbottom = self.pos


class Goal(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc):
        super().__init__()
        self.pos = vec((xloc, yloc))

        self.image = pygame.image.load(os.path.join('assets', 'PlatformerTiles.png')).convert()
        self.surf = pygame.Surface((25, 25))
        self.rect = self.surf.get_rect()


def level_generate():
    environment = pygame.sprite.Group()
    player_character = None
    enemies = pygame.sprite.Group()
    invisible_barrier = pygame.sprite.Group()
    goal = None

    level_file = open("level.txt", encoding="utf-8")

    level_line_no = 0

    for levelLine in level_file.readlines():
        level_line_split = list(levelLine)
        for i in range(30):
            if level_line_split[i] == "#":  # wall
                environment.add(Platform(3+i*17+8, 30+level_line_no*17+8))
            elif level_line_split[i] == "@":  # player start position
                player_character = Player(3+i*17+8, 30+level_line_no*17+8)
            elif level_line_split[i] == "&":  # enemy start position
                enemies.add(Enemy(3+i*17+8, 30+level_line_no*17+8, random.randint(1, 3)))
            elif level_line_split[i] == "_":  # invisible enemy barrier
                invisible_barrier.add(InvisibleBarrier(3+i*17+8, 30+level_line_no*17+8))
            elif level_line_split[i] == "*":  # goal
                goal = Goal(3+i*17+8, 30+level_line_no*17+8)
        level_line_no += 1

    level_file.close()

    return player_character, enemies, environment, invisible_barrier, goal
