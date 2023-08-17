class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2
        )
        canvas.pack()


class Cell:
    def __init__(self, point1, point2, win=None):
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.x1 = point1.x
        self.y1 = point1.y
        self.x2 = point2.x
        self.y2 = point2.y
        self.center_x = (self.x1 + self.x2) // 2
        self.center_y = (self.y1 + self.y2) // 2
        self.win = win

    def draw(self):
        wall_color = "white"
        background = "black"
        top = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
        top.draw(self.win.canvas, wall_color if self.has_top_wall else background)
        right = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
        right.draw(self.win.canvas, wall_color if self.has_right_wall else background)
        bottom = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
        bottom.draw(self.win.canvas, wall_color if self.has_bottom_wall else background)
        left = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
        left.draw(self.win.canvas, wall_color if self.has_left_wall else background)

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "grey"
        start = Point(self.center_x, self.center_y)
        end = Point(to_cell.center_x, to_cell.center_y)
        line = Line(start, end)
        line.draw(self.win.canvas, color)
