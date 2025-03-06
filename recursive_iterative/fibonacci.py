from functools import lru_cache 
from typing import Generator

@lru_cache(maxsize=None)
def cache_fib_n(n: int) -> int:
    if n < 2:
        return n
    
    return cache_fib_n(n - 1) + cache_fib_n(n - 2)
    

def iterative_fib_n(n: int) -> Generator[int, None, None]:
    yield 0

    if n > 1:
        yield 1
    
    last, next = 0, 1
    
    for _ in range(1, n):
        last, next = next, last + next
        yield next
    
    return 


if __name__ == "__main__":
    print(cache_fib_n(20))
    print(iterative_fib_n(20))