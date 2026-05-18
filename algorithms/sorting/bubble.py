from .solver import SortingSolver
from typing import Iterator, List, Tuple

class BubbleSort(SortingSolver):
    def run(self) -> Iterator[Tuple[List[int], str, int, int, int]]:
        arr = self.arr[:]
        n = len(arr)
        # Номера строк из bubble_sort.cpp:
        # 1: void bubbleSort(int arr[], int n) {
        # 2:     for (int i = 0; i < n-1; i++) {
        # 3:         for (int j = 0; j < n-i-1; j++) {
        # 4:             if (arr[j] > arr[j+1]) {
        # 5:                 swap(arr[j], arr[j+1]);
        # 6:             }
        # 7:         }
        # 8:     }
        # 9: }
        yield arr, "Начало пузырьковой сортировки", -1, -1, 1
        for i in range(n-1):
            if self.stopped: break
            yield arr, f"Внешний цикл i={i}", -1, -1, 2
            for j in range(n-1-i):
                if self.stopped: break
                yield arr, f"Сравнение {arr[j]} и {arr[j+1]}", j, j+1, 3
                if arr[j] > arr[j+1]:
                    yield arr, f"Обмен {arr[j]} и {arr[j+1]}", j, j+1, 4  # строка условия if (перед обменом)
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    yield arr, f"Обмен выполнен: swap", j, j+1, 5  # строка swap
                else:
                    yield arr, f"Без обмена", j, j+1, 4  # строка условия if
        yield arr, "Сортировка завершена", -1, -1, 9
