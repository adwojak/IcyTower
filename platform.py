import pygame
import random
from constants import NEW_PLATFORM_GENERATION_HEIGHT, BASE_PLATFORM_SPEED, PLATFORM_ELEMENT_HEIGHT, PLATFORM_ELEMENT_WIDTH, PLATFORM_MIDDLE, PLATFORM_START, GAME_HEIGHT, GAME_WIDTH, WALL_BLOCK_WIDTH

LEFT_SIDE_IMAGE = pygame.image.load(PLATFORM_START)
MIDDLE_IMAGE = pygame.image.load(PLATFORM_MIDDLE)
RIGHT_SIDE_IMAGE = pygame.transform.flip(LEFT_SIDE_IMAGE, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(
        self, x_position, y_position, collision_side, middle_repeats, left_side_image, middle_image, right_side_image
    ):
        super().__init__()
        self.x = x_position
        self.y = y_position
        self.collision_side = collision_side
        self.left_side_image = left_side_image
        self.middle_image = middle_image
        self.right_side_image = right_side_image
        self.surface = self.generate_platform(middle_repeats)
        self.rect = self.get_rect()

    def generate_platform(self, middle_repeats):
        width = PLATFORM_ELEMENT_WIDTH * (middle_repeats + 2)
        surface = pygame.Surface((width, PLATFORM_ELEMENT_HEIGHT))
        surface.blit(self.left_side_image, (0, 0))
        for element in range(middle_repeats):
            surface.blit(self.middle_image, ((element + 1) * PLATFORM_ELEMENT_WIDTH, 0))
        surface.blit(self.right_side_image, (width - PLATFORM_ELEMENT_WIDTH, 0))
        return surface

    def get_rect(self):
        rect = self.surface.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect

    def get_position(self):
        return self.x, self.y

    def update_vertical(self, value):
        self.y += value
        self.rect.y += value

    def draw(self, base_surface, platform_speed):
        if self.y > GAME_HEIGHT:
            self.kill()
        self.update_vertical(platform_speed)
        base_surface.blit(self.surface, self.get_position())


class PlatformGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.initialize_platforms()

    def generate_platform_parameters(self):
        middle_repeats = random.randint(2, 8)
        platform_width = PLATFORM_ELEMENT_WIDTH * (middle_repeats + 2)
        platform_x = random.randint(WALL_BLOCK_WIDTH + 5, GAME_WIDTH - WALL_BLOCK_WIDTH - 5 - platform_width)
        return platform_x, middle_repeats

    def initialize_platforms(self):
        self.add(self.generate_platform(0, GAME_HEIGHT - PLATFORM_ELEMENT_HEIGHT, GAME_WIDTH // PLATFORM_ELEMENT_WIDTH))
        for count in range(1, 4):
            platform_x, middle_repeats = self.generate_platform_parameters()
            self.add(self.generate_platform(platform_x, GAME_WIDTH - 160 * count, middle_repeats))

    def generate_platform(self, x_position, y_position, middle_repeats):
        return Platform(x_position, y_position, "top", middle_repeats, LEFT_SIDE_IMAGE, MIDDLE_IMAGE, RIGHT_SIDE_IMAGE)

    def draw(self, base_surface):
        sprites = self.sprites()
        if len(sprites) < 4:
            platform_x, middle_repeats = self.generate_platform_parameters()
            self.add(self.generate_platform(platform_x, NEW_PLATFORM_GENERATION_HEIGHT, middle_repeats))
        for sprite in sprites:
            sprite.draw(base_surface, BASE_PLATFORM_SPEED)
