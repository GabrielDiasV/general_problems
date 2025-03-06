from enum import Enum
from typing import List, NamedTuple, Callable, Optional, Generic
import random
from math import sqrt
from generic_search import Node, Stack, dfs, bfs, node_to_path, astar

class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int 
    column: int 


class Maze:

    def __init__(self, rows:int = 10, columns:int = 10, start:MazeLocation = MazeLocation(0, 0), goal:MazeLocation = MazeLocation(9, 9), sparseness:float = 0.2) -> None:
        self._rows = rows 
        self._columns = columns
        self.start = start 
        self.goal = goal
        # Creates a grid of empty cells
        self._grid:List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        # Fill in blocked cells
        self._randomly_fill(rows, columns, sparseness)
        # Fill in the start and goal locations
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL


    def _randomly_fill(self, rows:int, columns:int, sparseness:float) -> None:
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED


    def __str__(self) -> str:
        output = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        
        return output
    

    def goal_test(self, ml:MazeLocation) -> bool:
        return ml == self.goal
    

    def successors(self, ml:MazeLocation) -> List[MazeLocation]:
        locations:List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        
        return locations
    

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH

        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY

        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    @staticmethod
    def enclidian_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
        def distance(ml: MazeLocation) -> float:
            xdist = ml.column - goal.column
            ydist = ml.row - goal.row

            return sqrt((xdist * xdist) + (ydist * ydist))
        return distance
    
    @staticmethod
    def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
        def distance(ml: MazeLocation) -> float:
            xdist = abs(ml.column - goal.column)
            ydist = abs(ml.row - goal.row)

            return xdist + ydist
        return distance


if __name__ == '__main__':
    maze: Maze = Maze()
    print(maze)

    solution1: Optional[Node[MazeLocation]] = dfs(maze.start, maze.successors, maze.goal_test)
    if solution1 is None:
        print("No solution found using depth-first search!")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)

        maze.mark(path1)
        print(maze)
        maze.clear(path1)

    solution2: Optional[Node[MazeLocation]] = bfs(maze.start, maze.successors, maze.goal_test)
    if solution2 is None:
        print("No solution found using breadth-first search!")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)

        maze.mark(path2)
        print(maze)
        maze.clear(path2)

    distance = maze.manhattan_distance(maze.goal)
    solution3: Optional[Node[MazeLocation]] = astar(maze.start, maze.goal_test, maze.successors, distance)
    if solution3 is None:
        print("No solution found using A* search!")
    else:
        path3: List[MazeLocation] = node_to_path(solution3)

        maze.mark(path3)
        print(maze)
        maze.clear(path3)

