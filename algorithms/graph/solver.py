from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Iterator, Optional

class GraphSolver(ABC):
    def __init__(self, graph: Dict[int, List[Tuple[int, int]]], source: int, target: int, n_vertices: int):
        self.graph = graph
        self.source = source
        self.target = target
        self.n = n_vertices
        self.stopped = False

    def stop(self):
        self.stopped = True

    @abstractmethod
    def run(self) -> Iterator[Tuple[str, int, int, List[int], List[int], Optional[Tuple[int,int]]]]:
        pass
