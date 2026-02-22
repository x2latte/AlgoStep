#include <iostream>
#include <vector>
#include <thread>
#include <chrono>

int main() {
    std::vector<int> arr = {5, 3, 8, 6, 2, 7, 4};

    int n = arr.size();
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                std::swap(arr[j], arr[j+1]);
            }
            // вывод состояния массива в stdout
            for (int k = 0; k < n; k++) std::cout << arr[k] << " ";
            std::cout << std::endl;
        }
    }
    return 0;
}
