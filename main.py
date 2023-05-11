import pygame
import sys

from math_tools import *


pygame.init()

infoObject = pygame.display.Info()
W_SIZE = WIDTH, HEIGHT = (infoObject.current_w, infoObject.current_h)
H_SIZE = H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

screen = pygame.display.set_mode(W_SIZE, pygame.FULLSCREEN)
display = pygame.Surface(W_SIZE)
clock = pygame.time.Clock()
FPS = 60


class Object:
    def __init__(
        self,
        screen: pygame.Surface,
        color: tuple,
        radius: int | float
    ):
        self.screen = screen
        self.radius = radius

        self.image = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.image.set_colorkey((0, 0, 0))
    
    def update(self):
        pass
    
    def draw(self, x, y):
        self.screen.blit(self.image, (x - self.radius, y - self.radius))

    def get_offset(self):
        return 0, 0


class MovingObject(Object):
    def __init__(
        self,
        screen: pygame.Surface,
        color: tuple,
        radius: int | float,
        movement_radius: int | float,
        angle: int | float,
        main_object: Object
    ):
        super().__init__(screen, color, radius)
        self.movement_radius = movement_radius
        self.angle = angle
        self.main_object = main_object

        self.vec = Vector(-self.movement_radius, 0)

        self.image = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.image.set_colorkey((0, 0, 0))

    def update(self):
        self.vec.rotate(self.angle)
    
    def draw(self, offset_x, offset_y):
        main_x, main_y = self.get_offset()
        self.screen.blit(self.image, (main_x + offset_x - self.radius, main_y + offset_y - self.radius))
        pass
    
    def get_offset(self):
        x, y = self.main_object.get_offset()
        return int(self.vec.x + x), int(self.vec.y + y)


rotate_speed = 365
length = 1

sun = Object(display, (253, 184, 19), 5)
earth = MovingObject(display, (0, 184, 34), 3, length * 151, rotate_speed / 365, sun)
mars = MovingObject(display, (253, 104, 19), 3, length * 250, rotate_speed / 687, sun)
moon = MovingObject(display, (200, 200, 200), 2, length * 40, rotate_speed / 30, earth)

objects_ = [sun, mars, moon, earth]

while True:
    display.fill((0, 0, 0))
    display.set_colorkey((0, 0, 0))
    screen.fill((0, 0, 0))

    mouse_pos = mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for obj in objects_:
        obj.update()
    
    x, y = earth.get_offset()
    earth.draw(H_WIDTH - x, H_HEIGHT - y)
    for obj in objects_[:-1]:
        obj.draw(H_WIDTH - x, H_HEIGHT - y)
    
    screen.blit(display, (0, 0))
    pygame.display.update()
    clock.tick(FPS)