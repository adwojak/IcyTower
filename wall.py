from platform import PlatformGenerator

import pygame

from constants import (
    GAME_HEIGHT,
    GAME_WIDTH,
    PLATFORM_ELEMENT_HEIGHT,
    PLATFORM_ELEMENT_WIDTH,
    WALL_BLOCK_HEIGHT,
    WALL_BLOCK_SPRITE,
    WALL_BLOCK_WIDTH,
)


class WallBlock(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, collision_side):
        super().__init__()
        self.x = x_position
        self.y = y_position
        self.collision_side = collision_side
        self.surface = pygame.Surface((WALL_BLOCK_WIDTH, WALL_BLOCK_HEIGHT))
        self.surface.blit(pygame.image.load(WALL_BLOCK_SPRITE), (0, 0))
        self.rect = self.get_rect()
        pygame.draw.rect(self.surface, (255, 0, 0), self.surface.get_rect(), 1)

    def get_rect(self):
        rect = self.surface.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect

    def get_position(self):
        return self.x, self.y

    def draw(self, base_surface):
        base_surface.blit(self.surface, self.get_position())


class Background(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.append_base_platform()
        self.append_wall_blocks()

    def append_base_platform(self):
        self.add(
            PlatformGenerator.generate_single_platform(
                0, GAME_HEIGHT - PLATFORM_ELEMENT_HEIGHT, GAME_WIDTH // PLATFORM_ELEMENT_WIDTH
            )
        )

    def append_wall_blocks(self):
        for block_counter in range(GAME_HEIGHT // WALL_BLOCK_HEIGHT + 1):
            self.add(WallBlock(0, WALL_BLOCK_HEIGHT * block_counter, "right"))
            self.add(WallBlock(GAME_WIDTH - WALL_BLOCK_WIDTH, WALL_BLOCK_HEIGHT * block_counter, "left"))

    def draw(self, base_surface):
        for sprite in self.sprites():
            sprite.draw(base_surface)
