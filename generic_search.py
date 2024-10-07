from __future__ import annotations
from typing import List, Dict, Iterable, Tuple, Any, Container, TypeVar, Sequence, Optional, Deque, Set, Callable, Generic
from typing import Protocol
from heapq import heappush, heappop
import bisect

T = TypeVar("T")
C = TypeVar("C", bound="Comparable")


class Node(Generic[T]):

    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Stack(Generic[T]):
        
        def __init__(self) -> None:
            self._container:List[T] = []
    
        def push(self, item: T) -> None:
            self._container.append(item)
    
        def pop(self) -> T:
            return self._container.pop()
        
        @property
        def empty(self) -> bool:
            return not self._container
    
        def __repr__(self) -> str:
            return repr(self._container)


class Queue(Generic[T]):

    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()
    
    @property
    def empty(self) -> bool:
        return not self._container
    
    def __repr__(self) -> str:
        return repr(self._container)
    

class Comparable(Protocol):

    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        return self < other and self != other

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return self > other or self == other

    def __ne__(self: C, other: C) -> bool:
        return not self == other
    
    
class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container
    
    def push(self, item: T) -> None:
        heappush(self._container, item)

    def pop(self) -> T:
        return heappop(self._container)
    
    def __repr__(self) -> str:
        return repr(self._container)


def linear_search(iterable: Iterable[T], target: T) -> bool:
    for item in iterable:
        if item == target:
            return True
        
    return False 


def binary_search(sequence: Sequence[C], key_target: C) -> bool:
    low = 0
    high = len(sequence) - 1
    while low <= high:
        mid = (low + high) // 2 
        if sequence[mid] < key_target:
            low = mid + 1
        elif sequence[mid] > key_target:
            high = mid - 1
        else:
            return True
    
    return False


def dfs(start: T, successors: Callable[[T],List[T]], goal_test: Callable[[T], bool]) -> Optional[Node[T]]:

    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(start, None))

    visited: Set[T] = {start}

    while not frontier.empty:
        current_node = frontier.pop()
        if goal_test(current_node.state):
            return current_node
        for child in successors(current_node.state):
            if child in visited:
                continue
            frontier.push(Node(child, current_node))
            visited.add(child)

    return None


def bfs(start: T, successors: Callable[[T], List[T]], goal_test: Callable[[T], bool]) -> Optional[Node[T]]:
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(start, None))

    visited: Set[T] = {start}

    while not frontier.empty:
        current_node = frontier.pop()
        if goal_test(current_node.state):
            return current_node
        for child in successors(current_node.state):
            if child in visited:
                continue
            frontier.push(Node(child, current_node))
            visited.add(child)

    return None


def astar(start:T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]], heuristic: Callable[[T], float]) -> Optional[Node[T]]: 
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(start, None, 0.0, heuristic(start)))
    explored: Dict[T: float] = {start: 0.0}

    while not frontier.empty:
        current_node = frontier.pop()
        if goal_test(current_node.state):
            return current_node
        for child in successors(current_node.state):
            new_cost = current_node.cost + 1
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))

    return None            


def node_to_path(final_node: Node[T]) -> List[T]:
    path: List[T] = []
    temp_node = final_node
    while temp_node.parent != None:
        path.append(temp_node.state)
        temp_node = temp_node.parent

    # adding start node
    path.append(temp_node.state)
    
    path.reverse()
    return path


if __name__ == "__main__":
    print(linear_search([1, 2, 3, 4, 5], 3))
    print(binary_search([1, 2, 3, 4, 5], 3))
    print(binary_search(['a', 'b', 'c', 'd', 'e'], 't'))