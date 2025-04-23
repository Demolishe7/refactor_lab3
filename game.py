import pygame
import random
from collections import defaultdict
from constants import BLOCKS, Config as C
from utils import draw_block

class FallingBlock:
    def __init__(self, x, y, size=C.BLOCK_SIZE):
        self.x, self.y, self.size = x, y, size
        self.speed = random.uniform(1, 3)

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        draw_block(surface, self.x, self.y, self.size, (100, 255, 100))

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.reset_game()

    def reset_game(self):
        self.board_positions = []
        self.active_block = self.get_new_block()
        self.falling_blocks = []
        self.score = 0
        self.tick_counter = 0

    def get_new_block(self):
        return {
            "type": random.randint(0, len(BLOCKS) - 1),
            "rotation": 0,
            "position": [4, 0],
        }

    def rotate_block(self):
        block = self.active_block
        block["rotation"] = (block["rotation"] + 1) % len(BLOCKS[block["type"]])

    def move_block(self, dx, dy):
        self.active_block["position"][0] += dx
        self.active_block["position"][1] += dy

    def lock_block(self):
        coords = self.get_block_coords()
        self.board_positions.extend(coords)
        self.check_complete_rows()
        self.active_block = self.get_new_block()

    def get_block_coords(self):
        t = self.active_block["type"]
        r = self.active_block["rotation"]
        px, py = self.active_block["position"]
        return [[x + px, y + py] for x, y in BLOCKS[t][r]]

    def is_valid_position(self, coords):
        for x, y in coords:
            if x < 0 or x >= C.BOARD_WIDTH or y >= C.BOARD_HEIGHT or [x, y] in self.board_positions:
                return False
        return True

    def update(self):
        self.tick_counter += 1
        if self.tick_counter >= (C.FPS // C.DIFFICULTY):
            self.tick_counter = 0
            new_coords = [[x, y + 1] for x, y in self.get_block_coords()]
            if self.is_valid_position(new_coords):
                self.active_block["position"][1] += 1
            else:
                self.lock_block()

        for fb in self.falling_blocks:
            fb.fall()

    def check_complete_rows(self):
        row_counts = defaultdict(int)
        for x, y in self.board_positions:
            row_counts[y] += 1

        full_rows = {row for row, count in row_counts.items() if count >= C.BOARD_WIDTH}
        self.board_positions = [pos for pos in self.board_positions if pos[1] not in full_rows]

        for row in sorted(full_rows):
            for pos in self.board_positions:
                if pos[1] < row:
                    pos[1] += 1

        self.score += [0, 40, 100, 300, 1200][len(full_rows)]

        for row in full_rows:
            for x in range(C.BOARD_WIDTH):
                self.falling_blocks.append(FallingBlock(x * C.BLOCK_SIZE + C.CAMERA_OFFSET[0],
                                                        row * C.BLOCK_SIZE + C.CAMERA_OFFSET[1]))

    def draw_board(self):
        for x, y in self.board_positions:
            draw_block(self.surface, x * C.BLOCK_SIZE + C.CAMERA_OFFSET[0],
                       y * C.BLOCK_SIZE + C.CAMERA_OFFSET[1],
                       C.BLOCK_SIZE)

    def draw_block(self):
        for x, y in self.get_block_coords():
            draw_block(self.surface, x * C.BLOCK_SIZE + C.CAMERA_OFFSET[0],
                       y * C.BLOCK_SIZE + C.CAMERA_OFFSET[1],
                       C.BLOCK_SIZE, (0, 200, 255))

    def draw_falling(self):
        for fb in self.falling_blocks:
            fb.draw(self.surface)

    def draw(self):
        self.draw_board()
        self.draw_block()
        self.draw_falling()
