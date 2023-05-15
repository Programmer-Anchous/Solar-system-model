import pygame
import sys

from space_objects import *
from tools import *


pygame.init()

infoObject = pygame.display.Info()
W_SIZE = WIDTH, HEIGHT = (infoObject.current_w, infoObject.current_h)
H_SIZE = H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

screen = pygame.display.set_mode(W_SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60

rotate_speed = 500
length = 10

radius = 1 / 100

sun = Object(
    screen,
    radius * 40000,
    "data/sun.png",
    rotate_speed / 3600,
    "Sun"
)
mercury = MovingObject(
    screen,
    radius * 2439,
    "data/mercury.png",
    rotate_speed / 80,
    "Mercury",
    length * 70,
    rotate_speed / 88,
    sun,
)
venus = MovingObject(
    screen,
    radius * 6051,
    "data/venus.png",
    rotate_speed / 80,
    "Venus",
    length * 108,
    rotate_speed / 224,
    sun,
)
earth = MovingObject(
    screen,
    radius * 6371,
    "data/earth.png",
    rotate_speed / 365,
    "Earth",
    length * 151,
    rotate_speed / 365,
    sun,
)
mars = MovingObject(
    screen,
    radius * 3389,
    "data/mars.png",
    rotate_speed / 70,
    "Mars",
    length * 250,
    rotate_speed / 687,
    sun,
)
jupiter = MovingObject(
    screen,
    radius * 40000,
    "data/jupiter.png",
    rotate_speed / 70,
    "Jupiter",
    length * 741,
    rotate_speed / 4329,
    sun,
)
saturn = MovingObject(
    screen,
    radius * 30000,
    "data/saturn.png",
    rotate_speed / 70,
    "Saturn",
    length * 1464,
    rotate_speed / 10768,
    sun,
)
uranus = MovingObject(
    screen,
    radius * 21000,
    "data/uranus.png",
    rotate_speed / 70,
    "Uranus",
    length * 2938,
    rotate_speed / 30660,
    sun,
)
neptune = MovingObject(
    screen,
    radius * 20000,
    "data/neptune.png",
    rotate_speed / 70,
    "Neptune",
    length * 4473,
    rotate_speed / 59860,
    sun,
)
moon = MovingObject(
    screen,
    radius * 1737,
    "data/moon.png",
    rotate_speed / 20,
    "Moon",
    length * 40,
    rotate_speed / 30,
    earth,
)

objects = Objects((H_WIDTH, H_HEIGHT), sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, moon)

mouse_pos = mx, my = 0, 0
is_drag = False
scale_factor = 1.1


class Panel:
    def __init__(self, screen, width, objects):
        self.screen = screen
        self.width = width
        self.screen_size = self.screen.get_size()
        self.objects = objects

        self.image = pygame.Surface((width, screen.get_height()))
        self.image.set_alpha(170)

        self.half_button_background = pygame.Surface((15, 100))
        self.half_button_background.set_alpha(170)
        pygame.draw.rect(
            self.half_button_background, (1, 1, 1), (0, 1, 14, 98), 0, -1, -1, 5, -1, 5
        )
        self.half_button_background.set_colorkey((0, 0, 0))

        self.button_background = pygame.Surface((30, 100))
        self.button_background.set_alpha(170)
        pygame.draw.rect(self.button_background, (1, 1, 1), (1, 1, 28, 98), 0, 5)
        self.button_background.set_colorkey((0, 0, 0))

        self.buttons = list()
        for i, obj in enumerate(self.objects.objects):
            button = TextButton(screen, obj.name, (20, i * 40 + 200))
            self.buttons.append(button)

        self.is_opened = False

        self.draw_trajectory_button = TextButton(
            self.screen, "draw trajectory", (20, 30)
        )

        self.speed_label = pygame.font.Font(None, 32).render("speed", True, (200,) * 3)
        self.speed_slider = Slider(self.screen, (self.width // 2, 140), (210, 15))
        self.speed_slider.set_value(1 / 1.5)

        self.exit_button = TextButton(
            self.screen, "exit", (20, self.screen_size[1] - 30)
        )

        image = pygame.Surface((30, 100))
        image.set_colorkey((0, 0, 0))
        image_pressed = image.copy()
        points = ((10, 30), (22, 50), (10, 70))
        pygame.draw.polygon(image, (200,) * 3, points)
        pygame.draw.polygon(image_pressed, (240,) * 3, points)
        rect_values = ((1, 1, 28, 98), 2, 5)
        pygame.draw.rect(image, (200,) * 3, *rect_values)
        pygame.draw.rect(image_pressed, (240,) * 3, *rect_values)
        self.open_button = Button(
            screen, image, image_pressed, (15, self.screen_size[1] // 2), True
        )

        image = pygame.Surface((30, 100))
        image.set_colorkey((0, 0, 0))
        image_pressed = image.copy()
        points = ((20, 30), (8, 50), (20, 70))
        pygame.draw.polygon(image, (200,) * 3, points)
        pygame.draw.polygon(image_pressed, (240,) * 3, points)
        pygame.draw.rect(image, (200,) * 3, *rect_values)
        pygame.draw.rect(image_pressed, (240,) * 3, *rect_values)

        self.close_button = Button(
            screen, image, image_pressed, (self.width, self.screen_size[1] // 2), True
        )

    def update(self, mouse_pos, clicked):
        change_visibility = False
        speed = False
        is_exit = False
        if self.is_opened:
            surf = blur(self.get_sub_surf(), 15)
            surf.blit(self.image, (0, 0))
            self.screen.blit(surf, (0, 0))
            self.screen.blit(
                self.half_button_background, (self.width, self.screen_size[1] // 2 - 50)
            )

            for i, button in enumerate(self.buttons):
                button.update(mouse_pos, clicked)
                if button.triggered():
                    self.objects.set_main_object(i)

            self.screen.blit(self.speed_label, (20, 100))
            self.speed_slider.update(clicked, mouse_pos)
            speed = self.speed_slider.get_value()

            self.draw_trajectory_button.update(mouse_pos, clicked)
            if self.draw_trajectory_button.triggered():
                change_visibility = True

            self.close_button.update(mouse_pos, clicked)
            if self.close_button.triggered():
                self.is_opened = False

            self.exit_button.update(mouse_pos, clicked)
            if self.exit_button.triggered():
                is_exit = True

            pygame.draw.line(
                self.screen,
                (200,) * 3,
                (self.width, 0),
                (self.width, self.screen_size[1] // 2 - 50),
            )
            pygame.draw.line(
                self.screen,
                (200,) * 3,
                (self.width, self.screen_size[1] // 2 + 49),
                (self.width, self.screen_size[1]),
            )
        else:
            self.screen.blit(self.button_background, (0, self.screen_size[1] // 2 - 50))
            self.open_button.update(mouse_pos, clicked)
            if self.open_button.triggered():
                self.is_opened = True
        return change_visibility, speed, is_exit

    def mouse_in_panel(self, mouse_pos):
        return panel.is_opened and mouse_pos[0] < self.width

    def get_sub_surf(self):
        sub = self.screen.subsurface((0, 0, self.width, self.screen_size[1]))
        return sub


panel = Panel(screen, 250, objects)

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                objects.camera.set_offsets((H_WIDTH, H_HEIGHT))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
            if event.button == 4:
                objects.scale(scale_factor)
            if event.button == 5:
                objects.scale(1 / scale_factor)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                panel.speed_slider.release()
                is_drag = False

    if clicked and not panel.mouse_in_panel(mouse_pos):
        is_drag = True

    objects.update()
    change_visibility, speed, is_exit = panel.update(mouse_pos, clicked)
    if change_visibility:
        objects.change_trajectory_visible()
    if speed:
        objects.set_speed(speed * 1.5)
    if is_exit:
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(FPS)
