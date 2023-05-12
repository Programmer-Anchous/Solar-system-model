import pygame
import sys

from math_tools import *


pygame.init()

infoObject = pygame.display.Info()
W_SIZE = WIDTH, HEIGHT = (infoObject.current_w, infoObject.current_h)
H_SIZE = H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

screen = pygame.display.set_mode(W_SIZE, pygame.FULLSCREEN)
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

        self.scale = 1
    
    def update(self):
        pass
    
    def draw(self, x, y):
        self.screen.blit(self.image, (x - self.radius, y - self.radius))

    def get_offsets(self):
        return 0, 0
    
    def set_scale(self, scale_factor):
        self.scale = scale_factor


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
        main_x, main_y = self.get_offsets()
        coords = (main_x + offset_x - self.radius, main_y + offset_y - self.radius)
        self.screen.blit(self.image, coords)

    
    def get_offsets(self):
        x, y = self.main_object.get_offsets()
        vec = self.vec * self.scale
        return int(vec.x + x), int(vec.y + y)


class Camera:
    def __init__(self, main_object, offsets):
        self.main_object = main_object
        self.x_offset, self.y_offset = offsets

        self.x, self.y = self.main_object.get_offsets()
    
    def __call__(self, obj):
        obj.draw(self.x_offset - self.x, self.y_offset - self.y)
    
    def update(self):
        self.x, self.y = self.main_object.get_offsets()
    
    def set_offsets(self, offsets):
        self.x_offset, self.y_offset = offsets
    
    def move(self, *movement):
        self.x_offset -= movement[0]
        self.y_offset -= movement[1]


class Objects:
    def __init__(self, *objects):
        self.objects = objects
        self.camera = Camera(self.objects[0], (H_WIDTH, H_HEIGHT))
        self.zoom = 1
        self.min_zoom = 0.01
        self.max_zoom = 100
    
    def update(self):
        for obj in self.objects:
            obj.update()
        
        self.camera.update()
        
        for obj in self.objects:
            obj.set_scale(self.zoom)

        for obj in self.objects:
            self.camera(obj)
    
    def move_camera(self, *movement):
        self.camera.move(*movement)
    
    def scale(self, scale_factor):
        self.zoom *= scale_factor
        if self.zoom < self.min_zoom:
            self.zoom = self.min_zoom
        elif self.zoom > self.max_zoom:
            self.zoom = self.max_zoom

rotate_speed = 365
length = 1

sun = Object(screen, (253, 184, 19), 5)
earth = MovingObject(screen, (0, 184, 34), 3, length * 151, rotate_speed / 365, sun)
mars = MovingObject(screen, (253, 104, 19), 3, length * 250, rotate_speed / 687, sun)
moon = MovingObject(screen, (200, 200, 200), 2, length * 40, rotate_speed / 30, earth)

objects = Objects(earth, sun, mars, moon)

mouse_pos = mx, my = 0, 0
is_drag = False
sacle_factor = 1.1

while True:
    screen.fill((0, 0, 0))

    mouse_pos = mx, my = pygame.mouse.get_pos()
    if is_drag:
        y_movement = prev_mouse_pos[1] - my
        x_movement = prev_mouse_pos[0] - mx
        objects.move_camera(x_movement, y_movement)

    prev_mouse_pos = mx, my

    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
            if event.button == 4:
                objects.scale(sacle_factor)
            if event.button == 5:
                objects.scale(1/sacle_factor)
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_drag = False

    if clicked:
        is_drag = True

    objects.update()
    # print(clock.get_fps())
    pygame.display.update()
    clock.tick(FPS)