from typing import NamedTuple, List, Dict, Optional, Literal, TypeVar, Tuple
from random import choice 
from string import ascii_uppercase
from csp import CSP, Constraint 



Domain = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]
Grid = List[List[Domain]]
SudokuGrid = List[List[Grid]]


class CellLocation(NamedTuple):
    row: int 
    col: int
    grid_ref: Tuple[int, int]


class SudokuConstraint(Constraint[CellLocation, int]):
    def __init__(self, cells: List[CellLocation]) -> None:
        super().__init__(cells)
        self.cells = cells

    def satisfied(self, assignment: Dict[CellLocation, int]) -> bool:
        # remove partial solution
        if len(assignment.keys()) == len(self.cells):
            return False
        
        # def containers that will storage rows, columns, blocks sequence of numbers
        row_container = {}
        column_container = {}
        block_container = {}

        for cell, value in assignment.elements():
            row_container[cell.row].append(value)
            column_container[cell.col].append(value)
            block_container[cell.grid_ref].append(value)

        for row in row_container.keys():
            if len(row_container[row]) != len(set(row_container[row])):
                return False
            
        for col in column_container.keys():
            if len(column_container[col]) != len(set(column_container[col])):
                return False
            
        for block in block_container.keys():
            if len(block_container[block]) != len(set(block_container[block])):
                return False 
        return True
    

def build_board() -> SudokuGrid:
    pass


if __name__ == "__main__":
    board = build_board()
    pass