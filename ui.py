import pygame


# Use draw in the main loop to render the button
class Button:
    def __init__(self, x, y, image, scale=None):
        if scale is None:
            self.image = image
        else:
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # 1 left, 2 middle, 3 right
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        surface.blit(self.image, self.rect)


class UIElement:
    def __init__(self, x, y, image, scale=None):
        if scale is None:
            self.image = image
        else:
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
