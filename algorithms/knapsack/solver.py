from abc import ABC, abstractmethod
from typing import List, Tuple, Iterator, NamedTuple

class Item(NamedTuple):
    name: str
    weight: int
    value: int

class KnapsackSolver(ABC):
    def __init__(self, items: List[Item], capacity: int):
        self.items = items
        self.capacity = capacity
        self.stopped = False

    def stop(self):
        self.stopped = True

    @abstractmethod
    def run(self) -> Iterator[Tuple[str, List[bool], int, int]]:
        pass
