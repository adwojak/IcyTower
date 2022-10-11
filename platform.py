from random import randint

from pygame import Surface
from pygame.font import Font
from pygame.image import load as load_image
from pygame.sprite import Sprite
from pygame.transform import flip

from constants import (
    BASE_PLATFORM_SPEED,
    COLLISION_SIDE_TOP,
    COLOR_RED,
    FONT_SIZE,
    GAME_HEIGHT,
    GAME_WIDTH,
    NEW_PLATFORM_GENERATION_HEIGHT,
    PLATFORM_ELEMENT_HEIGHT,
    PLATFORM_ELEMENT_WIDTH,
    PLATFORM_MIDDLE,
    PLATFORM_START,
    WALL_BLOCK_WIDTH,
)

LEFT_SIDE_IMAGE = load_image(PLATFORM_START)
MIDDLE_IMAGE = load_image(PLATFORM_MIDDLE)
RIGHT_SIDE_IMAGE = flip(LEFT_SIDE_IMAGE, True, False)


class Platform(Sprite):
    def __init__(
        self,
        x_position,
        y_position,
        middle_repeats,
        platform_level,
    ):
        super().__init__()
        self.x = x_position
        self.y = y_position
        self.collision_side = COLLISION_SIDE_TOP
        self.left_side_image = LEFT_SIDE_IMAGE
        self.middle_image = MIDDLE_IMAGE
        self.right_side_image = RIGHT_SIDE_IMAGE
        self.platform_level = platform_level
        self.platform_width = PLATFORM_ELEMENT_WIDTH * (middle_repeats + 2)
        self.image = self.generate_platform(middle_repeats)
        self.rect = self.get_rect()
        self.font = Font(None, FONT_SIZE)
        self.text = self.generate_text()

    def generate_platform(self, middle_repeats):
        surface = Surface((self.platform_width, PLATFORM_ELEMENT_HEIGHT))
        surface.blit(self.left_side_image, (0, 0))
        for element in range(middle_repeats):
            surface.blit(self.middle_image, ((element + 1) * PLATFORM_ELEMENT_WIDTH, 0))
        surface.blit(self.right_side_image, (self.platform_width - PLATFORM_ELEMENT_WIDTH, 0))
        return surface

    def get_rect(self):
        rect = self.image.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect

    def get_position(self):
        return self.x, self.y

    def update_vertical(self, value):
        self.y += value
        self.rect.y += value

    def generate_text(self):
        return self.font.render(str(self.platform_level), True, COLOR_RED)

    def update(self):
        if self.y > GAME_HEIGHT:
            self.kill()
        self.update_vertical(BASE_PLATFORM_SPEED)
        self.image.blit(self.text, ((self.platform_width - self.text.get_width()) // 2, 10))


def generate_platform_parameters():
    middle_repeats = randint(2, 8)
    platform_width = PLATFORM_ELEMENT_WIDTH * (middle_repeats + 2)
    platform_x = randint(WALL_BLOCK_WIDTH + 5, GAME_WIDTH - WALL_BLOCK_WIDTH - 5 - platform_width)
    return platform_x, middle_repeats


def generate_starting_platforms():
    platforms = [Platform(0, GAME_HEIGHT - PLATFORM_ELEMENT_HEIGHT, GAME_WIDTH // PLATFORM_ELEMENT_WIDTH, 0)]
    for count in range(1, 4):
        platform_x, middle_repeats = generate_platform_parameters()
        platforms.append(
            Platform(
                platform_x,
                GAME_WIDTH - 160 * count,
                middle_repeats,
                platforms[-1].platform_level + 1,
            )
        )
    return platforms


def generate_new_platforms(platforms_group):
    if len(platforms_group) < 4:
        platform_x, middle_repeats = generate_platform_parameters()
        platforms_group.add(
            Platform(
                platform_x,
                NEW_PLATFORM_GENERATION_HEIGHT,
                middle_repeats,
                platforms_group.sprites()[-1].platform_level + 1,
            )
        )
