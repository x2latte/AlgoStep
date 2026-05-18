from .solver import SortingSolver
from typing import Iterator, List, Tuple

class MergeSort(SortingSolver):
    def run(self) -> Iterator[Tuple[List[int], str, int, int]]:
        arr = self.arr[:]
        n = len(arr)
        yield arr, "Начало сортировки слиянием", -1, -1

        def _merge(l, m, r):
            left = arr[l:m+1]
            right = arr[m+1:r+1]
            i = j = 0
            k = l
            while i < len(left) and j < len(right):
                if self.stopped: return
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                yield arr, f"Слияние: выбор элемента из левого/правого подмассива", k, -1
                k += 1
            while i < len(left):
                arr[k] = left[i]
                yield arr, f"Слияние: остаток левой части", k, -1
                i += 1; k += 1
            while j < len(right):
                arr[k] = right[j]
                yield arr, f"Слияние: остаток правой части", k, -1
                j += 1; k += 1

        def _merge_sort(l, r):
            if self.stopped or l >= r: return
            m = (l+r)//2
            yield from _merge_sort(l, m)
            yield from _merge_sort(m+1, r)
            yield from _merge(l, m, r)

        yield from _merge_sort(0, n-1)
        yield arr, "Сортировка завершена", -1, -1
