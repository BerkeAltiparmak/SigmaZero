"""
Handle user input and display current GameState object
"""

import numpy as np

class GameState:
    """
    Class used to represent the current state of the chessboard.
    """
    def __init__(self):
        """
        Initialization of the board

        First character: color of the piece
        Second character: type of piece
        "--" if there is no piece there at that moment
        """

        # Declare the initial chessboard as a np array of strings
        self.board = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']], dtype = 'U')

        # For tracking whose turn it is
        self.whiteToMove = True

        self.moveLog = []

        # Dictionary from character to function
        # Map every letter to function that should be called
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves,
                              'B': self.getBishopMoves, 'N': self.getKnightMoves,
                              'Q': self.getQueenMoves,'K': self.getKingMoves}

        # Keeping track of the kings' locations
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)

        # Keeping track of mates
        self.checkMate = False
        self.staleMate = False




    def makeMove(self, move):
        """Takes in a valid move and updates the board accordingly. Also updates the log and changes the player turn.
        NOTE: Does not work for castling, en-passant and pawn promotion.
        :param move: a Move object
        """

        self.board[move.startRow][move.startCol] = "--" # the position we started from becomes blank
        self.board[move.endRow][move.endCol] = move.pieceMoved # the piece goes to the target position

        self.moveLog.append(move)  # keep track of the moves
        self.whiteToMove = not self.whiteToMove  # change the player to move

        # Update king's location if the moved piece is the king
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)



    def undoMove(self):
            """
            Undo the last move, if it's not the first move.
            """
            if len(self.moveLog) != 0: # check if it's not the first move
                # Remove and get the last move
                move = self.moveLog.pop()
                # Put the pieces back
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured

                self.whiteToMove = not self.whiteToMove  # change the player to move

                # Update king's location if the moved piece is the king
                if move.pieceMoved == 'wK':
                    self.whiteKingLocation = (move.startRow, move.startCol)
                elif move.pieceMoved == 'bK':
                    self.blackKingLocation = (move.startRow, move.startCol)


    def getValidMoves(self):
        """
        Remove the Move objects from the moves list that cause checks and return the moves list.
        :return: a list of all valid moves of Move objects
        """
        #1 - Generate all possible moves
        moves = self.getAllPossibleMoves()
        #2 - For each move, make the move
        for i in range(len(moves) - 1, -1, -1): # loop through the moves list backwards
            self.makeMove(moves[i])
            #3 - Generate all opponent's moves
            #4 - If one move attacks your king, remove the move
            self.whiteToMove = not self.whiteToMove # swap back since we made a move in step 2
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0: # either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else: # to prevent crashes when we undo moves
            self.checkMate = False
            self.staleMate = False

        return moves

    def inCheck(self):
        """
        Determine if the current player is in check.
        :return:
        """
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        """
        Determine if the enemy can attack the square (r,c).
        :param r: row of the square
        :param c: col of the square
        :return: True if the square can be attacked, False otherwise
        """
        self.whiteToMove = not self.whiteToMove # switch to enemy POV
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # square is under attack
                return True
        return False

    def getAllPossibleMoves(self):
        """
        Generates all possible moves without considering checks.
        :return: A list of Move objects of legal moves.
        """

        moves = []
        # Loop through the 2D array and check every position for a piece
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] # the first letter of the string denotes the player (b or w)
                # Check who's turn it and if it matches,
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        """
        Get all the pawn moves for the pawn located at r,c and add these moves to the moves list.

        :param r: the row of the pawn
        :param c: the col of the pawn
        :param moves: a list of the legal Move objects so far
        """
        # White pawn moves
        if self.whiteToMove:
            # If the position in front of the pawn is empty
            if self.board[r-1][c] == '--':
                # Append that possible move
                moves.append(Move((r,c), (r-1,c), self.board))
                # initial pawn move two squares
                if (r == 6) and (self.board[r-2][c] == '--'):
                    moves.append(Move((r,c), (r-2,c), self.board))

            # Captures
            if c-1 >= 0: # capturing to the left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= len(self.board[0]) - 1: # capturing to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        # Black pawn moves
        else:

            if self.board[r + 1][c] == '--':
                moves.append(Move((r, c), (r + 1, c), self.board))
                # initial pawn move two squares
                if (r == 1) and (self.board[r + 2][c]) == '--':
                    moves.append(Move((r, c), (r + 2, c), self.board))

            # Captures
            if c - 1 >= 0:  # capturing to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if (c + 1) <= len(self.board[0]) - 1:  # capturing to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        """
        :param r: row of the rook
        :param c: column of the rook
        :param moves: a list of the legal Move objects so far
        """
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if (0 <= endRow < len(self.board)) and (0 <= endCol < len(self.board[0])):
                    endPiece = self.board[endRow][endCol]
                    # If the square is empty, add it to the list
                    if endPiece == '--':
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    # If the square has an enemy piece, add it to the list and break
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    # If it is our piece, directly break
                    else:
                        break
                # If it is off the board, break
                else:
                    break


    def getKnightMoves(self, r, c, moves):
        directions = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        allycolor = 'w' if self.whiteToMove else 'b'
        for m in directions:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allycolor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else: # önemli (kendi taşı varsa)
                        break
                else: # önemli (off board)
                    break


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r,c, moves)

    def getKingMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        allycolor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allycolor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():
    """
    A class representing a move with a starting position, ending position and a GameState object.
    """
    def __init__(self, startSq, endSq, board):
        # Get the rows and cols of the starting and ending squares
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol] # get the movedPiece
        self.pieceCaptured = board[self.endRow][self.endCol]  # might be "--"

        # Generate moveID unique to each starting and ending square
        # For comparison to other Move objects
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):
        """
        Overriding the equals method so we can compare two Move objects.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        """
        Get the chess notation of the move using the rankFile helper function.
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    # Create dictionaries for converting chess notation to computer notation and vice versa
    # Maps keys to values
    # Key : Value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    # Reverse the values and keys in the dictionary
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def getRankFile(self, r, c):
        """
        Convert computer notation to rank-file notation using the dictionaries above.
        """
        return self.colsToFiles[c] + self.rowsToRanks[r]