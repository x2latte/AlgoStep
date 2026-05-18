from .solver import KnapsackSolver
from typing import Iterator, List, Tuple

class BruteForceKnapsack(KnapsackSolver):
    def run(self) -> Iterator[Tuple[str, List[bool], int, int, int]]:
        n = len(self.items)
        best_value = 0
        best_taken = [False] * n
        yield "Начало полного перебора", best_taken, 0, self.capacity, 1
        for mask in range(1 << n):
            if self.stopped: break
            weight = 0
            value = 0
            taken = [False] * n
            for i in range(n):
                if mask >> i & 1:
                    weight += self.items[i].weight
                    value += self.items[i].value
                    taken[i] = True
            yield f"Проверка комбинации {mask:0{n}b}: вес {weight}, ценность {value}", taken, value, self.capacity - weight, 4
            if weight <= self.capacity and value > best_value:
                best_value = value
                best_taken = taken[:]
                yield f"Найдена новая лучшая комбинация! Ценность {best_value}", best_taken, best_value, self.capacity - weight, 5
        yield f"Полный перебор завершён. Оптимум = {best_value}", best_taken, best_value, self.capacity - sum(self.items[i].weight for i in range(n) if best_taken[i]), 8
