from random import choice
from cell import Cell, Point
from time import sleep


class Maze:
    def __init__(self, x, y, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self.x = x
        self.y = y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._visited_cells = []
        self._create_cells()
        self._draw_cells()
        self._break_entrance_and_exit()
        self._break_walls_r()
        self._visited_cells = []

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i=0, j=0):
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        cell1 = self._cells[i][j]
        self._visited_cells.append(cell1)
        unvisited = self._get_unvisited_neighbor_r(i, j)
        if unvisited is None:
            return False
        for indexes in unvisited:
            cell2_i, cell2_j, direction = indexes
            cell2 = self._cells[cell2_i][cell2_j]
            wall_open = (
                direction == "up"
                and cell1.has_top_wall == False
                or direction == "right"
                and cell1.has_right_wall == False
                or direction == "down"
                and cell1.has_bottom_wall == False
                or direction == "left"
                and cell1.has_left_wall == False
            )
            if wall_open:
                cell1.draw_move(cell2)
                self._animate()
                self._cells.append(cell2)
                result = self._solve_r(cell2_i, cell2_j)
                if result:
                    return True
                cell1.draw_move(cell2, undo=True)
                self._animate()
        return False

    def _animate(self):
        self.win.redraw()
        sleep(0.01)

    def _draw_cells(self):
        for i in range(0, len(self._cells)):
            for j in range(0, len(self._cells[i])):
                self._cells[i][j].draw()
                self._animate()

    def _create_cells(self):
        for _ in range(0, self.num_rows):
            self._cells.append([None] * self.num_cols)
        current_y = self.y
        for i in range(0, len(self._cells)):
            current_x = self.x
            for j in range(0, len(self._cells[i])):
                point1 = Point(current_x, current_y)
                current_x += self.cell_size_x
                point2 = Point(current_x, current_y + self.cell_size_x)
                self._cells[i][j] = Cell(point1, point2, self.win)
            current_y += self.cell_size_y

    def _get_unvisited_neighbor_r(self, i, j):
        unvisited = []
        test_indexes = [
            (i - 1, j, "up"),
            (i, j + 1, "right"),
            (i + 1, j, "down"),
            (i, j - 1, "left"),
        ]
        for indexes in test_indexes:
            i, j, _ = indexes
            row_in_bounds = i >= 0 and i < self.num_rows
            col_in_bounds = j >= 0 and j < self.num_cols
            if row_in_bounds and col_in_bounds:
                if self._cells[i][j] not in self._visited_cells:
                    unvisited.append(indexes)
        if unvisited:
            return unvisited
        return None

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_left_wall = False
        entrance.draw()
        self._animate()
        exit = self._cells[self.num_rows - 1][self.num_cols - 1]
        exit.has_right_wall = False
        exit.draw()
        self._animate()

    def _break_walls_r(self, i=None, j=None):
        if i is None or j is None:
            i = choice(range(0, self.num_rows))
            j = choice(range(0, self.num_cols))
        cell1 = self._cells[i][j]
        self._visited_cells.append(cell1)
        count = 0
        cell_count = self.num_rows * self.num_cols
        while count < cell_count:
            count += 1
            unvisited = self._get_unvisited_neighbor_r(i, j)
            if unvisited is None:
                return
            cell2_i, cell2_j, direction = choice(unvisited)
            cell2 = self._cells[cell2_i][cell2_j]
            if direction == "up":
                cell1.has_top_wall = False
                cell2.has_bottom_wall = False
            if direction == "right":
                cell1.has_right_wall = False
                cell2.has_left_wall = False
            if direction == "down":
                cell1.has_bottom_wall = False
                cell2.has_top_wall = False
            if direction == "left":
                cell1.has_left_wall = False
                cell2.has_right_wall = False
            cell1.draw()
            cell2.draw()
            self._animate()
            self._break_walls_r(cell2_i, cell2_j)
