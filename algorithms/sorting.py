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
        step_callback(arr, "Начало bubbleSort", 1, -1, -1)
        for i in range(n-1):
            if self.stopped: break
            step_callback(arr, f"Внешний цикл i={i}", 2, -1, -1)
            for j in range(n-1-i):
                if self.stopped: break
                step_callback(arr, f"Сравнение j={j}", 3, j, j+1)
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    step_callback(arr, f"Обмен {j}↔{j+1}", 4, j, j+1)
                else:
                    step_callback(arr, f"Без обмена {j}↔{j+1}", 5, j, j+1)
        step_callback(arr, "Конец bubbleSort", 6, -1, -1)

    def selection_sort(self, step_callback: Callable):
        arr = self.arr[:]
        n = self.n
        step_callback(arr, "Начало selectionSort", 1, -1, -1)
        for i in range(n-1):
            if self.stopped: break
            min_idx = i
            step_callback(arr, f"Внешний цикл i={i}, min_idx={min_idx}", 2, i, -1)
            for j in range(i+1, n):
                if self.stopped: break
                step_callback(arr, f"Поиск минимума j={j}, текущий min_idx={min_idx}", 3, j, min_idx)
                if arr[j] < arr[min_idx]:
                    min_idx = j
                    step_callback(arr, f"Новый минимум min_idx={min_idx}", 4, j, min_idx)
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                step_callback(arr, f"Обмен {i}↔{min_idx}", 5, i, min_idx)
        step_callback(arr, "Конец selectionSort", 6, -1, -1)

    def insertion_sort(self, step_callback: Callable):
        arr = self.arr[:]
        n = self.n
        step_callback(arr, "Начало insertionSort", 1, -1, -1)
        for i in range(1, n):
            if self.stopped: break
            key = arr[i]
            j = i-1
            step_callback(arr, f"Внешний цикл i={i}, key={key}", 2, i, -1)
            while j >= 0 and arr[j] > key:
                if self.stopped: break
                arr[j+1] = arr[j]
                step_callback(arr, f"Сдвиг j={j} вправо", 3, j, j+1)
                j -= 1
            arr[j+1] = key
            step_callback(arr, f"Вставка key={key} на позицию {j+1}", 4, j+1, -1)
        step_callback(arr, "Конец insertionSort", 5, -1, -1)

    def quick_sort(self, step_callback: Callable):
        arr = self.arr[:]
        def _quick(l, r):
            if self.stopped or l >= r: return
            pivot = arr[(l+r)//2]
            i, j = l, r
            step_callback(arr, f"Разделение l={l}, r={r}, pivot={pivot}", 1, -1, -1)
            while i <= j:
                while arr[i] < pivot:
                    i += 1
                while arr[j] > pivot:
                    j -= 1
                if i <= j:
                    arr[i], arr[j] = arr[j], arr[i]
                    step_callback(arr, f"Обмен {i}↔{j}", 2, i, j)
                    i += 1
                    j -= 1
            if l < j: _quick(l, j)
            if i < r: _quick(i, r)
        _quick(0, len(arr)-1)
        step_callback(arr, "Конец quickSort", 3, -1, -1)

    def merge_sort(self, step_callback: Callable):
        arr = self.arr[:]
        def _merge(l, m, r):
            left = arr[l:m+1]
            right = arr[m+1:r+1]
            i = j = 0
            k = l
            step_callback(arr, f"Слияние l={l}, m={m}, r={r}", 1, -1, -1)
            while i < len(left) and j < len(right):
                if self.stopped: return
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                step_callback(arr, f"Выбор элемента на позицию k={k}", 2, k, -1)
                k += 1
            while i < len(left):
                arr[k] = left[i]
                step_callback(arr, f"Остаток левой части k={k}", 3, k, -1)
                i += 1; k += 1
            while j < len(right):
                arr[k] = right[j]
                step_callback(arr, f"Остаток правой части k={k}", 3, k, -1)
                j += 1; k += 1
        def _merge_sort(l, r):
            if self.stopped or l >= r: return
            m = (l+r)//2
            _merge_sort(l, m)
            _merge_sort(m+1, r)
            _merge(l, m, r)
        step_callback(arr, "Начало mergeSort", 4, -1, -1)
        _merge_sort(0, len(arr)-1)
        step_callback(arr, "Конец mergeSort", 5, -1, -1)

    def heap_sort(self, step_callback: Callable):
        arr = self.arr[:]
        n = len(arr)

        def heapify(n, i):
            largest = i
            l = 2*i + 1
            r = 2*i + 2
            if l < n and arr[l] > arr[largest]:
                largest = l
            if r < n and arr[r] > arr[largest]:
                largest = r
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                step_callback(arr, f"Heapify просеивание i={i}", 1, i, largest)
                heapify(n, largest)

        step_callback(arr, "Начало heapSort", 2, -1, -1)
        for i in range(n//2-1, -1, -1):
            if self.stopped: return
            heapify(n, i)
            step_callback(arr, f"Построение кучи i={i}", 3, -1, -1)
        for i in range(n-1, 0, -1):
            if self.stopped: return
            arr[i], arr[0] = arr[0], arr[i]
            step_callback(arr, f"Обмен 0↔{i}", 4, 0, i)
            heapify(i, 0)
        step_callback(arr, "Конец heapSort", 5, -1, -1)

    def counting_sort(self, step_callback: Callable):
        arr = self.arr[:]
        if not arr:
            step_callback([], "Массив пуст", -1, -1, -1)
            return
        max_val = max(arr)
        min_val = min(arr)
        range_size = max_val - min_val + 1
        count = [0] * range_size
        output = [0] * len(arr)
        step_callback(arr, f"Подсчёт: диапазон {min_val}..{max_val}", 1, -1, -1)
        for v in arr:
            if self.stopped: return
            count[v - min_val] += 1
            step_callback(arr, f"Гистограмма: count[{v-min_val}]={count[v-min_val]}", 2, -1, -1)
        for i in range(1, len(count)):
            count[i] += count[i-1]
            step_callback(arr, f"Префиксные суммы: count[{i}]={count[i]}", 3, -1, -1)
        for v in reversed(arr):
            if self.stopped: return
            output[count[v - min_val] - 1] = v
            count[v - min_val] -= 1
            step_callback(output.copy(), f"Размещение {v}", 4, -1, -1)
        step_callback(output, "Конец countingSort", 5, -1, -1)
