from typing import List, Callable

class SortingSolver:
    def __init__(self, arr: List[int]):
        self.arr = arr[:]
        self.n = len(arr)
        self.stopped = False

    def stop(self):
        self.stopped = True

    def bubble_sort(self, step_callback: Callable):
        arr = self.arr[:]
        n = self.n
        step_callback(arr, "Начало bubbleSort", -1, -1)
        for i in range(n-1):
            if self.stopped: break
            for j in range(n-1-i):
                if self.stopped: break
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    step_callback(arr, f"Пузырёк: обмен {j}↔{j+1}", j, j+1)
                else:
                    step_callback(arr, f"Пузырёк: сравнение {j} и {j+1} (без обмена)", j, j+1)
        step_callback(arr, "Пузырьковая сортировка завершена", -1, -1)

    def selection_sort(self, step_callback: Callable):
        arr = self.arr[:]
        n = self.n
        step_callback(arr, "Начало selectionSort", -1, -1)
        for i in range(n-1):
            if self.stopped: break
            min_idx = i
            for j in range(i+1, n):
                if self.stopped: break
                if arr[j] < arr[min_idx]:
                    min_idx = j
                step_callback(arr, f"Выбором: ищем минимум, текущий кандидат {j}", j, min_idx)
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                step_callback(arr, f"Выбором: обмен {i}↔{min_idx}", i, min_idx)
        step_callback(arr, "Сортировка выбором завершена", -1, -1)

    def insertion_sort(self, step_callback: Callable):
        arr = self.arr[:]
        n = self.n
        step_callback(arr, "Начало insertionSort", -1, -1)
        for i in range(1, n):
            if self.stopped: break
            key = arr[i]
            j = i-1
            while j >= 0 and arr[j] > key:
                if self.stopped: break
                arr[j+1] = arr[j]
                step_callback(arr, f"Вставками: сдвиг {j} вправо", j, j+1)
                j -= 1
            arr[j+1] = key
            step_callback(arr, f"Вставками: вставка {key} на позицию {j+1}", j+1, -1)
        step_callback(arr, "Сортировка вставками завершена", -1, -1)

    def quick_sort(self, step_callback: Callable):
        arr = self.arr[:]
        def _quick(l, r):
            if self.stopped or l >= r: return
            pivot = arr[(l+r)//2]
            i, j = l, r
            step_callback(arr, f"Быстрая: опорный {pivot} (l={l}, r={r})", -1, -1)
            while i <= j:
                while arr[i] < pivot: i += 1
                while arr[j] > pivot: j -= 1
                if i <= j:
                    arr[i], arr[j] = arr[j], arr[i]
                    step_callback(arr, f"Быстрая: обмен {i}↔{j}", i, j)
                    i += 1
                    j -= 1
            if l < j: _quick(l, j)
            if i < r: _quick(i, r)
        _quick(0, len(arr)-1)
        step_callback(arr, "Быстрая сортировка завершена", -1, -1)

    def merge_sort(self, step_callback: Callable):
        arr = self.arr[:]
        def _merge(l, m, r):
            left = arr[l:m+1]
            right = arr[m+1:r+1]
            i=j=0
            k=l
            step_callback(arr, f"Слияние: отрезки [{l},{m}] и [{m+1},{r}]", -1, -1)
            while i < len(left) and j < len(right):
                if self.stopped: return
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i+=1
                else:
                    arr[k] = right[j]
                    j+=1
                step_callback(arr, f"Слияние: выбор элемента", k, -1)
                k+=1
            while i < len(left):
                arr[k] = left[i]
                step_callback(arr, "Слияние: остаток левой", k, -1)
                i+=1; k+=1
            while j < len(right):
                arr[k] = right[j]
                step_callback(arr, "Слияние: остаток правой", k, -1)
                j+=1; k+=1
        def _merge_sort(l, r):
            if self.stopped or l>=r: return
            m = (l+r)//2
            _merge_sort(l, m)
            _merge_sort(m+1, r)
            _merge(l, m, r)
        step_callback(arr, "Начало mergeSort", -1, -1)
        _merge_sort(0, len(arr)-1)
        step_callback(arr, "Сортировка слиянием завершена", -1, -1)

    def counting_sort(self, step_callback: Callable):
        arr = self.arr[:]
        if not arr:
            step_callback([], "Массив пуст", -1, -1)
            return
        max_val = max(arr)
        min_val = min(arr)
        range_size = max_val - min_val + 1
        count = [0]*range_size
        output = [0]*len(arr)
        step_callback(arr, f"Подсчёт: диапазон {min_val}..{max_val}", -1, -1)
        for v in arr:
            if self.stopped: return
            count[v-min_val] += 1
        for i in range(1, len(count)):
            if self.stopped: return
            count[i] += count[i-1]
        for v in reversed(arr):
            if self.stopped: return
            output[count[v-min_val]-1] = v
            count[v-min_val] -= 1
            step_callback(output, "Подсчёт: размещаем", -1, -1)
        step_callback(output, "Сортировка подсчётом завершена", -1, -1)
