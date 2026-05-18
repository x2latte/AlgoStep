void backtrack(int i, int weight, int value, int &bestValue, Item items[], int n, int capacity) {
    if (i == n) {
        if (value > bestValue) bestValue = value;
        return;
    }
    backtrack(i+1, weight, value, bestValue, items, n, capacity);
    if (weight + items[i].weight <= capacity) {
        backtrack(i+1, weight + items[i].weight, value + items[i].value, bestValue, items, n, capacity);
    }
}
