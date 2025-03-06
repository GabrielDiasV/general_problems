from typing import TypeVar, Generic, List
T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    # Overload __repr__ method to make it easier to debug using print
    def __repr__(self) -> str:
        return repr(self._container)
    

class HanoiTower:

    def __init__(self, num_discs:int, num_pegs:int) -> None:
        self.num_discs = num_discs
        self.num_pegs = num_pegs
        self.pegs = [Stack() for _ in range(num_pegs)]
        for i in range(1, num_discs + 1):
            self.pegs[0].push(i)

    def hanoi(self, begin: Stack[int], end: Stack[int], temp: Stack[int], num_discs: int) -> None:
        if num_discs == 1:
            end.push(begin.pop())
        else:
            self.hanoi(begin, temp, end, num_discs - 1)
            self.hanoi(begin, end, temp, 1)
            self.hanoi(temp, end, begin, num_discs - 1)

    def __repr__(self) -> str:
        return repr(self.pegs)


if __name__ == "__main__":
    num_discs: int = 3
    num_pegs: int = 3
    hanoi_tower = HanoiTower(num_discs, num_pegs)
    print(hanoi_tower)
    hanoi_tower.hanoi(hanoi_tower.pegs[0], hanoi_tower.pegs[2], hanoi_tower.pegs[1], num_discs)
    print(hanoi_tower)
