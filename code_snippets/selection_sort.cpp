void selectionSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        // Находим индекс минимального элемента в неотсортированной части
        int min_idx = i;
        for (int j = i+1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        // Меняем найденный минимум с первым элементом
        if (min_idx != i) {
            swap(arr[i], arr[min_idx]);
        }
    }
}
