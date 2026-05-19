from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextEdit, QLabel)
from PyQt6.QtCore import QThread, pyqtSignal
import time
import random
from algorithms.sorting import BubbleSort, SelectionSort, InsertionSort, QuickSort, MergeSort, CountingSort
from algorithms.graph import Dijkstra, BellmanFord, BruteForceGraph, AStar, FloydWarshall
from algorithms.knapsack import GreedyKnapsack, DPKnapsack, BruteForceKnapsack, BacktrackingKnapsack, BranchAndBoundKnapsack
from algorithms.knapsack.solver import Item

class TestWorker(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, test_type):
        super().__init__()
        self.test_type = test_type

    def run(self):
        if self.test_type == "sorting":
            arrays = [
                ([64, 25, 12, 22, 11, 90, 5, 33], "Случайный массив (8 эл.)"),
                ([3, 2, 1, 5, 4], "Почти отсортированный (5 эл.)"),
                ([1, 2, 3, 4, 5], "Уже отсортированный (5 эл.)"),
                ([5, 4, 3, 2, 1], "Обратный порядок (5 эл.)"),
                ([random.randint(1, 100) for _ in range(20)], "Случайный массив (20 эл.)"),
            ]
            algos = [("Пузырьковая", BubbleSort), ("Выбором", SelectionSort),
                     ("Вставками", InsertionSort), ("Быстрая", QuickSort),
                     ("Слиянием", MergeSort), ("Подсчётом", CountingSort)]
            for arr, desc in arrays:
                self.log_signal.emit(f"\n▶ {desc}: {arr[:10]}{'...' if len(arr)>10 else ''}")
                for name, Algo in algos:
                    solver = Algo(arr)
                    start = time.time()
                    list(solver.run())
                    elapsed = time.time() - start
                    self.log_signal.emit(f"   {name:15}: {elapsed:.5f} сек")
        elif self.test_type == "graph":
            # Тестовый граф 1: обычный
            graph1 = {0:[(1,2),(2,4)], 1:[(2,1),(3,7)], 2:[(4,3)], 3:[(4,1)]}
            src1, tgt1, n1 = 0, 4, 5
            desc1 = "Граф 1 (5 вершин, 7 рёбер, все веса ≥0)"
            # Граф 2: линейный
            graph2 = {0:[(1,1)], 1:[(2,1)], 2:[(3,1)], 3:[]}
            src2, tgt2, n2 = 0, 3, 4
            desc2 = "Граф 2 (линейный, 4 вершины)"
            # Граф 3: с отрицательными весами для проверки Дейкстры
            graph3 = {0:[(1,2),(2,4)], 1:[(2,-1),(3,7)], 2:[(4,3)], 3:[(4,1)]}
            src3, tgt3, n3 = 0, 4, 5
            desc3 = "Граф 3 (есть отрицательное ребро 1→2 = -1)"
            test_cases = [(graph1, src1, tgt1, n1, desc1),
                          (graph2, src2, tgt2, n2, desc2),
                          (graph3, src3, tgt3, n3, desc3)]
            algos = [("Дейкстра", Dijkstra), ("Беллман-Форд", BellmanFord),
                     ("Полный перебор", BruteForceGraph), ("A*", AStar),
                     ("Флойд-Уоршелл", FloydWarshall)]
            for graph, src, tgt, n, desc in test_cases:
                self.log_signal.emit(f"\n▶ {desc}: старт={src}, цель={tgt}, вершин={n}")
                # Покажем первые 5 рёбер для примера
                edge_sample = []
                for u in sorted(graph.keys()):
                    for v,w in graph[u]:
                        edge_sample.append(f"{u}→{v}({w})")
                        if len(edge_sample) >= 5:
                            break
                    if len(edge_sample) >= 5:
                        break
                self.log_signal.emit(f"   Примеры рёбер: {', '.join(edge_sample)}{' ...' if len(edge_sample)>=5 else ''}")
                for name, Algo in algos:
                    # Пропускаем Дейкстру для графа с отрицательными весами
                    if name == "Дейкстра" and any(w < 0 for u in graph for v,w in graph[u]):
                        self.log_signal.emit(f"   {name:15}: пропущен (отрицательные веса)")
                        continue
                    solver = Algo(graph, src, tgt, n)
                    start = time.time()
                    try:
                        list(solver.run())
                        elapsed = time.time() - start
                        self.log_signal.emit(f"   {name:15}: {elapsed:.5f} сек")
                    except Exception as e:
                        self.log_signal.emit(f"   {name:15}: ошибка - {e}")
        elif self.test_type == "knapsack":
            test_cases = [
                ([Item("A",2,3), Item("B",3,4), Item("C",4,5)], 5, "3 предмета, вместимость 5"),
                ([Item("A",1,1), Item("B",2,2), Item("C",3,3), Item("D",4,4)], 5, "4 предмета, вместимость 5"),
                ([Item("A",5,10), Item("B",3,7), Item("C",2,4)], 8, "3 предмета, вместимость 8"),
            ]
            algos = [("Жадный", GreedyKnapsack), ("DP", DPKnapsack),
                     ("Полный перебор", BruteForceKnapsack), ("Backtracking", BacktrackingKnapsack),
                     ("Ветви и границы", BranchAndBoundKnapsack)]
            for items, capacity, desc in test_cases:
                self.log_signal.emit(f"\n▶ {desc}:")
                # Выводим список предметов
                items_str = ", ".join([f"{it.name}({it.weight},{it.value})" for it in items[:5]])
                if len(items) > 5:
                    items_str += f" ... и ещё {len(items)-5}"
                self.log_signal.emit(f"   Предметы: {items_str}")
                for name, Algo in algos:
                    solver = Algo(items, capacity)
                    start = time.time()
                    list(solver.run())
                    elapsed = time.time() - start
                    self.log_signal.emit(f"   {name:15}: {elapsed:.5f} сек")
        self.finished_signal.emit()

class TestingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.sort_btn = QPushButton("Тестировать сортировку")
        self.graph_btn = QPushButton("Тестировать графы")
        self.knap_btn = QPushButton("Тестировать рюкзак")
        self.sort_btn.clicked.connect(lambda: self.run_test("sorting"))
        self.graph_btn.clicked.connect(lambda: self.run_test("graph"))
        self.knap_btn.clicked.connect(lambda: self.run_test("knapsack"))
        btn_layout.addWidget(self.sort_btn)
        btn_layout.addWidget(self.graph_btn)
        btn_layout.addWidget(self.knap_btn)
        layout.addLayout(btn_layout)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def run_test(self, test_type):
        self.output.clear()
        self.output.append(f"Запуск тестирования {test_type}...\n")
        self.worker = TestWorker(test_type)
        self.worker.log_signal.connect(self.output.append)
        self.worker.finished_signal.connect(lambda: self.output.append("\n✅ Тестирование завершено."))
        self.worker.start()
