from pygame import Surface
from pygame.image import load as load_image
from pygame.sprite import Sprite

from constants import (
    COLLISION_SIDE_LEFT,
    COLLISION_SIDE_RIGHT,
    GAME_HEIGHT,
    GAME_WIDTH,
    WALL_BLOCK_HEIGHT,
    WALL_BLOCK_SPRITE,
    WALL_BLOCK_WIDTH,
)


class WallBlock(Sprite):
    def __init__(self, x_position, y_position, collision_side):
        super().__init__()
        self.x = x_position
        self.y = y_position
        self.collision_side = collision_side
        self.image = Surface((WALL_BLOCK_WIDTH, WALL_BLOCK_HEIGHT))
        self.image.blit(load_image(WALL_BLOCK_SPRITE), (0, 0))
        self.rect = self.get_rect()

    def get_rect(self):
        rect = self.image.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect


def generate_walls():
    walls = []
    for block_counter in range(GAME_HEIGHT // WALL_BLOCK_HEIGHT + 1):
        walls.extend(
            (
                WallBlock(0, WALL_BLOCK_HEIGHT * block_counter, COLLISION_SIDE_RIGHT),
                WallBlock(GAME_WIDTH - WALL_BLOCK_WIDTH, WALL_BLOCK_HEIGHT * block_counter, COLLISION_SIDE_LEFT),
            )
        )
    return walls
