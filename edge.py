from __future__ import annotations
from dataclasses import dataclass 

# dataclass automatically creates a __init__ method, __repr__ method, __eq__ method, __ne__ method, and __hash__ method
# with parameters as the attributes defined and typed
@dataclass
class Edge:
    u: int # from vertex
    v: int # to vertex

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)
    
    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"
    

