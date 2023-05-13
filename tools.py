from PIL import Image
import pygame


def load_image(filepath):
    img = pygame.image.load(filepath).convert_alpha()
    # image.set_colorkey(image.get_at((0, 0)))
    return img


def average_color(img):
    # convert pygame.Surfac -> PIL.Image
    strFormat = 'RGBA'
    raw_str = pygame.image.tostring(img, strFormat, False)
    pil_image = Image.frombytes(strFormat, img.get_size(), raw_str)

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
