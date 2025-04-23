import pygame

def draw_block(surface, x, y, size, color=(0, 255, 0), border=2):
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (30, 30, 30), rect, border)
