import pygame


class Player:
    JUMP_HEIGHT = 5
    MAXIMUM_JUMP_HEIGHT = 20 * JUMP_HEIGHT

    HORIZONTAL_ACCELERATION_VALUE = 0.5
    HORIZONTAL_ACCELERATION_MIN = -3 * HORIZONTAL_ACCELERATION_VALUE
    HORIZONTAL_ACCELERATION_MAX = 3 * HORIZONTAL_ACCELERATION_VALUE
    HORIZONTAL_ACCELERATION_UPPER_LIMIT = 20 * HORIZONTAL_ACCELERATION_VALUE
    HORIZONTAL_ACCELERATION_LOWER_LIMIT = -1 * HORIZONTAL_ACCELERATION_UPPER_LIMIT

    def __init__(self):
        self.x = 300
        self.y = 300
        self.horizontal_acceleration = 0.0
        self.jump_available = True
        self.currently_jumping = False
        self.jump_height = 0  # TMP do wywalenia, potem sprawdzamy czy dotyka czegos

        # self.image = pygame.Surface((20, 20))
        # self.image.fill((255, 0, 0))
        self.image = pygame.image.load("sprites/player/idle1.png")

    def calculate_move(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            self.accelerate_left()
        elif key_pressed[pygame.K_RIGHT]:
            self.accelerate_right()
        else:
            self.decrease_acceleration()

        if key_pressed[pygame.K_SPACE]:
            self.proceed_jump()

    def move_player(self, key_pressed):
        self.calculate_move(key_pressed)
        self.x += self.horizontal_acceleration
        self.jump()

    def jump(self):
        if self.jump_available:
            return
        if self.currently_jumping:
            self.y -= self.JUMP_HEIGHT
            self.jump_height += self.JUMP_HEIGHT
            if self.jump_height > self.MAXIMUM_JUMP_HEIGHT:
                self.currently_jumping = False
        else:
            self.y += self.JUMP_HEIGHT
            self.jump_height -= self.JUMP_HEIGHT
            if self.jump_height <= 0:
                self.jump_available = True

    def accelerate_right(self):
        self.horizontal_acceleration += self.HORIZONTAL_ACCELERATION_VALUE
        self.horizontal_acceleration = min(self.horizontal_acceleration, self.HORIZONTAL_ACCELERATION_UPPER_LIMIT)

    def accelerate_left(self):
        self.horizontal_acceleration -= self.HORIZONTAL_ACCELERATION_VALUE
        self.horizontal_acceleration = max(self.horizontal_acceleration, self.HORIZONTAL_ACCELERATION_LOWER_LIMIT)

    def decrease_acceleration(self):
        if self.HORIZONTAL_ACCELERATION_MIN < self.horizontal_acceleration < self.HORIZONTAL_ACCELERATION_MAX:
            self.horizontal_acceleration = 0
        elif self.horizontal_acceleration >= self.HORIZONTAL_ACCELERATION_MAX:
            self.horizontal_acceleration -= self.HORIZONTAL_ACCELERATION_VALUE
        else:
            self.horizontal_acceleration += self.HORIZONTAL_ACCELERATION_VALUE

    def proceed_jump(self):
        if self.jump_available:
            self.jump_available = False
            self.currently_jumping = True

    def get_position(self):
        return self.x, self.y
