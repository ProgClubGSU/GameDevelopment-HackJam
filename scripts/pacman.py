import random
import time
import pygame
import sys

from pygame.locals import *
from sprites import *

pygame.init()
FPS = 60
frames_per_sec = pygame.time.Clock()

# Other Variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# Planned 20 x 20 block space with each ground block being 30 px

# Setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, (0, 0, 0))

background = pygame.image.load("assets/background.png")
DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURF.fill((0, 0, 0))
pygame.display.set_caption("2D Platformer")

# Creating Sprite Groups
player_character = Player()
sprites_to_render = pygame.sprite.Group()  # Floor, enemies, player
enemies = pygame.sprite.Group()
enemy_boundaries = pygame.sprite.Group()  # Invisible bounds for enemies

# TODO: ingest system from text file to level generation

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY_SURF.blit(background, (0, 0))

    for entity in sprites_to_render:
        DISPLAY_SURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(player_character, enemies):
        time.sleep(0.5)

        DISPLAY_SURF.fill((255, 0, 0))
        DISPLAY_SURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in sprites_to_render:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    for entity in enemies:
        if pygame.sprite.spritecollideany(entity, enemy_boundaries):
            entity.moving_right = not entity.moving_right

    # TODO: Player Character gravity interaction

    pygame.display.update()
    frames_per_sec.tick(FPS)
