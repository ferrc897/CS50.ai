import re
import random

class Minesweeper:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.mines = 0
        self.difficulty = 1
        self.board = []
        self.game_setted = False
        self.lose = False
        self.win = False
        self.valid_moves = set()


    def board_characteristics(self):
        if self.difficulty == 1:
            self.width, self.height, self.mines = 8, 8, 10

        elif self.difficulty == 2:
            self.width, self.height, self.mines = 16, 16, 40

        elif self.difficulty == 3:
            self.width, self.height, self.mines = 26, 16, 99



    def create_board(self):
        for i in range(self.height):
            row = []
            for j in range(self.width):
                cell = Cell(self, (i,j))
                row.append(cell)
                self.valid_moves.add(cell.position)
            self.board.append(row)



    def move(self, move):
        i, j = move
        if not self.game_setted:
            self.set_game(move)

        if move not in self.valid_moves:
            print("Invalid move")
            raise ValueError

        self.board[i][j].reveal_cells()

        if self.board[i][j].mine:
            self.lose = True


        if len(self.valid_moves) == self.mines:
            self.win = True


    def set_game(self, move):
        initial_move = Cell(self, move)
        adyacent_to_initial_move = initial_move.adjacent_move()
        for _ in range(self.mines):
            while True:
                try:
                    i = random.randint(0, self.height - 1)
                    j = random.randint(0, self.width - 1)

                    if self.board[i][j].mine or self.board[i][j].position in adyacent_to_initial_move or self.board[i][j].position not in self.valid_moves:
                        raise ValueError
                    else:
                        self.board[i][j].mine = True
                    self.game_setted = True
                    break

                except ValueError:
                    pass


class Cell:
    def __init__(self, game, position):
        self.game = game
        self.show = False
        self.mine = False
        self.position = position
        self.count = 0


    def __str__(self):
        if self.mine and self.show:
            return "💣"

        if self.count > 0:
            numbers = ["1️⃣ ", "2️⃣ ", "3️⃣ ", "4️⃣ ", "5️⃣ ", "6️⃣ ", "7️⃣ ", "8️⃣ ", "9️⃣ "]
            return numbers[self.count - 1]

        if not self.show:
            return "🟩"

        if self.show:
            return "🟫"


    def count_mines(self):
        count = 0
        max_y, min_y, max_x, min_x = self.adjacent_cells()
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                if self.game.board[i][j].mine:
                    count += 1

        self.count = count


    def adjacent_cells(self):
        y, x = self.position
        max_y = y + 1
        min_y = y - 1
        max_x = x + 1
        min_x = x - 1

        if max_y > self.game.height - 1:
            max_y = self.game.height - 1

        if min_y < 0:
            min_y = 0

        if max_x > self.game.width - 1:
            max_x = self.game.width - 1

        if min_x < 0:
            min_x = 0

        return max_y, min_y, max_x, min_x


    def reveal_cells(self):
        max_y, min_y, max_x, min_x = self.adjacent_cells()
        self.count_mines()
        self.show = True
        self.game.valid_moves.remove(self.position)
        if self.count == 0 and not self.mine:
            for i in range(min_y, max_y + 1):
                for j in range(min_x, max_x + 1):
                    if not self.game.board[i][j].show:
                        self.game.board[i][j].reveal_cells()


    def adjacent_move(self):
        adjacent_cells = set()
        max_y, min_y, max_x, min_x = self.adjacent_cells()
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                adjacent_cells.add(self.game.board[i][j].position)
        return adjacent_cells


ABC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V','W','X','Y','Z']


def main():
    MS = Minesweeper()
    while True:
        try:
            MS.difficulty = int(input("Choose difficulty:\n1.easy\n2.medium\n3.hard\n"))
            if MS.difficulty < 1 or MS.difficulty > 3:
                raise ValueError
            break
        except ValueError:
            print("Write 1, 2 or 3")
            pass
    MS.board_characteristics()
    MS.create_board()
    print()

    while True:
        while True:
            try:
                display_board(MS)
                MS.move((create_coord(input("Write a coordinate (e.g A1): "))))
                break
            except (ValueError, IndexError):
                pass

        if MS.lose:
            for i in range(MS.height):
                for j in range(MS.width):
                    if MS.board[i][j].mine:
                        MS.board[i][j].show = True

            display_board(MS)
            print("You lost :(")
            return 0


        if MS.win:
            print("You won :)")
            return 0


def display_board(game):
    print("    ", end="")

    for _ in range(game.width):
        print(ABC[_], end= " ")

    print()

    for i in range(game.height):
        if i + 1 < 10:
            print(i + 1, end="  ")

        else:
            print(i + 1, end=" ")

        for j in range(game.width):
            print(game.board[i][j], end="")

        print()


def create_coord(coord):
    matches = re.search(r"([A-Z][A-Z]?)([0-9][0-9]?)", coord.upper())
    if matches:
        i, j = matches.groups()
        i = ABC.index(i)
        j = int(j) - 1
        return (j, i)
    else:
        print("Invalid Coordinate")
        raise ValueError


if __name__ == "__main__":
    main()