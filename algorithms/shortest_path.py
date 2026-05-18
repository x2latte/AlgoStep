from typing import Dict, List, Tuple, Callable
from collections import defaultdict
import heapq

class ShortestPathSolver:
    def __init__(self, graph: Dict[int, List[Tuple[int,int]]], source: int, target: int, n_vertices: int):
        self.graph = graph
        self.source = source
        self.target = target
        self.n = n_vertices
        self.stopped = False

    def stop(self):
        self.stopped = True

    def dijkstra(self, step_callback: Callable) -> Tuple[int, List[int]]:
        INF = 10**9
        dist = [INF]*self.n
        prev = [-1]*self.n
        visited = [False]*self.n
        dist[self.source] = 0
        for _ in range(self.n):
            if self.stopped: break
            u = -1
            best = INF
            for i in range(self.n):
                if not visited[i] and dist[i] < best:
                    best = dist[i]
                    u = i
            if u == -1 or u == self.target:
                break
            visited[u] = True
            step_callback(f"Выбрана вершина {u} (расстояние {dist[u]})", u, dist[u], dist, visited, [], None)
            for v,w in self.graph.get(u, []):
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    step_callback(f"Релаксация {u}→{v}: теперь {dist[v]}", v, dist[v], dist, visited, [], (u,v))
        path = []
        cur = self.target
        while cur != -1:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        step_callback(f"✅ Кратчайшее расстояние = {dist[self.target]}", -1, dist[self.target], dist, visited, path, None)
        return dist[self.target], path

    def heuristic(self, a: int, b: int) -> int:
        return 0

    def a_star(self, step_callback: Callable) -> Tuple[int, List[int]]:
        INF = 10**9
        g_score = [INF]*self.n
        f_score = [INF]*self.n
        prev = [-1]*self.n
        g_score[self.source] = 0
        f_score[self.source] = self.heuristic(self.source, self.target)
        open_set = [(f_score[self.source], self.source)]
        closed = [False]*self.n
        while open_set:
            if self.stopped: break
            _, current = heapq.heappop(open_set)
            if closed[current]:
                continue
            closed[current] = True
            step_callback(f"A*: обрабатываем вершину {current}, f={f_score[current]}", current, g_score[current], g_score, closed, [], None)
            if current == self.target:
                break
            for neighbor, w in self.graph.get(current, []):
                tentative_g = g_score[current] + w
                if tentative_g < g_score[neighbor]:
                    prev[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, self.target)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    step_callback(f"A*: улучшен путь до {neighbor}, g={g_score[neighbor]}", neighbor, g_score[neighbor], g_score, closed, [], (current, neighbor))
        path = []
        cur = self.target
        while cur != -1:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        step_callback(f"✅ A* завершён. Расстояние = {g_score[self.target]}", -1, g_score[self.target], g_score, closed, path, None)
        return g_score[self.target], path

    def brute_force(self, step_callback: Callable) -> Tuple[int, List[int]]:
        INF = 10**9
        best_dist = INF
        best_path = []
        visited = [False]*self.n
        cur_path = []
        def dfs(v, cur_dist):
            nonlocal best_dist, best_path
            if self.stopped:
                return
            visited[v] = True
            cur_path.append(v)
            step_callback(f"Посещаем {v}, длина пути {cur_dist}", v, cur_dist, [], visited, cur_path, None)
            if v == self.target:
                if cur_dist < best_dist:
                    best_dist = cur_dist
                    best_path = cur_path.copy()
                    step_callback(f"★ НОВЫЙ ЛУЧШИЙ ПУТЬ: {best_dist}", v, cur_dist, [], visited, best_path, None)
            else:
                for to,w in self.graph.get(v, []):
                    if not visited[to]:
                        dfs(to, cur_dist + w)
            visited[v] = False
            cur_path.pop()
        dfs(self.source, 0)
        step_callback(f"✅ Перебор закончен, лучший путь = {best_dist}", -1, best_dist, [], visited, best_path, None)
        return best_dist, best_path

    def bellman_ford(self, step_callback: Callable) -> Tuple[int, List[int]]:
        INF = 10**9
        dist = [INF]*self.n
        prev = [-1]*self.n
        dist[self.source] = 0
        edges = [(u,v,w) for u in self.graph for v,w in self.graph[u]]
        for i in range(self.n-1):
            updated = False
            for u,v,w in edges:
                if self.stopped: break
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True
                    step_callback(f"Итер {i+1}: улучшаем {v} до {dist[v]}", v, dist[v], dist, [], [], (u,v))
            if not updated:
                break
        path = []
        cur = self.target
        while cur != -1:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        step_callback(f"✅ Беллман-Форд: расстояние {dist[self.target]}", -1, dist[self.target], dist, [], path, None)
        return dist[self.target], path

    def floyd_warshall(self, step_callback: Callable) -> Tuple[int, List[int]]:
        INF = 10**9
        dist = [[INF]*self.n for _ in range(self.n)]
        next_vertex = [[-1]*self.n for _ in range(self.n)]
        for i in range(self.n):
            dist[i][i] = 0
        for u in self.graph:
            for v,w in self.graph[u]:
                dist[u][v] = w
                next_vertex[u][v] = v
        for k in range(self.n):
            if self.stopped: break
            for i in range(self.n):
                for j in range(self.n):
                    if dist[i][k] != INF and dist[k][j] != INF and dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertex[i][j] = next_vertex[i][k]
            step_callback(f"Флойд-Уоршелл: итерация {k+1}/{self.n}", -1, -1, dist, [], [], None)
        path = []
        if dist[self.source][self.target] != INF:
            cur = self.source
            while cur != self.target:
                path.append(cur)
                cur = next_vertex[cur][self.target]
                if cur == -1: break
            path.append(self.target)
        step_callback(f"✅ Флойд-Уоршелл: расстояние = {dist[self.source][self.target]}", -1, dist[self.source][self.target], dist, [], path, None)
        return dist[self.source][self.target], path
