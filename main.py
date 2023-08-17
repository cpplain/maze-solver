from maze import Maze
from window import Window

def main():
    win = Window(800, 600)

    maze = Maze(40, 40, 13, 18, 40, 40, win)
    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()
