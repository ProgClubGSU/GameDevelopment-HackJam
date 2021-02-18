import time
import sys

from sprites import *

pygame.init()
frames_per_sec = pygame.time.Clock()
# Planned 20 x 20 block space with each ground block being 30 px

# Setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, (0, 0, 0))

# background = pygame.image.load("assets/background.png")
DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURF.fill((0, 0, 0))
pygame.display.set_caption("2D Platformer")

# generate level from text file and instantiate all sprites
player_character, enemies, environment, enemy_boundaries, goal = level_generate()


def quit_game():
    for entity in environment:
        entity.kill()

    time.sleep(2)
    pygame.quit()
    sys.exit()


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()

    # DISPLAY_SURF.blit(background, (0, 0))
    DISPLAY_SURF.fill((0, 0, 0))

    # render all things
    for entity in environment:
        DISPLAY_SURF.blit(entity.image, entity.rect)

    for enemy in enemies:
        DISPLAY_SURF.blit(enemy.image, enemy.rect)
        enemy.move()

    DISPLAY_SURF.blit(player_character.image, player_character.rect)
    player_character.move()
    # end rendering

    if pygame.sprite.collide_rect(player_character, goal):
        time.sleep(0.5)

        DISPLAY_SURF.fill((0, 255, 0))
        DISPLAY_SURF.blit(game_over, (30, 250))
        pygame.display.update()
        quit_game()

    if pygame.sprite.spritecollideany(player_character, enemies):
        time.sleep(0.5)

        DISPLAY_SURF.fill((255, 0, 0))
        DISPLAY_SURF.blit(game_over, (30, 250))

        pygame.display.update()
        quit_game()

    for entity in enemies:
        if pygame.sprite.spritecollideany(entity, enemy_boundaries):
            entity.moving_right = not entity.moving_right

    hits = pygame.sprite.spritecollide(player_character, environment, False)
    if hits:
        player_character.rect.y = hits[0].rect.top + 1
        player_character.vel.y = 0

    pygame.display.update()
    frames_per_sec.tick(FPS)
