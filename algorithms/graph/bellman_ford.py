from .solver import GraphSolver
from typing import Iterator, List, Tuple, Optional

class BellmanFord(GraphSolver):
    def run(self) -> Iterator[Tuple[str, int, int, List[int], List[int], Optional[Tuple[int,int]]]]:
        INF = 10**9
        dist = [INF] * self.n
        prev = [-1] * self.n
        dist[self.source] = 0
        edges = []
        for u in self.graph:
            for v, w in self.graph[u]:
                edges.append((u, v, w))
        yield f"Начало алгоритма Беллмана-Форда из вершины {self.source}", self.source, 0, dist[:], [], None
        for i in range(self.n-1):
            if self.stopped: break
            updated = False
            for u, v, w in edges:
                if self.stopped: break
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True
                    yield f"Итерация {i+1}: улучшаем расстояние до {v} = {dist[v]}", v, dist[v], dist[:], [], (u, v)
            if not updated:
                break
        path = []
        cur = self.target
        while cur != -1:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        yield f"Путь найден: {' → '.join(map(str, path))}, длина = {dist[self.target]}", -1, dist[self.target], dist[:], path, None
