from typing import NamedTuple, List, Dict, Optional, Literal, TypeVar, Tuple
from random import choice 
from string import ascii_uppercase
from csp import CSP, Constraint 

V = TypeVar("V")

# type alias for grid
Fill = Literal[" ", "X"]
Grid = List[List[V]]


class GridLocation(NamedTuple):
    row: int
    column: int


def display_grid(grid: Grid[Fill]) -> None:
    for row in grid:
        print(row)


def initialize_grid(rows:int, columns: int) -> Grid[Fill]:
    return [[" " for c in range(columns)] for r in range(rows)]


def generate_domain(rectangles: List[Tuple[int, int]], grid:Grid[Fill]) -> Dict[Tuple[int, int], List[Grid[GridLocation]]]:
    domain = {}
    x_max = len(grid)
    y_max = len(grid[0])
    for rectangle in rectangles:
        domain[rectangle] = []
        x_dim = rectangle[0]
        y_dim = rectangle[1]
        for row in range(x_max):
            if row + y_dim <= x_max:
                for column in range(y_max):
                    if column + x_dim <= y_max:
                        domain[rectangle].append([[]])
    return domain


class BoardConstraint(Constraint[Tuple[int, int], Grid[GridLocation]]):
    def __init__(self, rectangles: List[Tuple[int, int]]):
        super().__init__(rectangles)
        self.rectangles = rectangles

    def satisfied(self, assignment: Dict[Tuple[int, int], Grid[GridLocation]]):
        if len(self.rectangles) != len(assignment):
            return False
        
        locations_list = []
        for grid in assignment.values():
            display_grid(grid)
            for row in grid:
                for grid_loc in row:
                    locations_list.append(grid_loc)
        
        return len(locations_list) == len(set(locations_list))


if __name__ == "__main__":
    inicial_grid = initialize_grid(9, 9)
    rectangles = [(3, 2), (2, 3), (2, 2)]
    domain = generate_domain(rectangles, inicial_grid)

    print(domain)

    csp: CSP[Tuple[int, int], Grid[GridLocation]] = CSP(rectangles, domain)
    csp.add_constraint(BoardConstraint(rectangles))
    solution: Optional[Dict] = csp.backtracking_search()
    if solution == None:
        print("No solution found!")
    else:
        print(solution)
