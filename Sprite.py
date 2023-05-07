import pygame
import time


class Sprite(object):
    def __init__(self, size: tuple[int, int], color: tuple[int, int, int], screen: pygame.surface.Surface, pos: tuple[int, int] = (0, 0)):
        self.rect = pygame.rect.Rect(pos, size)
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size
        self.following = True

    def follow(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.left = mouse_pos[0] - int(self.size[0] / 2)
        self.rect.top = mouse_pos[1] - int(self.size[1] / 2)

    def get_grid(self, grid):
        self.grid = grid

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
