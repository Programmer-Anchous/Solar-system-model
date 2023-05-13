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

rotate_speed = 365 / 3
length = 1

sun = Object(screen, 5, "data/sun.png")
earth = MovingObject(screen, 4, "data/earth.png", length * 151, rotate_speed / 365, sun)
mars = MovingObject(screen, 4, "data/mars.png", length * 250, rotate_speed / 687, sun)
moon = MovingObject(screen, 3, "data/moon.png", length * 40, rotate_speed / 30, earth)

objects = Objects((H_WIDTH, H_HEIGHT), sun, earth, sun, mars, moon)

mouse_pos = mx, my = 0, 0
is_drag = False
scale_factor = 1.1

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
                objects.scale(scale_factor)
            if event.button == 5:
                objects.scale(1 / scale_factor)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_drag = False

    if clicked:
        is_drag = True
    
    objects.update()

    # print(clock.get_fps())
    pygame.display.update()
    clock.tick(FPS)
