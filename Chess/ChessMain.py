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
    # Generate valid moves
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made

    # Load images and set running to true
    loadImages()
    running = True

    # variables for implementing the function for moving pieces
    sqSelected = () #keep track of the last click (tuple):(row,col)
    playerClicks = [] # keep track of player clicks --> two tuples, [(6,4),(4,4)]

    # Main while loop
    while running:
        for e in p.event.get():
            # Exit the program if we quit
            if e.type == p.QUIT:
                running = False

            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # get location of the mouse

                # Calculate the row and col of current mouse click
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                # To prevent the player from moving a piece to the same position
                if sqSelected == (row, col):
                    sqSelected = () #deselect square
                    playerClicks = []
                # If it is a different square, actually append the move to playerClicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                # If this is the second click, move the piece
                # Else, only append sqSelected to playerClicks
                if len(playerClicks) == 2:
                    # Create the Move object
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    # Debugging -- print the notation for the move
                    print(move.getChessNotation())

                    if move in validMoves:
                        # Make the move
                        gs.makeMove(move)
                        moveMade = True
                        # Clear the variables for future moves
                        sqSelected = ()
                        playerClicks = []
                    # If not a valid move, just make this the initial square selected
                    else:
                        playerClicks = [sqSelected]

            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo a move when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        # If a move was made, generate the valid moves for the new state of the board
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