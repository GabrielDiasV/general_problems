from typing import NamedTuple, List, Dict, Optional
from random import choice 
from string import ascii_uppercase
from csp import CSP, Constraint 

# type alias for grid
Grid = List[List[str]]


class GridLocation(NamedTuple):
    row: int
    column: int


def generate_grid(rows:int, columns: int) -> Grid:
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))


def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    lenght: int = len(word)

    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + lenght + 1)
            rows: range = range(row, row + lenght + 1)
            if col + lenght <= width:
                domain.append([GridLocation(row, c) for c in columns])
                if row + lenght <= height:
                    domain.append([GridLocation(r, col + (r - row)) for r in rows])

            if row + lenght <= height:
                domain.append([GridLocation(r, col) for r in rows])
                if col - lenght >= 0 :
                    domain.append([GridLocation(r, col - (r - row)) for r in rows]) 

    return domain


class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words = words

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        all_locations = [locs for values in assignment.values() for locs in values]

        # if there is any element duplicated, them means two works are occupying the same space, so the state is invalid as solution
        return len(set(all_locations)) == len(all_locations)
    

if __name__ == "__main__":
    grid: Grid = generate_grid(9 , 9)
    words: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY"]
    locations: Dict[str, List[List[GridLocation]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)
    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words)) 
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()

    if solution is None:
        print("No solution found!")
    else:
        for word, grid_locations in solution.items():
            # random reverse half the time
            if choice([True, False]):
                grid_locations.reverse()

            for index, letter in enumerate(word):
                (row, col) = (grid_locations[index].row, grid_locations[index].column)
                grid[row][col] = letter

        display_grid(grid)