import pygame
from game import Game

LARGURA_TELA = 640
ALTURA_TELA = 480

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))
    pygame.display.set_caption("PONG")
    done = False
    clock = pygame.time.Clock()
    game = Game()

    while not done:
        done = game.eventos_game()
        game.logica()
        game.exibir_palavras_tela(tela)
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()