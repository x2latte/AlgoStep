from .solver import SortingSolver
from typing import Iterator, List, Tuple

class BubbleSort(SortingSolver):
    def run(self) -> Iterator[Tuple[List[int], str, int, int]]:
        arr = self.arr[:]
        n = len(arr)
        yield arr, "Начало пузырьковой сортировки", -1, -1
        for i in range(n-1):
            if self.stopped: break
            for j in range(n-1-i):
                if self.stopped: break
                yield arr, f"Сравнение элементов {arr[j]} и {arr[j+1]}", j, j+1
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    yield arr, f"Обмен элементов {arr[j]} и {arr[j+1]}", j, j+1
        yield arr, "Сортировка завершена", -1, -1
