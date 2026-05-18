void countingSort(int arr[], int n) {
    int max_val = *max_element(arr, arr+n);
    int min_val = *min_element(arr, arr+n);
    int range = max_val - min_val + 1;
    vector<int> count(range), output(n);
    for (int i=0; i<n; i++) count[arr[i]-min_val]++;
    for (int i=1; i<range; i++) count[i] += count[i-1];
    for (int i=n-1; i>=0; i--) {
        output[count[arr[i]-min_val]-1] = arr[i];
        count[arr[i]-min_val]--;
    }
    for (int i=0; i<n; i++) arr[i] = output[i];
}
