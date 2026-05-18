void branchAndBound(int idx, int weight, int value, int &bestValue, Item items[], int n, int capacity) {
    if (weight > capacity) return;
    if (idx == n) {
        if (value > bestValue) bestValue = value;
        return;
    }
    int bound = value;
    int remaining = capacity - weight;
    for (int i = idx; i < n; i++) {
        if (items[i].weight <= remaining) {
            bound += items[i].value;
            remaining -= items[i].weight;
        } else {
            bound += (items[i].value * remaining) / items[i].weight;
            break;
        }
    }
    if (bound <= bestValue) return;
    branchAndBound(idx+1, weight, value, bestValue, items, n, capacity);
    branchAndBound(idx+1, weight + items[idx].weight, value + items[idx].value, bestValue, items, n, capacity);
}
