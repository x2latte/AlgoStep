from .solver import SortingSolver
from typing import Iterator, List, Tuple

class QuickSort(SortingSolver):
    def run(self) -> Iterator[Tuple[List[int], str, int, int]]:
        arr = self.arr[:]
        n = len(arr)
        yield arr, "Начало быстрой сортировки", -1, -1

        def _quick(l, r):
            if self.stopped or l >= r: return
            pivot = arr[(l+r)//2]
            i, j = l, r
            yield arr, f"Выбран pivot = {pivot} (l={l}, r={r})", -1, -1
            while i <= j:
                while arr[i] < pivot: i += 1
                while arr[j] > pivot: j -= 1
                if i <= j:
                    arr[i], arr[j] = arr[j], arr[i]
                    yield arr, f"Обмен элементов {arr[i]} и {arr[j]}", i, j
                    i += 1
                    j -= 1
            if l < j: yield from _quick(l, j)
            if i < r: yield from _quick(i, r)

        yield from _quick(0, n-1)
        yield arr, "Сортировка завершена", -1, -1
