import pygame
import random
from copy import deepcopy
from pygame.locals import *
from constants import BLOCK_SIZE, CAMERA_OFFSET, BLOCK_FALL_SPEED, BOARD_WIDTH, BOARD_HEIGHT, BLOCKS

class ActiveBlock:
    def __init__(self, board_positions, falling_blocks):
        self.board_positions = board_positions
        self.falling_blocks = falling_blocks
        self.reset()
        self.last_translate_time = 0

    def reset(self):
        self.rotation_id = 0
        self.block_id = random.randint(0, len(BLOCKS)-1)
        self.positions = deepcopy(BLOCKS[self.block_id][self.rotation_id])
        self.x_offset = 0
        self.y_offset = 0
        self.fall_speed = BLOCK_FALL_SPEED
        self.last_fall_time = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                self.move(-1)
            elif event.key == K_RIGHT:
                self.move(1)
            elif event.key == K_UP:
                self.rotate()
            elif event.key == K_DOWN:
                self.fall_speed = BLOCK_FALL_SPEED / 10
        elif event.type == pygame.KEYUP:
            if event.key == K_DOWN:
                self.fall_speed = BLOCK_FALL_SPEED

    def move(self, direction):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_translate_time > 200:
            new_positions = deepcopy(self.positions)
            for pos in new_positions:
                pos[0] += direction
            if not self.check_collision(new_positions):
                self.positions = new_positions
                self.x_offset += direction
            self.last_translate_time = current_time

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > self.fall_speed * 1000:
            new_positions = deepcopy(self.positions)
            for pos in new_positions:
                pos[1] += 1
            if not self.check_collision(new_positions):
                self.positions = new_positions
                self.y_offset += 1
            else:
                self.board_positions.extend(self.positions)
                self.reset()
            self.last_fall_time = current_time

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * BLOCK_SIZE + CAMERA_OFFSET[0],
                               pos[1] * BLOCK_SIZE + CAMERA_OFFSET[1],
                               BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, (0, 255, 0), rect)
            pygame.draw.rect(surface, (30, 30, 30), rect, 2)

    def check_collision(self, positions):
        for pos in positions:
            if pos[0] < 0 or pos[0] >= BOARD_WIDTH or pos[1] >= BOARD_HEIGHT:
                return True
            if pos in self.board_positions:
                return True
        return False

    def rotate(self):
        new_rotation_id = (self.rotation_id + 1) % 4
        new_positions = deepcopy(BLOCKS[self.block_id][new_rotation_id])
        for pos in new_positions:
            pos[0] += self.x_offset
            pos[1] += self.y_offset
        if not self.check_collision(new_positions):
            self.rotation_id = new_rotation_id
            self.positions = new_positions


class FallingBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = random.randint(-30, -10) / 10
        self.angle = 0
        self.da = random.choice([-1, 1]) * 3
        self.surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (0, 255, 0), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.surface, (30, 30, 30), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)

    def update(self):
        self.dy += 0.1
        self.y += self.dy
        self.x += random.randint(-5, 5) * 0.1
        self.angle += self.da

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.surface, self.angle)
        surface.blit(rotated, (self.x, self.y))


class BlockButton:
    def __init__(self, x, y, block_size=25, border_width=3):
        self.x = x
        self.y = y
        self.block_size = block_size
        self.border_width = border_width
        self.map = [
            [1, 1, 5, 0, 1, 0, 0, 0, 4, 1, 5, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 1, 3, 0, 1, 0, 0, 0, 1, 1, 1, 0, 2, 1, 3],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 1, 5, 0, 1, 0, 1, 0, 0, 1, 0]
        ]
        self.colour = [0, 0, 0]
        self.rect = pygame.Rect(self.x, self.y, len(self.map[0]) * self.block_size, len(self.map) * self.block_size)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colour[1] = min(self.colour[1] + 1, 255)
        else:
            self.colour[1] = max(self.colour[1] - 0.2, 0)

    def draw(self, surface):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                cell = self.map[row][col]
                x_pos = col * self.block_size + self.x
                y_pos = row * self.block_size + self.y
                if cell == 1:
                    rect = pygame.Rect(x_pos, y_pos, self.block_size, self.block_size)
                    pygame.draw.rect(surface, self.colour, rect)
                    pygame.draw.rect(surface, (30, 30, 30), rect, self.border_width)

    def handle_event(self, event, callback):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                callback()
