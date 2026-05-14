import random
import math
from typing import List, Tuple, Callable
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    weight: int
    value: int

class KnapsackSolver:
    def __init__(self, items: List[Item], capacity: int):
        self.items = items
        self.capacity = capacity
        self.stopped = False

    def stop(self):
        self.stopped = True

    def greedy(self, step_callback: Callable) -> Tuple[int, List[bool]]:
        indices = sorted(range(len(self.items)), key=lambda i: self.items[i].value/self.items[i].weight, reverse=True)
        taken = [False]*len(self.items)
        weight, value = 0, 0
        for idx in indices:
            if self.stopped: break
            desc = f"Рассматриваем {self.items[idx].name} (вес {self.items[idx].weight}, ценность {self.items[idx].value})"
            if weight + self.items[idx].weight <= self.capacity:
                taken[idx] = True
                weight += self.items[idx].weight
                value += self.items[idx].value
                desc += " → берём"
            else:
                desc += " → не влезает"
            step_callback(desc, taken.copy(), value, self.capacity - weight)
        return value, taken

    def brute_force(self, step_callback: Callable) -> Tuple[int, List[bool]]:
        n = len(self.items)
        best_val, best_taken = 0, [False]*n
        for mask in range(1<<n):
            if self.stopped: break
            weight, val = 0, 0
            taken = [False]*n
            for i in range(n):
                if mask>>i & 1:
                    weight += self.items[i].weight
                    val += self.items[i].value
                    taken[i] = True
            desc = f"Комбинация {mask:0{n}b}: вес {weight}, ценность {val}"
            if weight <= self.capacity and val > best_val:
                best_val, best_taken = val, taken.copy()
                desc += " ★ НОВАЯ ЛУЧШАЯ!"
            step_callback(desc, taken, val, self.capacity - weight)
        step_callback("Оптимум найден!", best_taken, best_val, self.capacity - sum(self.items[i].weight for i in range(n) if best_taken[i]))
        return best_val, best_taken

    def dp(self, step_callback: Callable) -> Tuple[int, List[bool]]:
        n, cap = len(self.items), self.capacity
        dp = [[0]*(cap+1) for _ in range(n+1)]
        for i in range(1, n+1):
            for w in range(cap+1):
                if self.stopped: break
                if self.items[i-1].weight <= w:
                    dp[i][w] = max(dp[i-1][w], dp[i-1][w-self.items[i-1].weight] + self.items[i-1].value)
                else:
                    dp[i][w] = dp[i-1][w]
                if w % max(1, cap//10) == 0 or w == cap:
                    step_callback(f"DP: [{i}][{w}] = {dp[i][w]}", [], dp[i][w], cap-w, dp)
            if self.stopped: break
        taken = [False]*n
        w = cap
        for i in range(n,0,-1):
            if dp[i][w] != dp[i-1][w]:
                taken[i-1] = True
                w -= self.items[i-1].weight
        step_callback(f"DP завершён. Ценность = {dp[n][cap]}", taken, dp[n][cap], w, dp)
        return dp[n][cap], taken

    def branch_and_bound(self, step_callback: Callable) -> Tuple[int, List[bool]]:
        n = len(self.items)
        items_with_idx = sorted([(i, self.items[i]) for i in range(n)], key=lambda x: x[1].value/x[1].weight, reverse=True)
        sorted_idx = [p[0] for p in items_with_idx]
        sorted_items = [self.items[i] for i in sorted_idx]

        best_val = 0
        best_taken = [False]*n

        def bound(idx, weight, value):
            if weight >= self.capacity:
                return value
            bound_val = value
            remain = self.capacity - weight
            for j in range(idx, n):
                if sorted_items[j].weight <= remain:
                    bound_val += sorted_items[j].value
                    remain -= sorted_items[j].weight
                else:
                    bound_val += (sorted_items[j].value / sorted_items[j].weight) * remain
                    break
            return bound_val

        def dfs(idx, weight, value, taken):
            nonlocal best_val, best_taken
            if self.stopped:
                return
            if idx == n:
                if value > best_val:
                    best_val = value
                    best_taken = [False]*n
                    for i, t in enumerate(taken):
                        if t:
                            best_taken[sorted_idx[i]] = True
                    step_callback(f"★ Новая лучшая ветка: ценность {best_val}", best_taken, best_val, self.capacity - weight)
                return
            if bound(idx+1, weight, value) > best_val:
                dfs(idx+1, weight, value, taken + [False])
            if weight + sorted_items[idx].weight <= self.capacity:
                new_taken = taken + [True]
                new_weight = weight + sorted_items[idx].weight
                new_value = value + sorted_items[idx].value
                step_callback(f"Ветка: берём {sorted_items[idx].name}, ценность={new_value}", 
                              [False]*n, new_value, self.capacity - new_weight)
                dfs(idx+1, new_weight, new_value, new_taken)

        step_callback("Запуск метода ветвей и границ...", [False]*n, 0, self.capacity)
        dfs(0, 0, 0, [])
        step_callback(f"Ветви и границы: оптимальная ценность = {best_val}", best_taken, best_val, 
                      self.capacity - sum(self.items[i].weight for i in range(n) if best_taken[i]))
        return best_val, best_taken

    def simulated_annealing(self, step_callback: Callable) -> Tuple[int, List[bool]]:
        """Метод имитации отжига (эвристика)"""
        n = len(self.items)
        # Начальное решение: жадное
        current_taken = [False]*n
        weight = 0
        value = 0
        indices = sorted(range(n), key=lambda i: self.items[i].value/self.items[i].weight, reverse=True)
        for i in indices:
            if weight + self.items[i].weight <= self.capacity:
                current_taken[i] = True
                weight += self.items[i].weight
                value += self.items[i].value
        best_taken = current_taken[:]
        best_val = value
        temperature = 1000.0
        cooling_rate = 0.95
        step_callback(f"Отжиг: начальное решение (жадное), ценность = {value}", current_taken, value, self.capacity - weight)
        while temperature > 1 and not self.stopped:
            # Генерируем соседнее решение: случайно добавить/удалить предмет
            new_taken = current_taken[:]
            idx = random.randint(0, n-1)
            new_taken[idx] = not new_taken[idx]
            # Проверяем вес
            new_weight = sum(self.items[i].weight for i in range(n) if new_taken[i])
            if new_weight <= self.capacity:
                new_value = sum(self.items[i].value for i in range(n) if new_taken[i])
                delta = new_value - value
                if delta > 0 or random.random() < math.exp(delta / temperature):
                    current_taken = new_taken[:]
                    weight = new_weight
                    value = new_value
                    if value > best_val:
                        best_val = value
                        best_taken = current_taken[:]
                        step_callback(f"Отжиг: новое лучшее решение, ценность = {best_val}", best_taken, best_val, self.capacity - weight)
            temperature *= cooling_rate
            step_callback(f"Отжиг: температура = {temperature:.2f}, текущая ценность = {value}", current_taken, value, self.capacity - weight)
        step_callback(f"Отжиг завершён, лучшая ценность = {best_val}", best_taken, best_val, self.capacity - sum(self.items[i].weight for i in range(n) if best_taken[i]))
        return best_val, best_taken
