import pygame

from math_tools import *


class Object:
    def __init__(self, screen: pygame.Surface, color: tuple, radius: int | float):
        self.screen = screen
        self.radius = radius

        self.image = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.image.set_colorkey((0, 0, 0))

        self.scale = 1

        self.trajectory = []
        self.trajectory_points_limit = 1000

    def update(self):
        if len(self.trajectory) > self.trajectory_points_limit:
            del self.trajectory[: -self.trajectory_points_limit]

    def draw(self, offset_x, offset_y, x, y):
        res_x, res_y = (x, y)
        self.trajectory.append((res_x, res_y))
        self.screen.blit(
            self.image, (res_x + offset_x - self.radius, res_y + offset_y - self.radius)
        )

    def get_offsets(self):
        return 0, 0

    def set_scale(self, scale_factor):
        self.scale = scale_factor

    def draw_trajectory(self, x_offset, y_offset):
        if len(self.trajectory) > 1:
            comparator = lambda coords: (coords[0] + x_offset, coords[1] + y_offset)
            points = tuple(map(comparator, self.trajectory))
            pygame.draw.aalines(self.screen, (200, 200, 200), False, points)

    def clear_trajectory(self):
        self.trajectory.clear()


class MovingObject(Object):
    def __init__(
        self,
        screen: pygame.Surface,
        color: tuple,
        radius: int | float,
        movement_radius: int | float,
        angle: int | float,
        main_object: Object,
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
        if len(self.trajectory) >= self.trajectory_points_limit:
            del self.trajectory[: -self.trajectory_points_limit]
        self.vec.rotate(self.angle)

    def draw(self, offset_x, offset_y, x, y):
        main_x, main_y = self.get_offsets()
        res_x, res_y = (main_x - x, main_y - y)
        self.trajectory.append((res_x, res_y))

        self.screen.blit(
            self.image, (res_x + offset_x - self.radius, res_y + offset_y - self.radius)
        )

    def get_offsets(self):
        x, y = self.main_object.get_offsets()
        vec = self.vec * self.scale
        return int(vec.x + x), int(vec.y + y)

    def draw_trajectory(self, x_offset, y_offset):
        if len(self.trajectory) > 1:
            comparator = lambda coords: (coords[0] + x_offset, coords[1] + y_offset)
            points = tuple(map(comparator, self.trajectory))
            pygame.draw.aalines(self.screen, (200, 200, 200), False, points)


class Camera:
    def __init__(self, main_object, offsets):
        self.main_object = main_object
        self.x_offset, self.y_offset = offsets

        self.x, self.y = self.main_object.get_offsets()

        self.camera_offset_x, self.camera_offset_y = 0, 0

    def __call__(self, obj):
        obj.draw(self.x_offset, self.y_offset, self.x, self.y)
        obj.draw_trajectory(self.x_offset, self.y_offset)

    def update(self):
        self.x, self.y = self.main_object.get_offsets()

    def set_offsets(self, offsets):
        self.x_offset, self.y_offset = offsets

    def move(self, x_movement, y_movement):
        self.x_offset -= x_movement
        self.y_offset -= y_movement

        self.camera_offset_x -= x_movement
        self.camera_offset_y -= y_movement


class Objects:
    def __init__(self, offsets, *objects):
        self.objects = objects
        self.camera = Camera(self.objects[0], offsets)
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
        prev_zoom = self.zoom
        self.zoom *= scale_factor
        if self.zoom < self.min_zoom:
            self.zoom = self.min_zoom
        elif self.zoom > self.max_zoom:
            self.zoom = self.max_zoom

        if self.zoom != prev_zoom:
            self.clear_trajectories()

    def clear_trajectories(self):
        for obj in self.objects:
            obj.clear_trajectory()
