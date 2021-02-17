import time

import pygame, sys
from pygame.locals import *
import random

pygame.init()
FPS = 60
frames_per_sec = pygame.time.Clock()

# Other Variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, (0, 0, 0))

background = pygame.image.load("assets/background.png")
DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURF.fill((0, 0, 0))
pygame.display.set_caption("2D Platformer")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/enemy_set.png")
        self.surf = pygame.Surface((50, 80))
        self.rect = self.surf.get_rect(center=(random.randint(40, 360), 0))

    def move(self):
        self.rect.move_ip()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player_character.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center=(160, 520))

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Creating Sprite Groups
player_character = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player_character)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        DISPLAY_SURF.blit(background, (0, 0))

        for entity in all_sprites:
            DISPLAY_SURF.blit(entity.image, entity.rect)
            entity.move()

        if pygame.sprite.spritecollideany(player_character, enemies):
            time.sleep(0.5)

            DISPLAY_SURF.fill((255, 0, 0))
            DISPLAY_SURF.blit(game_over, (30, 250))

            pygame.display.update()
            for entity in all_sprites:
                entity.kill()

            time.sleep(2)
            pygame.quit()
            sys.exit()
        pygame.display.update()
        frames_per_sec.tick(FPS)