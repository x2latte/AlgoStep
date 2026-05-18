// Жадный алгоритм для задачи о рюкзаке
struct Item {
    int weight;
    int value;
    string name;
};

bool compare(Item a, Item b) {
    double r1 = (double)a.value / a.weight;
    double r2 = (double)b.value / b.weight;
    return r1 > r2;
}

int greedyKnapsack(Item items[], int n, int capacity) {
    sort(items, items + n, compare);
    int currentWeight = 0;
    int totalValue = 0;
    for (int i = 0; i < n; i++) {
        if (currentWeight + items[i].weight <= capacity) {
            currentWeight += items[i].weight;
            totalValue += items[i].value;
        }
    }
    return totalValue;
}
