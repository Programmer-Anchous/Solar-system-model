from PIL import Image, ImageFilter
import pygame


def to_pil(surf):
    strFormat = "RGBA"
    raw_str = pygame.image.tostring(surf, strFormat, False)
    pil_image = Image.frombytes(strFormat, surf.get_size(), raw_str)
    return pil_image


def to_surf(image):
    mode = image.mode
    size = image.size
    data = image.tobytes()

    py_image = pygame.image.fromstring(data, size, mode)
    return py_image


def blur(surface, scale_factor):
    width, height = surface.get_size()
    surface = pygame.transform.smoothscale(
        surface, (width // scale_factor, height // scale_factor)
    )
    surface = pygame.transform.smoothscale(surface, (width, height))
    return surface


def load_image(filepath):
    img = pygame.image.load(filepath).convert_alpha()
    # image.set_colorkey(image.get_at((0, 0)))
    return img


def average_color(img):
    pil_image = to_pil(img)

    r = g = b = 0
    pixels_im = pil_image.load()
    x, y = pil_image.size
    amount = x * y

    for i in range(x):
        for j in range(y):
            colors = list(pixels_im[i, j])
            r += colors[0]
            g += colors[1]
            b += colors[2]

    return (r // amount, g // amount, b // amount)


def negative_color(color):
    return tuple(map(lambda x: 255 - x, color))


def get_trajectory_color(img):
    return negative_color(average_color(img))


class Button:
    def __init__(
        self,
        screen: pygame.Surface,
        image: pygame.Surface,
        image_pressed: pygame.Surface,
        coords: tuple | list,
        center: bool = False,
    ):
        self.screen = screen
        self.image = image
        self.image_pressed = image_pressed
        if center:
            self.rect = self.image.get_rect(center=coords)
        else:
            self.rect = self.image.get_rect(topleft=coords)

        self.clicked = False

    def update(self, mouse_pos: tuple, click: bool):
        self.clicked = False
        if self.rect.collidepoint(mouse_pos):
            current_image = self.image_pressed
            if click:
                self.clicked = True
        else:
            current_image = self.image
        self.screen.blit(current_image, self.rect)

    def triggered(self) -> bool:
        return self.clicked


class TextButton(Button):
    def __init__(
        self,
        screen: pygame.Surface,
        text: str,
        coords: tuple | list,
        center: bool = False,
    ):
        self.text = text
        font = pygame.font.Font(None, 32)
        image = font.render(text, True, (200,) * 3)
        image_pressed = font.render(text, True, (240,) * 3)
        super().__init__(screen, image, image_pressed, coords, center)


class Slider(pygame.sprite.Sprite):
    def __init__(self, display, coords, size=(200, 20)):
        self.offset = size[1] // 8
        self.radius = size[1] // 2
        self.display = display
        self.size = size

        self.image = pygame.Surface(size)
        pygame.draw.rect(
            self.image,
            (230, 230, 230),
            (
                self.offset,
                self.offset,
                size[0] - self.offset * 2,
                size[1] - self.offset * 2,
            ),
            2,
            self.radius,
        )
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect(center=coords)

        self.point_image = pygame.Surface((size[1], size[1] * 1.5))
        pygame.draw.rect(
            self.point_image,
            (230, 230, 230),
            (0, 0, *self.point_image.get_size()),
            0,
            self.radius,
        )
        pygame.draw.rect(
            self.point_image,
            (200, 200, 200),
            (0, 0, *self.point_image.get_size()),
            2,
            self.radius,
        )
        self.point_image.set_colorkey((0, 0, 0))

        self.point_rect = self.point_image.get_rect(
            center=(coords[0] - size[0] // 2 + self.offset * 2, coords[1])
        )

        self.start, self.end = (
            self.point_rect.centerx,
            self.point_rect.centerx + size[0] - size[1] // 2,
        )
        self.length = self.end - self.start
        self.dragged = False

    def release(self):
        self.dragged = False

    def set_value(self, num):
        self.point_rect.x = self.start + self.length * (num)

    def get_value(self) -> int:
        return round((self.point_rect.centerx - self.start) / self.length * 100) / 100

    def update(self, clicked, mouse_pos):
        if clicked and self.rect.collidepoint(mouse_pos):
            self.dragged = True
        if self.dragged:
            if mouse_pos[0] <= self.start:
                self.point_rect.centerx = self.start
            elif mouse_pos[0] >= self.end:
                self.point_rect.centerx = self.end
            else:
                self.point_rect.centerx = mouse_pos[0]

        image = self.image.copy()
        pygame.draw.rect(
            image,
            (230, 230, 230),
            (
                self.offset,
                self.offset,
                self.point_rect.centerx - self.start,
                self.size[1] - self.offset * 2,
            ),
            0,
            self.radius,
        )

        self.display.blit(image, self.rect)
        self.display.blit(self.point_image, self.point_rect)
