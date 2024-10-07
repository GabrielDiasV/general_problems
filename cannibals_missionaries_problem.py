from __future__ import annotations
from typing import List, Optional
from generic_search import bfs, Node, node_to_path, PriorityQueue 

MAX_NUM: int = 3


class MCState:
    def __init__(self, missionaries: int, cannibals:int, boat: bool) -> None:
        self.wc: int = cannibals
        self.wm: int = missionaries
        self.em: int = MAX_NUM - missionaries
        self.ec: int = MAX_NUM - cannibals
        self.wboat: bool = boat

        if ((self.wm == MAX_NUM) and (self.wc == MAX_NUM) and not boat):
            raise('ValueError. Invalid Input.')
        
        if ((self.em == MAX_NUM) and (self.ec == MAX_NUM) and boat):
            raise('ValueError. Invalid Input.')

    def __str__(self) -> str:
        return (f'''On the west bank there are {self.wm} missionaries and {self.wc} cannibals.\n
On the east bank there are {self.em} missionaries and {self.ec} cannibals \n
The boat is on the {"west" if self.wboat else "east"} bank.
                ''')
    
    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm > 0:
            return False
        if self.em < self.ec and self.em > 0:
            return False
        return True

    def goal_test(self) -> bool:
        return (self.ec == MAX_NUM and self.em == MAX_NUM and self.is_legal)
    
    def successors(self) -> List[MCState]:
        sucs: List[MCState] = []
        if self.wboat:
            if self.wm > 1:
                sucs.append(MCState(self.wm - 2, self.wc, not self.wboat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.wboat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.wboat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.wboat))
            if self.wc > 0 and self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.wboat))
        else:
            if self.em > 1:
                sucs.append(MCState(self.em - 2, self.ec, self.wboat))
            if self.em > 0:
                sucs.append(MCState(self.em - 1, self.ec, self.wboat))
            if self.ec > 1:
                sucs.append(MCState(self.em, self.ec - 2, self.wboat))
            if self.ec > 0:
                sucs.append(MCState(self.em, self.ec - 1, self.wboat))
            if self.ec > 0 and self.em > 0:
                sucs.append(MCState(self.em - 1, self.ec - 1, self.wboat))
        return [state for state in sucs if state.is_legal]
    
    @staticmethod
    def display_solution(path: List[MCState]):
        if len(path) == 0:
            return 
        old_state: MCState = path[0]
        print(old_state)
        for currenct_state in path[1:]:
            if currenct_state.wboat:
                print(f"{old_state.em - currenct_state.em} missionaries and {old_state.ec - currenct_state.ec} cannibals moved from the east bank to the west bank. \n")
            else:
                print(f"{old_state.wm - currenct_state.wm} missionaries and {old_state.wc - currenct_state.wc} cannibals moved from the west bank to the east bank .\n")

            print(currenct_state)
            old_state = currenct_state


if __name__ == "__main__":
    start: MCState = MCState(MAX_NUM, MAX_NUM, True)
    solution: Optional[Node[MCState]] = bfs(start, MCState.successors, MCState.goal_test)
    if solution is None:
        print("No solution found!")
    else:
        path: List[MCState] = node_to_path(solution)
        MCState.display_solution(path)
