// Полный перебор для задачи о рюкзаке
int bruteForceKnapsack(Item items[], int n, int capacity) {
    int bestValue = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        int weight = 0, value = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) {
                weight += items[i].weight;
                value += items[i].value;
            }
        }
        if (weight <= capacity && value > bestValue) bestValue = value;
    }
    return bestValue;
}
