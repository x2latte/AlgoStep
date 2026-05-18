from .solver import KnapsackSolver
from typing import Iterator, List, Tuple

class BranchAndBoundKnapsack(KnapsackSolver):
    def run(self) -> Iterator[Tuple[str, List[bool], int, int, int]]:
        n = len(self.items)
        # сортируем
        items_with_idx = sorted([(i, self.items[i]) for i in range(n)], key=lambda x: x[1].value / x[1].weight, reverse=True)
        sorted_idx = [p[0] for p in items_with_idx]
        sorted_items = [self.items[i] for i in sorted_idx]
        best_value = 0
        best_taken = [False] * n
        yield "Начало ветвей и границ", best_taken, 0, self.capacity, 1

        def bound(idx, weight, value):
            if weight >= self.capacity:
                return value
            bound_val = value
            remain = self.capacity - weight
            for j in range(idx, n):
                if sorted_items[j].weight <= remain:
                    bound_val += sorted_items[j].value
                    remain -= sorted_items[j].weight
                else:
                    bound_val += (sorted_items[j].value / sorted_items[j].weight) * remain
                    break
            return bound_val

        def dfs(idx, weight, value, taken):
            nonlocal best_value, best_taken
            if self.stopped:
                return
            if idx == n:
                if value > best_value:
                    best_value = value
                    best_taken = [False]*n
                    for i, t in enumerate(taken):
                        if t:
                            best_taken[sorted_idx[i]] = True
                    yield f"Новая лучшая ветка: ценность {best_value}", best_taken, best_value, self.capacity - weight, 8
                return
            # не брать
            if bound(idx+1, weight, value) > best_value:
                yield from dfs(idx+1, weight, value, taken + [False])
            # взять
            if weight + sorted_items[idx].weight <= self.capacity:
                new_taken = taken + [True]
                new_weight = weight + sorted_items[idx].weight
                new_value = value + sorted_items[idx].value
                yield f"Берём {sorted_items[idx].name}, ценность={new_value}", [False]*n, new_value, self.capacity - new_weight, 6
                yield from dfs(idx+1, new_weight, new_value, new_taken)

        yield from dfs(0, 0, 0, [])
        yield f"Ветви и границы завершены. Оптимум = {best_value}", best_taken, best_value, self.capacity - sum(self.items[i].weight for i in range(n) if best_taken[i]), 12
