import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import time
import random
import os

from algorithms.knapsack import Item, KnapsackSolver
from algorithms.shortest_path import ShortestPathSolver
from algorithms.sorting import SortingSolver
from viz.knapsack_viz import KnapsackCanvas
from viz.graph_viz import GraphCanvas
from viz.sorting_viz import SortingCanvas

class AlgoStepApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AlgoStep - Дискретная оптимизация и сортировка")
        self.root.geometry("1450x950")
        self.root.configure(bg='#f0f4f8')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[12,5], background='#e0e7f0')
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('TLabelframe', font=('Segoe UI', 10), background='#ffffff')
        self.style.configure('TLabelframe.Label', font=('Segoe UI', 10, 'bold'), foreground='#2c3e50')
        
        self.current_solver = None
        self.loop_active = False
        self.speed_var = tk.DoubleVar(value=0.3)
        
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        self.knap_frame = ttk.Frame(notebook)
        notebook.add(self.knap_frame, text="🎒 Задача о рюкзаке")
        self.setup_knapsack()
        
        self.graph_frame = ttk.Frame(notebook)
        notebook.add(self.graph_frame, text="🗺️ Кратчайший путь")
        self.setup_graph()
        
        self.sort_frame = ttk.Frame(notebook)
        notebook.add(self.sort_frame, text="📊 Сортировка")
        self.setup_sorting()
        
        self.test_frame = ttk.Frame(notebook)
        notebook.add(self.test_frame, text="🧪 Тестирование")
        self.setup_testing()
        
        self.status_var = tk.StringVar(value="Готов")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, font=('Segoe UI', 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def show_info(self, title, text):
        info_win = tk.Toplevel(self.root)
        info_win.title(title)
        info_win.geometry("500x400")
        text_widget = tk.Text(info_win, wrap=tk.WORD, bg='#ffffe0', fg='black', font=('Segoe UI',10))
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)
        scroll = ttk.Scrollbar(info_win, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scroll.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # ------------------- Рюкзак -------------------
    def setup_knapsack(self):
        main_panel = ttk.Frame(self.knap_frame)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        left = ttk.Frame(main_panel)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        top_left = ttk.Frame(left)
        top_left.pack(fill=tk.X)
        ttk.Label(top_left, text="Вместимость:", font=('Segoe UI',10)).pack(side=tk.LEFT)
        self.capacity_spin = tk.IntVar(value=10)
        ttk.Spinbox(top_left, from_=1, to=100, textvariable=self.capacity_spin, width=6).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_left, text="🎲 Случайные данные", command=self.random_knapsack).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_left, text="❓", width=3, command=lambda: self.show_info("Задача о рюкзаке", 
            "Задача о рюкзаке: выбрать набор предметов с максимальной суммарной ценностью, не превышая вместимость.\n\n"
            "Алгоритмы:\n"
            "• Жадный: берёт предметы с лучшим соотношением ценность/вес. Быстро, но не всегда оптимально.\n"
            "• Полный перебор: проверяет все 2^n комбинаций. Точно, но медленно.\n"
            "• Динамическое программирование: заполняет таблицу O(n*W). Точно, умеренно быстро.\n"
            "• Ветви и границы: умный перебор с отсечением. Точно, быстрее полного.\n"
            "• Имитация отжига: эвристика, ищет приближённое решение.")).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(left, text="Предметы (название вес ценность):").pack(anchor=tk.W, pady=(10,0))
        self.items_text = tk.Text(left, height=6, width=32, bg='#ffffff', fg='black', font=('Consolas',9))
        self.items_text.pack(pady=5)
        self.items_text.insert(tk.END, "Книга 3 5\nНоутбук 4 8\nРучка 1 2\nФлешка 2 4")
        
        algo_frame = ttk.LabelFrame(left, text="Выбор алгоритма")
        algo_frame.pack(fill=tk.X, pady=5)
        self.algo_var = tk.StringVar(value="greedy")
        for text, val in [("Жадный", "greedy"), ("Полный перебор", "brute"), 
                          ("Динамическое программирование", "dp"), ("Ветви и границы", "bnb"),
                          ("Имитация отжига", "annealing")]:
            ttk.Radiobutton(algo_frame, text=text, variable=self.algo_var, value=val).pack(anchor=tk.W, padx=5, pady=1)
        
        self.step_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(left, text="Пошаговый режим", variable=self.step_mode).pack(anchor=tk.W, pady=5)
        speed_frame = ttk.Frame(left)
        speed_frame.pack(fill=tk.X, pady=5)
        ttk.Label(speed_frame, text="Скорость (сек/шаг):").pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(speed_frame, from_=0.05, to=1.5, variable=self.speed_var, orient=tk.HORIZONTAL)
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(speed_frame, textvariable=self.speed_var).pack(side=tk.LEFT)
        self.loop_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left, text="Циклический повтор", variable=self.loop_var).pack(anchor=tk.W, pady=5)
        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=10)
        self.run_btn = ttk.Button(btn_frame, text="▶ ЗАПУСТИТЬ", command=self.run_knapsack)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="⏹ СТОП", command=self.stop_algorithm, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        right = ttk.Frame(main_panel)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.knap_canvas = KnapsackCanvas(right, width=500, height=350)
        self.knap_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        self.knap_log = tk.Text(right, height=12, bg='#ffffff', fg='black', font=('Segoe UI',9))
        scroll = ttk.Scrollbar(right, command=self.knap_log.yview)
        self.knap_log.configure(yscrollcommand=scroll.set)
        self.knap_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def random_knapsack(self):
        n = random.randint(3, 6)
        cap = random.randint(10, 30)
        self.capacity_spin.set(cap)
        items = []
        names = ["Книга", "Ручка", "Ноутбук", "Телефон", "Флешка", "Часы", "Кофе", "Зонт", "Очки", "Блокнот"]
        for i in range(n):
            name = random.choice(names) + str(i)
            weight = random.randint(1, 10)
            value = random.randint(1, 20)
            items.append(f"{name} {weight} {value}")
        self.items_text.delete(1.0, tk.END)
        self.items_text.insert(tk.END, "\n".join(items))

    # ------------------- Граф -------------------
    def setup_graph(self):
        main_panel = ttk.Frame(self.graph_frame)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        left = ttk.Frame(main_panel)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        top_left = ttk.Frame(left)
        top_left.pack(fill=tk.X)
        ttk.Button(top_left, text="🎲 Случайный граф", command=self.random_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_left, text="❓", width=3, command=lambda: self.show_info("Кратчайший путь", 
            "Задача поиска кратчайшего пути: найти путь минимальной длины между двумя вершинами.\n\n"
            "Алгоритмы:\n"
            "• Дейкстра: жадный, работает с неотрицательными весами.\n"
            "• Полный перебор (DFS): проверяет все пути, точен, но экспоненциален.\n"
            "• Беллман-Форд: допускает отрицательные рёбра, находит кратчайшие пути.\n"
            "• A*: эвристический, обычно быстрее Дейкстры.\n"
            "• Флойд-Уоршелл: находит кратчайшие пути между всеми парами.")).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(left, text="Граф (список рёбер):").pack(anchor=tk.W, pady=(10,0))
        self.graph_text = tk.Text(left, height=8, width=35, bg='#ffffff', fg='black', font=('Consolas',9))
        self.graph_text.pack(pady=5)
        self.graph_text.insert(tk.END, "0 1 2\n0 2 4\n1 2 1\n1 3 7\n2 4 3\n3 4 1")
        frame = ttk.Frame(left)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text="Старт:").pack(side=tk.LEFT)
        self.start_var = tk.IntVar(value=0)
        ttk.Spinbox(frame, from_=0, to=20, textvariable=self.start_var, width=4).pack(side=tk.LEFT, padx=5)
        ttk.Label(frame, text="Цель:").pack(side=tk.LEFT)
        self.target_var = tk.IntVar(value=4)
        ttk.Spinbox(frame, from_=0, to=20, textvariable=self.target_var, width=4).pack(side=tk.LEFT, padx=5)
        
        algo_frame = ttk.LabelFrame(left, text="Выбор алгоритма")
        algo_frame.pack(fill=tk.X, pady=5)
        self.path_algo = tk.StringVar(value="dijkstra")
        for text, val in [("Дейкстра", "dijkstra"), ("Полный перебор", "brute"),
                          ("Беллман-Форд", "bellman"), ("A*", "astar"), ("Флойд-Уоршелл", "floyd")]:
            ttk.Radiobutton(algo_frame, text=text, variable=self.path_algo, value=val).pack(anchor=tk.W, padx=5, pady=1)
        
        self.path_step_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(left, text="Пошаговый режим", variable=self.path_step_mode).pack(anchor=tk.W, pady=5)
        speed_frame = ttk.Frame(left)
        speed_frame.pack(fill=tk.X, pady=5)
        ttk.Label(speed_frame, text="Скорость:").pack(side=tk.LEFT)
        self.path_speed_scale = ttk.Scale(speed_frame, from_=0.05, to=1.5, variable=self.speed_var, orient=tk.HORIZONTAL)
        self.path_speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.path_loop_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left, text="Циклический повтор", variable=self.path_loop_var).pack(anchor=tk.W, pady=5)
        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=10)
        self.run_path_btn = ttk.Button(btn_frame, text="▶ ЗАПУСТИТЬ", command=self.run_path)
        self.run_path_btn.pack(side=tk.LEFT, padx=5)
        self.stop_path_btn = ttk.Button(btn_frame, text="⏹ СТОП", command=self.stop_algorithm, state=tk.DISABLED)
        self.stop_path_btn.pack(side=tk.LEFT, padx=5)
        
        right = ttk.Frame(main_panel)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.graph_canvas = GraphCanvas(right, width=650, height=420)
        self.graph_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        self.path_log = tk.Text(right, height=10, bg='#ffffff', fg='black', font=('Segoe UI',9))
        self.path_log.pack(fill=tk.BOTH, expand=True)

    def random_graph(self):
        n = random.randint(3, 6)
        edges = []
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.3:
                    w = random.randint(1, 10)
                    edges.append(f"{i} {j} {w}")
        self.graph_text.delete(1.0, tk.END)
        self.graph_text.insert(tk.END, "\n".join(edges))
        self.start_var.set(random.randint(0, n-1))
        self.target_var.set(random.randint(0, n-1))

    # ------------------- Сортировка -------------------
    def setup_sorting(self):
        main_panel = ttk.Frame(self.sort_frame)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        left = ttk.Frame(main_panel)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        top_left = ttk.Frame(left)
        top_left.pack(fill=tk.X)
        ttk.Button(top_left, text="🎲 Случайный массив", command=self.random_array).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_left, text="❓", width=3, command=lambda: self.show_info("Сортировка", 
            "Сортировка – упорядочивание элементов по возрастанию/убыванию.\n\n"
            "Алгоритмы:\n"
            "• Пузырьковая: простой, медленный, O(n²).\n"
            "• Выбором: находит минимум и ставит в начало, O(n²).\n"
            "• Вставками: строит отсортированную часть, хорош для малых данных.\n"
            "• Быстрая: рекурсивная, O(n log n), обычно самая быстрая.\n"
            "• Слиянием: стабильная, O(n log n), требует доп. памяти.\n"
            "• Подсчётом: не сравнений, быстра для целых чисел в малом диапазоне.\n"
            "• Пирамидальная: использует кучу, O(n log n), нестабильная.")).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(left, text="Исходный массив (числа через пробел):").pack(anchor=tk.W)
        self.sort_array_text = tk.Text(left, height=4, width=30, bg='#ffffff', fg='black', font=('Consolas',9))
        self.sort_array_text.pack(pady=5)
        self.sort_array_text.insert(tk.END, "64 25 12 22 11 90 5 33")
        
        algo_frame = ttk.LabelFrame(left, text="Алгоритм сортировки")
        algo_frame.pack(fill=tk.X, pady=5)
        self.sort_algo = tk.StringVar(value="bubble")
        algorithms = [("Пузырьковая", "bubble"), ("Выбором", "selection"), ("Вставками", "insertion"),
                      ("Быстрая", "quick"), ("Слиянием", "merge"), ("Подсчётом", "counting"),
                      ("Пирамидальная", "heap")]
        for text, val in algorithms:
            ttk.Radiobutton(algo_frame, text=text, variable=self.sort_algo, value=val).pack(anchor=tk.W, padx=5, pady=1)
        
        self.sort_step_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(left, text="Пошаговый режим", variable=self.sort_step_mode).pack(anchor=tk.W, pady=5)
        self.sort_animate = tk.BooleanVar(value=True)
        ttk.Checkbutton(left, text="Плавная анимация обмена", variable=self.sort_animate).pack(anchor=tk.W, pady=2)
        speed_frame = ttk.Frame(left)
        speed_frame.pack(fill=tk.X, pady=5)
        ttk.Label(speed_frame, text="Скорость:").pack(side=tk.LEFT)
        self.sort_speed_scale = ttk.Scale(speed_frame, from_=0.05, to=1.0, variable=self.speed_var, orient=tk.HORIZONTAL)
        self.sort_speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.sort_loop_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left, text="Циклический повтор", variable=self.sort_loop_var).pack(anchor=tk.W, pady=5)
        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=10)
        self.run_sort_btn = ttk.Button(btn_frame, text="▶ ЗАПУСТИТЬ", command=self.run_sorting)
        self.run_sort_btn.pack(side=tk.LEFT, padx=5)
        self.stop_sort_btn = ttk.Button(btn_frame, text="⏹ СТОП", command=self.stop_algorithm, state=tk.DISABLED)
        self.stop_sort_btn.pack(side=tk.LEFT, padx=5)
        
        right = ttk.Frame(main_panel)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.sort_canvas = SortingCanvas(right, width=600, height=350)
        self.sort_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        self.sort_log = tk.Text(right, height=10, bg='#ffffff', fg='black', font=('Segoe UI',9))
        scroll = ttk.Scrollbar(right, command=self.sort_log.yview)
        self.sort_log.configure(yscrollcommand=scroll.set)
        self.sort_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def random_array(self):
        arr = [random.randint(5, 99) for _ in range(10)]
        self.sort_array_text.delete(1.0, tk.END)
        self.sort_array_text.insert(tk.END, ' '.join(map(str, arr)))

    # ------------------- Тестирование -------------------
    def setup_testing(self):
        main = ttk.Frame(self.test_frame)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(main, text="Выберите задачу и запустите тесты:", font=('Segoe UI',12)).pack(anchor=tk.W)
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Тестировать рюкзак", command=self.test_knapsack).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Тестировать граф", command=self.test_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Тестировать сортировку", command=self.test_sorting).pack(side=tk.LEFT, padx=5)
        self.test_output = tk.Text(main, height=20, bg='#ffffff', fg='black', font=('Consolas',10))
        self.test_output.pack(fill=tk.BOTH, expand=True, pady=10)
        scroll = ttk.Scrollbar(main, command=self.test_output.yview)
        self.test_output.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def test_knapsack(self):
        self.test_output.delete(1.0, tk.END)
        self.test_output.insert(tk.END, "Тестирование алгоритмов рюкзака\n" + "="*40 + "\n")
        # Тестовые наборы
        test_cases = [
            ([Item("A",2,3), Item("B",3,4), Item("C",4,5)], 5),
            ([Item("A",1,1), Item("B",2,2), Item("C",3,3), Item("D",4,4)], 5),
            ([Item("A",5,10), Item("B",3,7), Item("C",2,4)], 8)
        ]
        for idx, (items, cap) in enumerate(test_cases):
            self.test_output.insert(tk.END, f"\nТест {idx+1}: вместимость={cap}, предметов={len(items)}\n")
            solver = KnapsackSolver(items, cap)
            results = {}
            for name, algo in [("Жадный", solver.greedy), ("Полный перебор", solver.brute_force),
                               ("DP", solver.dp), ("Ветви и границы", solver.branch_and_bound),
                               ("Отжиг", solver.simulated_annealing)]:
                start = time.time()
                val, _ = algo(lambda *args: None)  # без шагов
                elapsed = time.time() - start
                results[name] = (val, elapsed)
            for name, (val, t) in results.items():
                self.test_output.insert(tk.END, f"  {name:15}: ценность={val:3}, время={t:.5f} сек\n")
        self.test_output.insert(tk.END, "\nТестирование завершено.\n")

    def test_graph(self):
        self.test_output.delete(1.0, tk.END)
        self.test_output.insert(tk.END, "Тестирование алгоритмов поиска пути\n" + "="*40 + "\n")
        test_cases = [
            ({0:[(1,2),(2,4)], 1:[(2,1),(3,7)], 2:[(4,3)], 3:[(4,1)]}, 0, 4, 5),
            ({0:[(1,1)], 1:[(2,1)], 2:[(3,1)], 3:[]}, 0, 3, 4),
        ]
        for idx, (graph, src, tgt, n) in enumerate(test_cases):
            self.test_output.insert(tk.END, f"\nТест {idx+1}: вершин={n}, старт={src}, цель={tgt}\n")
            results = {}
            for name, algo in [("Дейкстра", lambda s: s.dijkstra), ("Полный перебор", lambda s: s.brute_force),
                               ("Беллман-Форд", lambda s: s.bellman_ford), ("A*", lambda s: s.a_star),
                               ("Флойд-Уоршелл", lambda s: s.floyd_warshall)]:
                start = time.time()
                solver = ShortestPathSolver(graph, src, tgt, n)
                dist, _ = algo(solver)(lambda *args: None)
                elapsed = time.time() - start
                results[name] = (dist, elapsed)
            for name, (d, t) in results.items():
                self.test_output.insert(tk.END, f"  {name:15}: расстояние={d:3}, время={t:.5f} сек\n")
        self.test_output.insert(tk.END, "\nТестирование завершено.\n")

    def test_sorting(self):
        self.test_output.delete(1.0, tk.END)
        self.test_output.insert(tk.END, "Тестирование алгоритмов сортировки\n" + "="*40 + "\n")
        test_arrays = [
            [64, 25, 12, 22, 11, 90, 5, 33],
            [3, 2, 1, 5, 4],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1]
        ]
        for idx, arr in enumerate(test_arrays):
            self.test_output.insert(tk.END, f"\nТест {idx+1}: длина {len(arr)}\nИсходный: {arr}\n")
            results = {}
            for name, algo in [("Пузырьковая", "bubble_sort"), ("Выбором", "selection_sort"),
                               ("Вставками", "insertion_sort"), ("Быстрая", "quick_sort"),
                               ("Слиянием", "merge_sort"), ("Подсчётом", "counting_sort"),
                               ("Пирамидальная", "heap_sort")]:
                solver = SortingSolver(arr)
                start = time.time()
                getattr(solver, algo)(lambda *args: None)
                elapsed = time.time() - start
                results[name] = elapsed
            for name, t in results.items():
                self.test_output.insert(tk.END, f"  {name:15}: время={t:.5f} сек\n")
        self.test_output.insert(tk.END, "\nТестирование завершено.\n")

    # ---------- Общие методы остановки ----------
    def stop_algorithm(self):
        if self.current_solver:
            self.current_solver.stop()
        self.status_var.set("Остановка...")
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.run_path_btn.config(state=tk.NORMAL)
        self.stop_path_btn.config(state=tk.DISABLED)
        self.run_sort_btn.config(state=tk.NORMAL)
        self.stop_sort_btn.config(state=tk.DISABLED)

    def parse_items(self):
        lines = self.items_text.get("1.0", tk.END).strip().splitlines()
        items = []
        for line in lines:
            parts = line.split()
            if len(parts)==3:
                items.append(Item(parts[0], int(parts[1]), int(parts[2])))
        return items, self.capacity_spin.get()

    def run_knapsack(self):
        items, cap = self.parse_items()
        if not items:
            self.status_var.set("Ошибка: нет предметов")
            return
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.loop_active = self.loop_var.get()
        def worker():
            while True:
                if self.current_solver:
                    self.current_solver.stop()
                solver = KnapsackSolver(items, cap)
                self.current_solver = solver
                self.knap_log.delete(1.0, tk.END)
                self.knap_canvas.set_problem(cap, items)
                self.status_var.set("Выполняется рюкзак...")
                q = queue.Queue()
                def callback(desc, taken, cur_val, left, dp_table=None):
                    q.put(('knap', desc, taken, cur_val, left))
                def process_queue():
                    try:
                        while True:
                            typ, desc, taken, cur_val, left = q.get_nowait()
                            if not self.knap_log.winfo_exists():
                                return
                            self.knap_log.insert(tk.END, desc + "\n")
                            self.knap_log.see(tk.END)
                            self.knap_canvas.update_state(taken, cap-left, cur_val)
                            self.root.update()
                            delay = self.speed_var.get() if self.step_mode.get() else 0
                            if delay>0: time.sleep(delay)
                            q.task_done()
                    except queue.Empty:
                        pass
                    finally:
                        if self.knap_log.winfo_exists():
                            self.root.after(50, process_queue)
                process_queue()
                algo = self.algo_var.get()
                if algo == "greedy": solver.greedy(callback)
                elif algo == "brute": solver.brute_force(callback)
                elif algo == "dp": solver.dp(callback)
                elif algo == "bnb": solver.branch_and_bound(callback)
                else: solver.simulated_annealing(callback)
                if solver.stopped: self.status_var.set("Остановлено")
                else: self.status_var.set("Алгоритм рюкзака завершён")
                if not self.loop_active or solver.stopped: break
                time.sleep(0.5)
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))
            self.current_solver = None
        threading.Thread(target=worker, daemon=True).start()

    def parse_graph(self):
        lines = self.graph_text.get("1.0", tk.END).strip().splitlines()
        graph = {}
        max_v = 0
        for line in lines:
            if not line.strip(): continue
            u,v,w = map(int, line.split())
            graph.setdefault(u, []).append((v,w))
            max_v = max(max_v, u, v)
        n = max_v+1
        return graph, self.start_var.get(), self.target_var.get(), n

    def run_path(self):
        graph, src, tgt, n = self.parse_graph()
        self.run_path_btn.config(state=tk.DISABLED)
        self.stop_path_btn.config(state=tk.NORMAL)
        self.loop_active = self.path_loop_var.get()
        def worker():
            while True:
                if self.current_solver: self.current_solver.stop()
                solver = ShortestPathSolver(graph, src, tgt, n)
                self.current_solver = solver
                self.path_log.delete(1.0, tk.END)
                self.graph_canvas.set_graph(graph, n)
                self.graph_canvas.clear_highlights()
                self.status_var.set("Поиск пути...")
                q = queue.Queue()
                def callback(desc, vertex, dist, distances, visited, path, edge):
                    q.put(('path', desc, vertex, path, edge))
                def process_queue():
                    try:
                        while True:
                            typ, desc, vertex, path, edge = q.get_nowait()
                            if not self.path_log.winfo_exists():
                                return
                            self.path_log.insert(tk.END, desc + "\n")
                            self.path_log.see(tk.END)
                            if vertex != -1:
                                self.graph_canvas.highlight_vertex(vertex, '#A5D6A5')
                            if edge:
                                self.graph_canvas.highlight_edge(edge[0], edge[1], '#FFA726')
                            if path:
                                self.graph_canvas.set_path(path)
                            self.root.update()
                            delay = self.speed_var.get() if self.path_step_mode.get() else 0
                            if delay>0: time.sleep(delay)
                            q.task_done()
                    except queue.Empty: pass
                    finally:
                        if self.path_log.winfo_exists():
                            self.root.after(50, process_queue)
                process_queue()
                algo = self.path_algo.get()
                if algo == "dijkstra": solver.dijkstra(callback)
                elif algo == "brute": solver.brute_force(callback)
                elif algo == "bellman": solver.bellman_ford(callback)
                elif algo == "astar": solver.a_star(callback)
                else: solver.floyd_warshall(callback)
                if solver.stopped: self.status_var.set("Остановлено")
                else: self.status_var.set("Поиск завершён")
                if not self.loop_active or solver.stopped: break
                time.sleep(0.5)
            self.root.after(0, lambda: self.run_path_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_path_btn.config(state=tk.DISABLED))
            self.current_solver = None
        threading.Thread(target=worker, daemon=True).start()

    def run_sorting(self):
        text = self.sort_array_text.get("1.0", tk.END).strip()
        try:
            arr = list(map(int, text.split()))
        except:
            self.status_var.set("Ошибка: введите числа через пробел")
            return
        if not arr:
            self.status_var.set("Пустой массив")
            return
        self.run_sort_btn.config(state=tk.DISABLED)
        self.stop_sort_btn.config(state=tk.NORMAL)
        self.loop_active = self.sort_loop_var.get()
        self.sort_canvas.set_animation(self.sort_animate.get())
        def worker():
            while True:
                if self.current_solver: self.current_solver.stop()
                solver = SortingSolver(arr)
                self.current_solver = solver
                self.sort_log.delete(1.0, tk.END)
                self.sort_canvas.set_data(arr)
                self.status_var.set("Сортировка...")
                q = queue.Queue()
                def callback(current_arr, desc, idx1, idx2):
                    if idx1 != -1 and idx2 != -1 and self.sort_animate.get():
                        q.put(('swap', current_arr, desc, idx1, idx2))
                    else:
                        q.put(('update', current_arr, desc, idx1, idx2))
                def process_queue():
                    try:
                        while True:
                            typ, cur_arr, desc, i1, i2 = q.get_nowait()
                            if not self.sort_log.winfo_exists():
                                return
                            self.sort_log.insert(tk.END, desc + "\n")
                            self.sort_log.see(tk.END)
                            if typ == 'swap' and self.sort_animate.get():
                                self.sort_canvas.animate_swap(i1, i2)
                                self.sort_canvas.values = cur_arr[:]
                                self.sort_canvas.draw(highlight_indices=(i1, i2))
                            else:
                                self.sort_canvas.update_state(cur_arr, i1, i2 if i2 != -1 else None)
                            self.root.update()
                            delay = self.speed_var.get() if self.sort_step_mode.get() else 0
                            if delay>0: time.sleep(delay)
                            q.task_done()
                    except queue.Empty: pass
                    finally:
                        if self.sort_log.winfo_exists():
                            self.root.after(50, process_queue)
                process_queue()
                algo = self.sort_algo.get()
                if algo == "bubble": solver.bubble_sort(callback)
                elif algo == "selection": solver.selection_sort(callback)
                elif algo == "insertion": solver.insertion_sort(callback)
                elif algo == "quick": solver.quick_sort(callback)
                elif algo == "merge": solver.merge_sort(callback)
                elif algo == "counting": solver.counting_sort(callback)
                else: solver.heap_sort(callback)
                if solver.stopped: self.status_var.set("Сортировка остановлена")
                else: self.status_var.set("Сортировка завершена")
                if not self.loop_active or solver.stopped: break
                time.sleep(0.8)
            self.root.after(0, lambda: self.run_sort_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_sort_btn.config(state=tk.DISABLED))
            self.current_solver = None
        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgoStepApp(root)
    root.mainloop()
