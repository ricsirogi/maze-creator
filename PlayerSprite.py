import pygame
import time


class Sprite(object):
    def __init__(self, size: tuple[int, int], color: tuple[int, int, int], screen: pygame.surface.Surface, unit: tuple[int, int]):
        self.rect = pygame.rect.Rect((0, 0), size)
        self.screen = screen
        self.color = color
        self.size = size
        self.unit = unit
        self.following = True

    def move(self):
        keys_pressed = pygame.key.get_pressed()
        new_pos = (self.rect.left, self.rect.top)

        if keys_pressed[pygame.K_UP]:
            new_pos = (self.rect.left, self.rect.top - self.unit[0])
        elif keys_pressed[pygame.K_RIGHT]:
            new_pos = (self.rect.left + self.unit[0], self.rect.top)
        elif keys_pressed[pygame.K_DOWN]:
            new_pos = (self.rect.left, self.rect.top + self.unit[0])
        elif keys_pressed[pygame.K_LEFT]:
            new_pos = (self.rect.left - self.unit[0], self.rect.top)

        return new_pos

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
