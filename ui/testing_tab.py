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
                [64, 25, 12, 22, 11, 90, 5, 33],
                [3, 2, 1, 5, 4],
                [1, 2, 3, 4, 5],
                [5, 4, 3, 2, 1],
                [random.randint(1, 100) for _ in range(20)]
            ]
            algos = [("Пузырьковая", BubbleSort), ("Выбором", SelectionSort),
                     ("Вставками", InsertionSort), ("Быстрая", QuickSort),
                     ("Слиянием", MergeSort), ("Подсчётом", CountingSort)]
            for arr in arrays:
                self.log_signal.emit(f"\nМассив: {arr[:10]}... (длина {len(arr)})")
                for name, Algo in algos:
                    solver = Algo(arr)
                    start = time.time()
                    list(solver.run())  # прогоняем все шаги
                    elapsed = time.time() - start
                    self.log_signal.emit(f"  {name:15}: {elapsed:.5f} сек")
        elif self.test_type == "graph":
            graph = {0:[(1,2),(2,4)], 1:[(2,1),(3,7)], 2:[(4,3)], 3:[(4,1)]}
            src, tgt = 0, 4
            n = 5
            algos = [("Дейкстра", Dijkstra), ("Беллман-Форд", BellmanFord),
                     ("Полный перебор", BruteForceGraph), ("A*", AStar), ("Флойд-Уоршелл", FloydWarshall)]
            for name, Algo in algos:
                solver = Algo(graph, src, tgt, n)
                start = time.time()
                list(solver.run())
                elapsed = time.time() - start
                self.log_signal.emit(f"{name:15}: {elapsed:.5f} сек")
        elif self.test_type == "knapsack":
            items = [Item("A",2,3), Item("B",3,4), Item("C",4,5), Item("D",1,2)]
            capacity = 5
            algos = [("Жадный", GreedyKnapsack), ("DP", DPKnapsack),
                     ("Полный перебор", BruteForceKnapsack), ("Backtracking", BacktrackingKnapsack),
                     ("Ветви и границы", BranchAndBoundKnapsack)]
            for name, Algo in algos:
                solver = Algo(items, capacity)
                start = time.time()
                list(solver.run())
                elapsed = time.time() - start
                self.log_signal.emit(f"{name:15}: {elapsed:.5f} сек")
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
        self.worker.finished_signal.connect(lambda: self.output.append("\nТестирование завершено."))
        self.worker.start()
