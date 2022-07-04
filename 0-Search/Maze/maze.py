import sys

sys.path.append("../Algorithms")

from classes import *
from DFS import *
from BFS import *
from GBFS import *
from A_star import *


class Maze:
    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

    def print(self, solution=None, explored=None):
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("███", end="")
                elif (i, j) == self.start:
                    print(" A ", end="")
                elif (i, j) == self.goal:
                    print(" B ", end="")
                elif solution is not None and (i, j) in solution:
                    print(" x ", end="")
                elif explored is not None and (i, j) in explored:
                    print(" o ", end="")
                else:
                    print("   ", end="")
            print()
        print("\n")

    def draw(self, save=False, filename=None, solution=None, explored=None):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA", (self.width * cell_size, self.height * cell_size), "black"
        )
        draw = ImageDraw.Draw(img)

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif explored is not None and (i, j) in explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    (
                        [
                            (j * cell_size + cell_border, i * cell_size + cell_border),
                            (
                                (j + 1) * cell_size - cell_border,
                                (i + 1) * cell_size - cell_border,
                            ),
                        ]
                    ),
                    fill=fill,
                )

        img.show()

        if save and filename is None:
            raise Exception("Please provide a filename for the image output.")
        elif save:
            img.save(filename)

    def solve(
        self,
        print_maze=False,
        print_solution=False,
        print_explored=False,
        draw_maze=False,
        save_maze=False,
        maze_filename=None,
        draw_solution=False,
        save_solution=False,
        solution_filename=None,
        draw_explored=False,
        save_explored=False,
        explored_filename=None,
    ):
        if print_maze:
            print("\nOriginal maze:")
            self.print()
        if draw_maze:
            self.draw()
        if save_maze:
            self.draw(save=True, filename=maze_filename)

        up = Move(action=lambda x: [(x[0] - 1, x[1])], move_id="up")
        down = Move(action=lambda x: [(x[0] + 1, x[1])], move_id="down")
        left = Move(action=lambda x: [(x[0], x[1] - 1)], move_id="left")
        right = Move(action=lambda x: [(x[0], x[1] + 1)], move_id="right")

        possible_moves = (up, down, left, right)

        def moves(state):
            actual_moves = []
            for move in possible_moves:
                [(i, j)] = move.action(state)
                if (
                    i >= 0
                    and i < self.height
                    and j >= 0
                    and j < self.width
                    and not self.walls[i][j]
                ):
                    actual_moves.append(move)

            return actual_moves

        problem = Search_Problem(
            starting_state=self.start, goal_state=self.goal, moves=moves
        )

        solution_nodes, explored_nodes = DFS(
            problem,
            # lambda x: abs(x.state[0] - self.goal[0]) + abs(x.state[1] - self.goal[1]),
        )
        solution = [step.state for step in solution_nodes]
        explored = [explr.state for explr in explored_nodes.nodes]

        if print_solution:
            print("Solution:")
            self.print(solution=solution)
        if print_explored:
            print("Explored states:")
            self.print(explored=explored)
        if draw_solution:
            self.draw(solution=solution)
        if save_solution:
            self.draw(save=True, filename=solution_filename, solution=solution)
        if draw_explored:
            self.draw(explored=explored)
        if save_explored:
            self.draw(save=True, filename=explored_filename, explored=explored)

        return solution_nodes, explored_nodes


if __name__ == "__main__":
    maze = Maze("maze examples/maze2.txt")
    maze.solve(draw_solution=True, draw_explored=True)
