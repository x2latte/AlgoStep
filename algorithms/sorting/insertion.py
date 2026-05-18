from .solver import SortingSolver
from typing import Iterator, List, Tuple

class InsertionSort(SortingSolver):
    def run(self) -> Iterator[Tuple[List[int], str, int, int]]:
        arr = self.arr[:]
        n = len(arr)
        yield arr, "Начало сортировки вставками", -1, -1
        for i in range(1, n):
            if self.stopped: break
            key = arr[i]
            j = i-1
            yield arr, f"Вставляем элемент {key}", i, -1
            while j >= 0 and arr[j] > key:
                if self.stopped: break
                arr[j+1] = arr[j]
                yield arr, f"Сдвиг элемента {arr[j]} вправо", j, j+1
                j -= 1
            arr[j+1] = key
            yield arr, f"Элемент {key} вставлен на позицию {j+1}", j+1, -1
        yield arr, "Сортировка завершена", -1, -1
