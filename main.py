import pygame
from game import Game
from constants import Config as C

def main():
    pygame.init()
    screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        screen.fill((0, 0, 0))
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(C.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_block(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_block(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move_block(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_block()

    pygame.quit()

if __name__ == "__main__":
    main()
