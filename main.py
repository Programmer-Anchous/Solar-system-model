import pygame
import sys

from space_objects import *


pygame.init()

infoObject = pygame.display.Info()
W_SIZE = WIDTH, HEIGHT = (infoObject.current_w, infoObject.current_h)
H_SIZE = H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

screen = pygame.display.set_mode(W_SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60

rotate_speed = 365
length = 1

sun = Object(screen, 15, "data/sun.png", rotate_speed / 3600, "Sun")
earth = MovingObject(screen, 8, "data/earth.png", rotate_speed / 80, "Earth", length * 151, rotate_speed / 365, sun)
mars = MovingObject(screen, 8, "data/mars.png", rotate_speed / 70, "Mars", length * 250, rotate_speed / 687, sun)
moon = MovingObject(screen, 4, "data/moon.png", rotate_speed / 20, "Moon", length * 40, rotate_speed / 30, earth)

objects = Objects((H_WIDTH, H_HEIGHT), sun, earth, mars, moon)

mouse_pos = mx, my = 0, 0
is_drag = False
scale_factor = 1.1


class Panel:
    def __init__(self, screen, width, objects):
        self.screen = screen
        self.width = width
        self.objects = objects

        self.image = pygame.Surface((width, screen.get_height()))
        self.image.set_alpha(150)

        self.objects_dict = {obj.name: obj for obj in self.objects.objects}

        self.buttons = list()
        for i, obj in enumerate(self.objects.objects):
            button = TextButton(screen, obj.name, (20, i * 40 + 100))
            self.buttons.append(button)

        self.is_opened = False

        image = pygame.Surface((30, 100))
        image.set_colorkey((0, 0, 0))
        image_pressed = image.copy()
        pygame.draw.polygon(image, (200,) * 3, ((4, 10), (30, 50), (4, 90)))
        pygame.draw.polygon(image_pressed, (240,) * 3, ((4, 10), (30, 50), (4, 90)))
        self.open_button = Button(screen, image, image_pressed, (15, self.screen.get_height() // 2), True)

        image = pygame.Surface((30, 100))
        image.set_colorkey((0, 0, 0))
        image_pressed = image.copy()
        pygame.draw.polygon(image, (200,) * 3, ((30, 10), (4, 50), (30, 90)))
        pygame.draw.polygon(image_pressed, (240,) * 3, ((30, 10), (4, 50), (30, 90)))
        self.close_button = Button(screen, image, image_pressed, (self.width - 15, self.screen.get_height() // 2), True)
    
    def update(self, mouse_pos, clicked):
        if self.is_opened:
            self.screen.blit(self.image, (0, 0))
            for i, button in enumerate(self.buttons):
                button.update(mouse_pos, clicked)
                if button.triggered():
                    self.objects.set_main_object(i)
            
            self.close_button.update(mouse_pos, clicked)
            if self.close_button.triggered():
                self.is_opened = False
        else:
            self.open_button.update(mouse_pos, clicked)
            if self.open_button.triggered():
                self.is_opened = True
    
    def mouse_in_panel(self, mouse_pos):
        return mouse_pos[0] < self.width
        

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
                objects.change_trajectory_visible()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
            if event.button == 4:
                objects.scale(scale_factor)
            if event.button == 5:
                objects.scale(1 / scale_factor)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_drag = False

    if clicked and not (panel.mouse_in_panel(mouse_pos)):
        is_drag = True
    
    objects.update()
    panel.update(mouse_pos, clicked)

    # print(clock.get_fps())
    pygame.display.update()
    clock.tick(FPS)
