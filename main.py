import pygame as py
from checkers.constants import WIDTH, HEIGHT
from checkers.board import Board

FPS = 60

WINDOW = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Checkers v0.01')

def main():
    run = True
    clock = py.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

            if event.type == py.MOUSEBUTTONDOWN:
                pass

        board.draw(WINDOW)
        py.display.update()
    py.quit()

main()
