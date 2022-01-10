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
        self.moveFunctions = {'p': self.getPawnMoves,
                              'R': self.getRookMoves,
                              'B': self.getBishopMoves,
                              'N': self.getKnightMoves,
                              'Q': self.getQueenMoves,
                              'K': self.getKingMoves
                              }


    def makeMove(self, move):
        """Takes in a valid move and updates the board accordingly. Also updates the log and changes the player turn.

        :param move: a Move object
        """

        self.board[move.startRow][move.startCol] = "--" # the position we started from becomes blank
        self.board[move.endRow][move.endCol] = move.pieceMoved # the piece goes to the target position

        self.moveLog.append(move)  # keep track of the moves
        self.whiteToMove = not self.whiteToMove  # change the player to move

    def undoMove(self):
            if len(self.moveLog) != 0:
                move = self.moveLog.pop()
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                self.whiteToMove = not self.whiteToMove  # change the player to move

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == '--':
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #açılışta iki ileri sürmek
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c-1 >= 0: #sola capture
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= 7: #sağa capture
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        else:
            if self.board[r + 1][c] == '--':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':  # açılışta iki ileri sürmek
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # sola capture
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # sağa capture
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
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

    def __init__(self, startSq, endSq, board):
        # Get the rows and cols of the starting and ending squares
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol] # get the movedPiece
        self.pieceCaptured = board[self.endRow][self.endCol]  # might be "--"

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """
    Overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    """
    Get the chess notation of the move using the rankFile helper function.
    """
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    # Create dictionaries for converting chess notation to computer notation and vice versa
    # Maps keys to values
    # Key : Value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    # Reverse the values and keys in the dictionary
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    """
    Convert computer notation to rank-file notation using the dictionaries above.
    """
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]