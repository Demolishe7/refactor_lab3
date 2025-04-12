import pygame
from pygame.locals import *
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, CAMERA_OFFSET, FPS, BOARD_WIDTH, BOARD_HEIGHT, DIFFICULTY
from blocks import ActiveBlock, FallingBlock, BlockButton

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Рефакторинг")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font('freesansbold.ttf', 100)
        self.score = 0
        self.display_score = 0

        self.board_positions = []
        self.falling_blocks = []
        self.active_block = ActiveBlock(self.board_positions, self.falling_blocks)
        self.state = "MENU"

        self.play_button = BlockButton(60, 400, block_size=20, border_width=3)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if self.state == "MENU":
                self.play_button.handle_event(event, self.change_state)
            elif self.state == "GAME":
                self.active_block.handle_event(event)

    def update(self):
        if self.state == "MENU":
            self.play_button.update()
        elif self.state == "GAME":
            self.active_block.update()
            self.check_complete_rows()
            for fb in list(self.falling_blocks):
                fb.update()

    def draw(self):
        self.screen.fill((100, 100, 100))
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "GAME":
            field_rect = pygame.Rect(CAMERA_OFFSET[0], CAMERA_OFFSET[1], BLOCK_SIZE * BOARD_WIDTH, BLOCK_SIZE * BOARD_HEIGHT)
            pygame.draw.rect(self.screen, (40, 40, 40), field_rect)
            self.draw_fixed_blocks()
            self.active_block.draw(self.screen)
            self.draw_grid()
            self.draw_score()
            for fb in self.falling_blocks:
                fb.draw(self.screen)

    def draw_menu(self):
        text_surface = self.font_large.render(str(DIFFICULTY), True, (0, 0, 0))
        self.screen.blit(text_surface, (200, 500))
        self.play_button.draw(self.screen)

    def draw_grid(self):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE + CAMERA_OFFSET[0], y * BLOCK_SIZE + CAMERA_OFFSET[1], BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, (30, 30, 30), rect, 2)

    def draw_fixed_blocks(self):
        for pos in self.board_positions:
            rect = pygame.Rect(pos[0] * BLOCK_SIZE + CAMERA_OFFSET[0],
                               pos[1] * BLOCK_SIZE + CAMERA_OFFSET[1],
                               BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.screen, (0, 255, 0), rect)

    def draw_score(self):
        if self.display_score < self.score:
            self.display_score += (self.score - self.display_score) * 0.005
        text_surface = self.font_large.render(str(round(self.display_score)), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(text_surface, text_rect)

    def change_state(self):
        self.state = "GAME"

    def check_complete_rows(self):
        row_counts = {row: 0 for row in range(BOARD_HEIGHT)}
        positions_to_remove = []
        rows_to_remove = []

        for pos in self.board_positions:
            if 0 <= pos[1] < BOARD_HEIGHT:
                row_counts[pos[1]] += 1

        for row, count in row_counts.items():
            if count >= BOARD_WIDTH:
                rows_to_remove.append(row)
                for pos in self.board_positions:
                    if pos[1] == row:
                        positions_to_remove.append(pos)

        for pos in positions_to_remove:
            self.board_positions.remove(pos)
            self.falling_blocks.append(FallingBlock(pos[0] * BLOCK_SIZE + CAMERA_OFFSET[0],
                                                     pos[1] * BLOCK_SIZE + CAMERA_OFFSET[1]))

        for removed_row in rows_to_remove:
            for pos in self.board_positions:
                if pos[1] < removed_row:
                    pos[1] += 1

        if len(rows_to_remove) == 1:
            self.score += 40
        elif len(rows_to_remove) == 2:
            self.score += 100
        elif len(rows_to_remove) == 3:
            self.score += 300
        elif len(rows_to_remove) == 4:
            self.score += 1200
