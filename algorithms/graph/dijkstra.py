import heapq
from .solver import GraphSolver
from typing import Iterator, List, Tuple, Optional

class Dijkstra(GraphSolver):
    def run(self) -> Iterator[Tuple[str, int, int, List[int], List[int], Optional[Tuple[int,int]], int]]:
        # Проверка на отрицательные веса рёбер
        negative_edges = []
        for u in self.graph:
            for v, w in self.graph[u]:
                if w < 0:
                    negative_edges.append((u, v, w))
        if negative_edges:
            msg = f"Ошибка: алгоритм Дейкстры не работает с отрицательными весами. Обнаружены рёбра: {negative_edges}"
            yield msg, -1, -1, [], [], None, -1
            return

        INF = 10**9
        dist = [INF] * self.n
        prev = [-1] * self.n
        dist[self.source] = 0
        pq = [(0, self.source)]
        visited = [False] * self.n
        yield f"Начало Дейкстры из {self.source}", self.source, 0, dist[:], [], None, 1
        while pq:
            if self.stopped: break
            d, u = heapq.heappop(pq)
            if visited[u]:
                continue
            visited[u] = True
            yield f"Выбрана вершина {u}, расстояние {d}", u, d, dist[:], [], None, 3
            if u == self.target: break
            for v, w in self.graph.get(u, []):
                if self.stopped: break
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
                    yield f"Релаксация {u}→{v}, новое расстояние {dist[v]}", v, dist[v], dist[:], [], (u, v), 6
        path = []
        cur = self.target
        while cur != -1:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        yield f"Путь: {' → '.join(map(str, path))}, длина = {dist[self.target]}", -1, dist[self.target], dist[:], path, None, 10
