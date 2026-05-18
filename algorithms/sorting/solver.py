from abc import ABC, abstractmethod
from typing import List, Iterator, Tuple

class SortingSolver(ABC):
    def __init__(self, arr: List[int]):
        self.arr = arr[:]
        self.stopped = False

    def stop(self):
        self.stopped = True

    @abstractmethod
    def run(self) -> Iterator[Tuple[List[int], str, int, int]]:
        pass
