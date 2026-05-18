from .solver import KnapsackSolver
from typing import Iterator, List, Tuple

class GreedyKnapsack(KnapsackSolver):
    def run(self) -> Iterator[Tuple[str, List[bool], int, int, int]]:
        n = len(self.items)
        indices = list(range(n))
        indices.sort(key=lambda i: self.items[i].value / self.items[i].weight, reverse=True)
        taken = [False] * n
        weight = 0
        value = 0
        yield "Начало жадного алгоритма", taken[:], value, self.capacity - weight, 1
        for idx in indices:
            if self.stopped: break
            item = self.items[idx]
            yield f"Рассматриваем {item.name} (вес {item.weight}, ценность {item.value})", taken[:], value, self.capacity - weight, 4
            if weight + item.weight <= self.capacity:
                taken[idx] = True
                weight += item.weight
                value += item.value
                yield f"Предмет {item.name} добавлен, вес={weight}, ценность={value}", taken[:], value, self.capacity - weight, 6
            else:
                yield f"Предмет {item.name} не помещается", taken[:], value, self.capacity - weight, 5
        yield f"Жадный алгоритм завершён. Итоговая ценность = {value}", taken[:], value, self.capacity - weight, 10
