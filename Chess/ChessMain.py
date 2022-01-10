"""
- Store current state of chess game
- Determine valid moves at the current state
- Keep a move log
"""

import pygame as p
import ChessEngine

# Global constants

# SOR: Bunlar niye boyle?
GRID_WIDTH = GRID_HEIGHT = 512
WIDTH = HEIGHT = GRID_WIDTH + 100

DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15

IMAGES = {}

'''
Initialize a global dictionary of images. Will be called once in the main.
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        # Load image by scaling it to the square size
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
        #NOTE: Access an image by 'IMAGES['wp']'

'''
Main function
'''
def main():
    # Initialize a pygame
    p.init()

    # Set display and background
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))

    # Initialize a GameState object
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo a move when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Graphics in the current GameState.
'''
def drawGameState(screen, gs):
    # These two functions are separated since we might want to add a highlighting attribute.
    drawBoard(screen)
    drawPieces(screen, gs.board)

'''
Draw the squares on the board. The top left square is always light. 
'''
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # Pick the color depending on row and col
            # Light squares have even parity, dark squares have odd parity.
            color = colors[((row + col) % 2)]
            # Draw the square
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw pieces on top of the squares.
'''
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            # If the position is not empty, draw the piece.
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()