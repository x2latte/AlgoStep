from .solver import SortingSolver
from typing import Iterator, List, Tuple

class CountingSort(SortingSolver):
    def run(self) -> Iterator[Tuple[List[int], str, int, int]]:
        arr = self.arr[:]
        if not arr:
            yield [], "Массив пуст", -1, -1
            return
        max_val = max(arr)
        min_val = min(arr)
        range_size = max_val - min_val + 1
        count = [0] * range_size
        output = [0] * len(arr)
        yield arr, f"Сортировка подсчётом, диапазон [{min_val}, {max_val}]", -1, -1
        for v in arr:
            count[v - min_val] += 1
            yield output, f"Подсчёт частоты для {v}", -1, -1
        for i in range(1, len(count)):
            count[i] += count[i-1]
            yield output, f"Префиксная сумма count[{i}] = {count[i]}", -1, -1
        for v in reversed(arr):
            output[count[v - min_val] - 1] = v
            count[v - min_val] -= 1
            yield output, f"Размещение {v} в выходной массив", -1, -1
        arr[:] = output
        yield arr, "Сортировка завершена", -1, -1
