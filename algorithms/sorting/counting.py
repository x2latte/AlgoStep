from .solver import SortingSolver
from typing import Iterator, List, Tuple

class CountingSort(SortingSolver):
    def run(self) -> Iterator[Tuple[List[int], str, int, int, int]]:
        arr = self.arr[:]
        if not arr:
            yield [], "Массив пуст", -1, -1, 1
            return
        max_val = max(arr)
        min_val = min(arr)
        range_size = max_val - min_val + 1
        count = [0] * range_size
        output = [0] * len(arr)
        yield arr, f"Сортировка подсчётом, диапазон [{min_val}, {max_val}]", -1, -1, 1
        # Подсчёт частот
        for v in arr:
            if self.stopped: break
            count[v - min_val] += 1
        yield arr, "Гистограмма частот построена", -1, -1, 2
        # Префиксные суммы (без вывода каждой итерации)
        for i in range(1, len(count)):
            if self.stopped: break
            count[i] += count[i-1]
        yield arr, "Префиксные суммы вычислены", -1, -1, 3
        # Размещение
        for v in reversed(arr):
            if self.stopped: break
            output[count[v - min_val] - 1] = v
            count[v - min_val] -= 1
            yield output, f"Размещение {v} в выходной массив", -1, -1, 4
        yield output, "Сортировка завершена", -1, -1, 5
