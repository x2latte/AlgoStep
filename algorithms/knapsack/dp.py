from .solver import KnapsackSolver
from typing import Iterator, List, Tuple

class DPKnapsack(KnapsackSolver):
    def run(self) -> Iterator[Tuple[str, List[bool], int, int, int]]:
        n = len(self.items)
        cap = self.capacity
        dp = [[0]*(cap+1) for _ in range(n+1)]
        yield f"Начало DP, таблица {n}x{cap}", [], 0, cap, 1
        for i in range(1, n+1):
            for w in range(cap+1):
                if self.stopped: break
                if self.items[i-1].weight <= w:
                    dp[i][w] = max(dp[i-1][w], dp[i-1][w - self.items[i-1].weight] + self.items[i-1].value)
                else:
                    dp[i][w] = dp[i-1][w]
                if w % max(1, cap//10) == 0 or w == cap:
                    yield f"DP: заполнена ячейка [{i}][{w}] = {dp[i][w]}", [], dp[i][w], cap - w, 4
        taken = [False] * n
        w = cap
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                taken[i-1] = True
                w -= self.items[i-1].weight
        yield f"DP завершён. Оптимальная ценность = {dp[n][cap]}", taken, dp[n][cap], w, 10
