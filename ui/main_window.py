from PyQt6.QtWidgets import QMainWindow, QTabWidget, QStatusBar
from .sorting_tab import SortingTab
from .graph_tab import GraphTab
from .knapsack_tab import KnapsackTab
from .testing_tab import TestingTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AlgoStep – Визуализация алгоритмов дискретной оптимизации")
        self.resize(1400, 900)
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.addTab(SortingTab(), "📊 Сортировка")
        self.tab_widget.addTab(GraphTab(), "🗺️ Графы")
        self.tab_widget.addTab(KnapsackTab(), "🎒 Рюкзак")
        self.tab_widget.addTab(TestingTab(), "🧪 Тестирование")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Готов")
