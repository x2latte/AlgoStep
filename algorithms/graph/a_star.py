import heapq
from .solver import GraphSolver
from typing import Iterator, List, Tuple, Optional

class AStar(GraphSolver):
    def heuristic(self, a, b):
        return 0

    def run(self) -> Iterator[Tuple[str, int, int, List[int], List[int], Optional[Tuple[int,int]]]]:
        INF = 10**9
        g = [INF] * self.n
        f = [INF] * self.n
        prev = [-1] * self.n
        g[self.source] = 0
        f[self.source] = self.heuristic(self.source, self.target)
        open_set = [(f[self.source], self.source)]
        closed = [False] * self.n
        yield f"Начало A* из вершины {self.source}", self.source, 0, g[:], [], None
        while open_set:
            if self.stopped: break
            _, u = heapq.heappop(open_set)
            if closed[u]:
                continue
            closed[u] = True
            yield f"Обрабатываем вершину {u}, f = {f[u]}", u, g[u], g[:], [], None
            if u == self.target:
                break
            for v, w in self.graph.get(u, []):
                if self.stopped: break
                tentative_g = g[u] + w
                if tentative_g < g[v]:
                    prev[v] = u
                    g[v] = tentative_g
                    f[v] = g[v] + self.heuristic(v, self.target)
                    heapq.heappush(open_set, (f[v], v))
                    yield f"Улучшен путь до {v}, g = {g[v]}", v, g[v], g[:], [], (u, v)
        path = []
        cur = self.target
        while cur != -1:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        yield f"Путь найден: {' → '.join(map(str, path))}, длина = {g[self.target]}", -1, g[self.target], g[:], path, None
