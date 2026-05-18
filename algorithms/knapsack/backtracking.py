from .solver import KnapsackSolver
from typing import Iterator, List, Tuple

class BacktrackingKnapsack(KnapsackSolver):
    def run(self) -> Iterator[Tuple[str, List[bool], int, int, int]]:
        n = len(self.items)
        best_value = 0
        best_taken = [False] * n
        current_taken = [False] * n
        yield "Начало backtracking", best_taken, 0, self.capacity, 1

        def backtrack(i, weight, value):
            nonlocal best_value, best_taken
            if self.stopped:
                return
            if i == n:
                if value > best_value:
                    best_value = value
                    best_taken = current_taken[:]
                    yield f"Найдено новое решение: ценность {best_value}", best_taken, best_value, self.capacity - weight, 3
                return
            # Не брать
            yield from backtrack(i+1, weight, value)
            # Взять
            if weight + self.items[i].weight <= self.capacity:
                current_taken[i] = True
                yield f"Берём {self.items[i].name}", current_taken, value + self.items[i].value, self.capacity - (weight + self.items[i].weight), 5
                yield from backtrack(i+1, weight + self.items[i].weight, value + self.items[i].value)
                current_taken[i] = False

        yield from backtrack(0, 0, 0)
        yield f"Backtracking завершён. Оптимум = {best_value}", best_taken, best_value, self.capacity - sum(self.items[i].weight for i in range(n) if best_taken[i]), 7
