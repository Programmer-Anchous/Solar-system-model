import pygame

from math_tools import *
from tools import *


class Object:
    def __init__(
        self,
        screen: pygame.Surface,
        radius: int | float,
        filepath: str,
        rotation_speed: int | float,
        name: str,
    ):
        self.screen = screen
        self.radius = radius
        self.name = name

        self.image = load_image(filepath)
        size = self.image.get_width()

        self.scale_factor = radius / (size / 2)

        self.scale = 1

        self.trajectory = []
        self.trajectory_points_limit = 1000

        self.trajectory_color = get_trajectory_color(self.image)

        self.current_image = self.get_scaled_image()

        self.is_draw_trajectory = True

        self.rotation = 0
        self.rotation_speed = rotation_speed
        self.current_rotation_speed = self.rotation_speed

    def update(self):
        if self.is_draw_trajectory:
            if len(self.trajectory) >= self.trajectory_points_limit:
                del self.trajectory[: -self.trajectory_points_limit]

    def draw(self, offset_x, offset_y, x, y):
        if self.is_draw_trajectory:
            self.trajectory.append((x, y))

        rotated_image = pygame.transform.rotate(self.current_image, self.rotation)
        offset = rotated_image.get_width() // 2
        self.rotation += self.current_rotation_speed
        if self.rotation > 360:
            self.rotation %= 360

        coords = (
            x + offset_x - offset,
            y + offset_y - offset,
        )
        self.screen.blit(
            rotated_image,
            coords,
        )

    def get_scaled_image(self):
        img = pygame.transform.scale(
            self.image,
            (
                self.image.get_width() * self.scale_factor * self.scale,
                self.image.get_height() * self.scale_factor * self.scale,
            ),
        )
        return img

    def get_offsets(self):
        return 0, 0

    def set_scale(self, scale_factor):
        if self.scale != scale_factor:
            self.current_image = self.get_scaled_image()
            self.scale = scale_factor

    def draw_trajectory(self, x_offset, y_offset):
        if len(self.trajectory) > 1:
            comparator = lambda coords: (coords[0] + x_offset, coords[1] + y_offset)
            points = tuple(map(comparator, self.trajectory))
            pygame.draw.aalines(self.screen, self.trajectory_color, False, points)

    def clear_trajectory(self):
        self.trajectory.clear()

    def set_trajectory_visible(self, status):
        self.is_draw_trajectory = status

    def set_speed(self, factor):
        self.current_rotation_speed = self.rotation_speed * factor


class MovingObject(Object):
    def __init__(
        self,
        screen: pygame.Surface,
        radius: int | float,
        filepath: str,
        rotation_speed: int | float,
        name: str,
        movement_radius: int | float,
        angle: int | float,
        main_object: Object,
    ):
        super().__init__(screen, radius, filepath, rotation_speed, name)
        self.movement_radius = movement_radius
        self.angle = angle
        self.current_angle = self.angle
        self.main_object = main_object

        self.vec = Vector(-self.movement_radius, 0)

        self.image = load_image(filepath)

        self.current_image = self.get_scaled_image()
        self.current_rotation_speed = self.rotation_speed

    def update(self):
        if self.is_draw_trajectory:
            if len(self.trajectory) >= self.trajectory_points_limit:
                del self.trajectory[: -self.trajectory_points_limit]
        self.vec.rotate(self.current_angle)

    def draw(self, offset_x, offset_y, x, y):
        main_x, main_y = self.get_offsets()
        res_x, res_y = (x - main_x, y - main_y)
        if self.is_draw_trajectory:
            self.trajectory.append((res_x, res_y))

        rotated_image = pygame.transform.rotate(self.current_image, self.rotation)
        offset = rotated_image.get_width() // 2
        self.rotation += self.current_rotation_speed
        if self.rotation > 360:
            self.rotation %= 360

        self.screen.blit(
            rotated_image, (res_x + offset_x - offset, res_y + offset_y - offset)
        )

    def get_scaled_image(self):
        img = pygame.transform.scale(
            self.image,
            (
                self.image.get_width() * self.scale_factor * self.scale,
                self.image.get_height() * self.scale_factor * self.scale,
            ),
        )
        return img

    def get_offsets(self):
        x, y = self.main_object.get_offsets()
        vec = self.vec * self.scale
        return int(vec.x + x), int(vec.y + y)

    def draw_trajectory(self, x_offset, y_offset):
        if len(self.trajectory) > 1:
            comparator = lambda coords: (coords[0] + x_offset, coords[1] + y_offset)
            points = tuple(map(comparator, self.trajectory))
            pygame.draw.aalines(self.screen, self.trajectory_color, False, points)

    def set_speed(self, factor):
        self.current_rotation_speed = self.rotation_speed * factor
        self.current_angle = self.angle * factor


class Camera:
    def __init__(self, main_object, offsets):
        self.main_object = main_object
        self.x_offset, self.y_offset = offsets

        self.x, self.y = self.main_object.get_offsets()

        self.camera_offset_x, self.camera_offset_y = 0, 0

        self.is_draw_trajectory = True

    def __call__(self, obj):
        if self.is_draw_trajectory:
            obj.draw_trajectory(self.x_offset, self.y_offset)
        obj.draw(self.x_offset, self.y_offset, self.x, self.y)

    def update(self):
        self.x, self.y = self.main_object.get_offsets()

    def set_offsets(self, offsets):
        self.x_offset, self.y_offset = offsets

    def move(self, x_movement, y_movement):
        self.x_offset -= x_movement
        self.y_offset -= y_movement

        self.camera_offset_x -= x_movement
        self.camera_offset_y -= y_movement

    def set_trajectory_visible(self, status):
        self.is_draw_trajectory = status

    def set_main_object(self, obj):
        self.main_object = obj


class Objects:
    def __init__(self, offsets, *objects):
        self.objects = objects
        self.camera = Camera(self.objects[0], offsets)
        self.zoom = 1
        self.min_zoom = 0.01
        self.max_zoom = 40

        self.is_draw_trajectory = True
        self.change_trajectory_visible()

    def update(self):
        for obj in self.objects:
            obj.set_scale(self.zoom)

        for obj in self.objects:
            obj.update()

        self.camera.update()

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

    def change_trajectory_visible(self):
        self.is_draw_trajectory = not self.is_draw_trajectory

        self.is_draw_trajectory = self.is_draw_trajectory
        self.camera.set_trajectory_visible(self.is_draw_trajectory)
        for obj in self.objects:
            obj.set_trajectory_visible(self.is_draw_trajectory)

        if self.is_draw_trajectory is False:
            self.clear_trajectories()

    def set_main_object(self, num):
        self.camera.set_main_object(self.objects[num])
        self.clear_trajectories()

    def set_speed(self, factor):
        for obj in self.objects:
            obj.set_speed(factor)
