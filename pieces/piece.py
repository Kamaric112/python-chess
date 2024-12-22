class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False

    def get_valid_moves(self, board):
        pass


class Pawn(Piece):
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        direction = -1 if self.color == 'white' else 1

        # Forward move
        if 0 <= row + direction < 8:
            if board[row + direction][col] is None:
                valid_moves.append((row + direction, col))
                # Initial two-square move
                if ((self.color == 'white' and row == 6) or
                        (self.color == 'black' and row == 1)):
                    if board[row + 2 * direction][col] is None:
                        valid_moves.append((row + 2 * direction, col))

        # Capture moves
        for c in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + c < 8:
                target = board[row + direction][col + c]
                if target and target.color != self.color:
                    valid_moves.append((row + direction, col + c))

        return valid_moves


class Knight(Piece):
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for move in moves:
            new_row = row + move[0]
            new_col = col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    valid_moves.append((new_row, new_col))

        return valid_moves


class Bishop(Piece):
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            for i in range(1, 8):
                new_row = row + i * direction[0]
                new_col = col + i * direction[1]
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                target = board[new_row][new_col]
                if target is None:
                    valid_moves.append((new_row, new_col))
                elif target.color != self.color:
                    valid_moves.append((new_row, new_col))
                    break
                else:
                    break

        return valid_moves


class Rook(Piece):
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for direction in directions:
            for i in range(1, 8):
                new_row = row + i * direction[0]
                new_col = col + i * direction[1]
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                target = board[new_row][new_col]
                if target is None:
                    valid_moves.append((new_row, new_col))
                elif target.color != self.color:
                    valid_moves.append((new_row, new_col))
                    break
                else:
                    break

        return valid_moves


class Queen(Piece):
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for direction in directions:
            for i in range(1, 8):
                new_row = row + i * direction[0]
                new_col = col + i * direction[1]
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                target = board[new_row][new_col]
                if target is None:
                    valid_moves.append((new_row, new_col))
                elif target.color != self.color:
                    valid_moves.append((new_row, new_col))
                    break
                else:
                    break

        return valid_moves


class King(Piece):
    def get_valid_moves(self, board):
        valid_moves = []
        row, col = self.position
        moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for move in moves:
            new_row = row + move[0]
            new_col = col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    valid_moves.append((new_row, new_col))

        return valid_moves
