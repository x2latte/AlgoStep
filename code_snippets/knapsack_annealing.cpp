// Имитация отжига (Simulated Annealing)
int simulatedAnnealing(Item items[], int n, int capacity) {
    vector<bool> current(n, false);
    int currentWeight = 0, currentValue = 0;
    vector<int> indices(n);
    iota(indices.begin(), indices.end(), 0);
    sort(indices.begin(), indices.end(), [&](int a, int b) {
        return (double)items[a].value/items[a].weight > (double)items[b].value/items[b].weight;
    });
    for (int idx : indices) {
        if (currentWeight + items[idx].weight <= capacity) {
            current[idx] = true;
            currentWeight += items[idx].weight;
            currentValue += items[idx].value;
        }
    }
    int bestValue = currentValue;
    double temperature = 1000.0, cooling = 0.95;
    while (temperature > 1) {
        int idx = rand() % n;
        vector<bool> neighbor = current;
        neighbor[idx] = !neighbor[idx];
        int newWeight = currentWeight + (neighbor[idx] ? items[idx].weight : -items[idx].weight);
        if (newWeight <= capacity) {
            int newValue = currentValue + (neighbor[idx] ? items[idx].value : -items[idx].value);
            int delta = newValue - currentValue;
            if (delta > 0 || exp(delta / temperature) > (double)rand() / RAND_MAX) {
                current = neighbor;
                currentWeight = newWeight;
                currentValue = newValue;
                if (currentValue > bestValue) bestValue = currentValue;
            }
        }
        temperature *= cooling;
    }
    return bestValue;
}
