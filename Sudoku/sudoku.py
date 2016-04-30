from collections import deque
from copy import deepcopy
import sys
from sudokuextract.extract import extract_sudoku, load_image, predictions_to_suduko_string


class SudokuSolver(object):
    def __init__(self, from_string):
        self.sudoku = self.init_sudoku(from_string)
        self.sudoku_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.sudoku_empty_number = "0"
        self.sudoku_size_per_line = len(self.sudoku_numbers)

    def init_sudoku(self, sudoku_string):
        return [list(line) for line in sudoku_string.split()]

    def get_remainning_pos(self, board):
        """
        :param board: List[List[String]]
        :return: Int
        """
        return sum([1 for row in board for c in row if c == self.sudoku_empty_number])

    def get_first_unknown(self, board):
        """
        :param board: List[List[String]]
        :return: Int, Int
        """
        for i in xrange(self.sudoku_size_per_line):
            for j in xrange(self.sudoku_size_per_line):
                if board[i][j] == self.sudoku_empty_number:
                    return i, j

    def get_possible(self, board, i, j):
        """
        :param board: List[List[String]]
        :param i: Int
        :param j: Int
        :return: List[String]
        """
        row = board[i]
        col = [r[j] for r in board]
        sqr = [board[a + 3 * (i / 3)][b + 3 * (j / 3)] for a in xrange(3) for b in xrange(3)]
        impossible = set(row + col + sqr)
        R = []
        for F in self.sudoku_numbers:
            if F in impossible:
                pass
            else:
                R.append(F)
        return R

    def get_next_state(self, board):
        """
        :param board: List[List[String]]
        :return: List[List[List[String]]]
        """
        R = []
        i, j = self.get_first_unknown(board)
        possibles = self.get_possible(board, i, j)
        for possible in possibles:
            S = deepcopy(board)
            S[i][j] = possible
            R.append(S)
        return R

    def solver(self, board):
        """
        :param board: List[List[String]]
        :return: String
        """
        q = deque()
        q.appendleft(board)
        while len(q) > 0:
            current_state = q.popleft()
            if self.get_remainning_pos(current_state) == 0:
                return current_state
            next_states = self.get_next_state(current_state)
            for next_state in next_states:
                q.appendleft(next_state)
        return None

    def run(self):
        solve = self.solver(self.sudoku)
        if solve:
            return "\n".join(["".join(line) for line in solve])
        else:
            return solve

if __name__ == "__main__":
    img = load_image(sys.argv[1])
    predictions, sudoku_box_images, whole_sudoku_image = extract_sudoku(img)
    sudoku = predictions_to_suduko_string(predictions)
    print "origin input"
    print sudoku
    print "result output"
    print SudokuSolver(sudoku).run()
