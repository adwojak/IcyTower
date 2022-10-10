from pygame import Surface
from pygame.image import load as load_image
from pygame.sprite import Group, Sprite

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
        self.surface = Surface((WALL_BLOCK_WIDTH, WALL_BLOCK_HEIGHT))
        self.surface.blit(load_image(WALL_BLOCK_SPRITE), (0, 0))
        self.rect = self.get_rect()

    def get_rect(self):
        rect = self.surface.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect

    def get_position(self):
        return self.x, self.y

    def draw(self, base_surface):
        base_surface.blit(self.surface, self.get_position())


class BackgroundGroup(Group):
    def __init__(self):
        super().__init__()
        self.append_wall_blocks()

    def append_wall_blocks(self):
        for block_counter in range(GAME_HEIGHT // WALL_BLOCK_HEIGHT + 1):
            self.add(WallBlock(0, WALL_BLOCK_HEIGHT * block_counter, COLLISION_SIDE_RIGHT))
            self.add(WallBlock(GAME_WIDTH - WALL_BLOCK_WIDTH, WALL_BLOCK_HEIGHT * block_counter, COLLISION_SIDE_LEFT))

    def draw(self, base_surface):
        for sprite in self.sprites():
            sprite.draw(base_surface)
