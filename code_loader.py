import os

class CodeLoader:
    @staticmethod
    def get_knapsack_code(algo):
        files = {
            "greedy": "knapsack_greedy.cpp",
            "brute": "knapsack_brute.cpp",
            "dp": "knapsack_dp.cpp",
            "bnb": "knapsack_bnb.cpp",
            "annealing": "knapsack_annealing.cpp"
        }
        if algo not in files:
            return "// Код будет добавлен"
        path = os.path.join("code_snippets", files[algo])
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return "// Ошибка загрузки кода"

    @staticmethod
    def get_graph_code(algo):
        files = {
            "dijkstra": "graph_dijkstra.cpp",
            "brute": "graph_brute.cpp",
            "bellman": "graph_bellman.cpp",
            "astar": "graph_astar.cpp",
            "floyd": "graph_floyd.cpp"
        }
        if algo not in files:
            return "// Код будет добавлен"
        path = os.path.join("code_snippets", files[algo])
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return "// Ошибка загрузки кода"

    @staticmethod
    def get_sort_code(algo):
        # Для сортировки пока оставим встроенные строки (можно позже вынести)
        codes = {
            "bubble": '''// Пузырьковая сортировка
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                swap(arr[j], arr[j+1]);
            }
        }
    }
}''',
            "selection": '''// Сортировка выбором
void selectionSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        int min_idx = i;
        for (int j = i+1; j < n; j++) {
            if (arr[j] < arr[min_idx]) min_idx = j;
        }
        if (min_idx != i) swap(arr[i], arr[min_idx]);
    }
}''',
            "insertion": '''// Сортировка вставками
void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i-1;
        while (j >= 0 && arr[j] > key) {
            arr[j+1] = arr[j];
            j--;
        }
        arr[j+1] = key;
    }
}''',
            "quick": '''// Быстрая сортировка
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low-1;
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) swap(arr[++i], arr[j]);
    }
    swap(arr[i+1], arr[high]);
    return i+1;
}
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi-1);
        quickSort(arr, pi+1, high);
    }
}''',
            "merge": '''// Сортировка слиянием
void merge(int arr[], int l, int m, int r) {
    int n1 = m-l+1, n2 = r-m;
    vector<int> L(n1), R(n2);
    for (int i=0;i<n1;i++) L[i]=arr[l+i];
    for (int j=0;j<n2;j++) R[j]=arr[m+1+j];
    int i=0,j=0,k=l;
    while (i<n1 && j<n2) arr[k++] = (L[i]<=R[j]) ? L[i++] : R[j++];
    while (i<n1) arr[k++]=L[i++];
    while (j<n2) arr[k++]=R[j++];
}
void mergeSort(int arr[], int l, int r) {
    if (l<r) {
        int m = l+(r-l)/2;
        mergeSort(arr,l,m);
        mergeSort(arr,m+1,r);
        merge(arr,l,m,r);
    }
}''',
            "counting": '''// Сортировка подсчётом
void countingSort(int arr[], int n) {
    int max_val = *max_element(arr, arr+n);
    int min_val = *min_element(arr, arr+n);
    int range = max_val - min_val + 1;
    vector<int> count(range), output(n);
    for (int i=0;i<n;i++) count[arr[i]-min_val]++;
    for (int i=1;i<range;i++) count[i] += count[i-1];
    for (int i=n-1;i>=0;i--) output[--count[arr[i]-min_val]] = arr[i];
    for (int i=0;i<n;i++) arr[i]=output[i];
}'''
        }
        return codes.get(algo, "// Код будет добавлен")
