from .solver import GraphSolver
from typing import Iterator, List, Tuple, Optional

class BruteForceGraph(GraphSolver):
    def run(self) -> Iterator[Tuple[str, int, int, List[int], List[int], Optional[Tuple[int,int]]]]:
        INF = 10**9
        self.best_dist = INF
        self.best_path = []
        visited = [False] * self.n
        cur_path = []

        def dfs(v, cur_dist):
            if self.stopped: return
            visited[v] = True
            cur_path.append(v)
            yield f"Посещаем вершину {v}, текущий путь: {cur_path}, расстояние = {cur_dist}", v, cur_dist, [], cur_path[:], None
            if v == self.target:
                if cur_dist < self.best_dist:
                    self.best_dist = cur_dist
                    self.best_path = cur_path[:]
                    yield f"Найден новый лучший путь: {self.best_path}, длина = {self.best_dist}", v, cur_dist, [], self.best_path, None
            else:
                for to, w in self.graph.get(v, []):
                    if not visited[to]:
                        yield from dfs(to, cur_dist + w)
            visited[v] = False
            cur_path.pop()

        yield from dfs(self.source, 0)
        yield f"Поиск завершён. Кратчайший путь: {self.best_path}, длина = {self.best_dist}", -1, self.best_dist, [], self.best_path, None
