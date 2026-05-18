from .solver import GraphSolver
from typing import Iterator, List, Tuple, Optional

class FloydWarshall(GraphSolver):
    def run(self) -> Iterator[Tuple[str, int, int, List[int], List[int], Optional[Tuple[int,int]]]]:
        INF = 10**9
        dist = [[INF] * self.n for _ in range(self.n)]
        nxt = [[-1] * self.n for _ in range(self.n)]
        for i in range(self.n):
            dist[i][i] = 0
        for u in self.graph:
            for v, w in self.graph[u]:
                dist[u][v] = w
                nxt[u][v] = v
        yield f"Начало алгоритма Флойда-Уоршелла, граф из {self.n} вершин", -1, -1, [], [], None
        for k in range(self.n):
            if self.stopped: break
            for i in range(self.n):
                for j in range(self.n):
                    if dist[i][k] != INF and dist[k][j] != INF and dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]
            yield f"Итерация {k+1}/{self.n} завершена", -1, -1, [], [], None
        if dist[self.source][self.target] == INF:
            yield f"Путь не существует", -1, -1, [], [], None
            return
        path = []
        cur = self.source
        while cur != self.target:
            path.append(cur)
            cur = nxt[cur][self.target]
        path.append(self.target)
        yield f"Путь найден: {' → '.join(map(str, path))}, длина = {dist[self.source][self.target]}", -1, dist[self.source][self.target], [], path, None
