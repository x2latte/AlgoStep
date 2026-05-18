from .solver import SortingSolver
from typing import Iterator, List, Tuple

class SelectionSort(SortingSolver):
    def run(self) -> Iterator[Tuple[List[int], str, int, int]]:
        arr = self.arr[:]
        n = len(arr)
        yield arr, "Начало сортировки выбором", -1, -1
        for i in range(n-1):
            if self.stopped: break
            min_idx = i
            for j in range(i+1, n):
                if self.stopped: break
                yield arr, f"Поиск минимума: сравнение {arr[j]} и {arr[min_idx]}", j, min_idx
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                yield arr, f"Обмен элементов {arr[i]} и {arr[min_idx]}", i, min_idx
        yield arr, "Сортировка завершена", -1, -1
