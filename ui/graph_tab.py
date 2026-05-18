from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextEdit, QComboBox, QCheckBox, QSlider, QLabel,
                             QSpinBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from visualizers.graph_visualizer import GraphVisualizer
from algorithms.graph import (Dijkstra, BellmanFord, BruteForceGraph, AStar, FloydWarshall)
import random
import os

class GraphTab(QWidget):
    def __init__(self):
        super().__init__()
        self.algorithms = {
            "Дейкстра": (Dijkstra, "dijkstra.cpp"),
            "Беллман-Форд": (BellmanFord, "bellman_ford.cpp"),
            "Полный перебор": (BruteForceGraph, "brute_force.cpp"),
            "A*": (AStar, "a_star.cpp"),
            "Флойд-Уоршелл": (FloydWarshall, "floyd_warshall.cpp"),
        }
        self.current_solver = None
        self.current_generator = None
        self.step_timer = QTimer()
        self.step_timer.timeout.connect(self.next_step)
        self.init_ui()
        self.set_default_graph()
        self.update_code()

    def init_ui(self):
        main_layout = QHBoxLayout()
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.graph_input = QTextEdit()
        self.graph_input.setPlainText("0 1 2\n0 2 4\n1 2 1\n1 3 7\n2 4 3\n3 4 1")
        left_layout.addWidget(QLabel("Граф (список рёбер: from to weight):"))
        left_layout.addWidget(self.graph_input)

        btn_layout = QHBoxLayout()
        self.random_btn = QPushButton("🎲 Случайный граф")
        self.random_btn.clicked.connect(self.random_graph)
        self.reset_btn = QPushButton("⟳ Сброс")
        self.reset_btn.clicked.connect(self.set_default_graph)
        btn_layout.addWidget(self.random_btn)
        btn_layout.addWidget(self.reset_btn)
        left_layout.addLayout(btn_layout)

        spin_layout = QHBoxLayout()
        spin_layout.addWidget(QLabel("Старт:"))
        self.start_spin = QSpinBox()
        self.start_spin.setRange(0, 20)
        spin_layout.addWidget(self.start_spin)
        spin_layout.addWidget(QLabel("Цель:"))
        self.target_spin = QSpinBox()
        self.target_spin.setRange(0, 20)
        self.target_spin.setValue(4)
        spin_layout.addWidget(self.target_spin)
        left_layout.addLayout(spin_layout)

        left_layout.addWidget(QLabel("Алгоритм:"))
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(self.algorithms.keys())
        self.algo_combo.currentTextChanged.connect(self.update_code)
        left_layout.addWidget(self.algo_combo)

        self.step_mode_cb = QCheckBox("Пошаговый режим")
        self.step_mode_cb.setChecked(True)
        left_layout.addWidget(self.step_mode_cb)

        left_layout.addWidget(QLabel("Скорость (сек/шаг):"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(5, 200)
        self.speed_slider.setValue(30)
        left_layout.addWidget(self.speed_slider)

        self.loop_cb = QCheckBox("Циклический повтор")
        left_layout.addWidget(self.loop_cb)

        btn_layout2 = QHBoxLayout()
        self.start_btn = QPushButton("▶ ЗАПУСТИТЬ")
        self.stop_btn = QPushButton("⏹ СТОП")
        self.stop_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_path)
        self.stop_btn.clicked.connect(self.stop_path)
        btn_layout2.addWidget(self.start_btn)
        btn_layout2.addWidget(self.stop_btn)
        left_layout.addLayout(btn_layout2)

        left_layout.addWidget(QLabel("Лог:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        left_layout.addWidget(self.log_text)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.visualizer = GraphVisualizer()
        right_layout.addWidget(self.visualizer)

        right_layout.addWidget(QLabel("Исходный код (C++):"))
        self.code_edit = QTextEdit()
        self.code_edit.setReadOnly(True)
        self.code_edit.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas;")
        right_layout.addWidget(self.code_edit)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        self.setLayout(main_layout)

    def update_code(self):
        algo_name = self.algo_combo.currentText()
        if algo_name not in self.algorithms:
            return
        _, filename = self.algorithms[algo_name]
        code_path = os.path.join("code_snippets", filename)
        try:
            with open(code_path, 'r') as f:
                code = f.read()
        except:
            code = f"// Код для {algo_name} не найден"
        self.code_edit.setPlainText(code)
        self.clear_code_highlight()

    def clear_code_highlight(self):
        cursor = self.code_edit.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#1e1e1e"))
        fmt.setForeground(QColor("#d4d4d4"))
        cursor.setCharFormat(fmt)
        cursor.clearSelection()
        self.code_edit.setTextCursor(cursor)

    def highlight_code_line(self, line_num):
        if line_num < 1:
            return
        self.clear_code_highlight()
        cursor = self.code_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        for _ in range(line_num - 1):
            cursor.movePosition(QTextCursor.MoveOperation.NextBlock)
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(255, 255, 0, 120))
        fmt.setForeground(QColor(0, 0, 0))
        cursor.setCharFormat(fmt)
        self.code_edit.setTextCursor(cursor)
        self.code_edit.ensureCursorVisible()

    def parse_graph(self):
        text = self.graph_input.toPlainText().strip()
        graph = {}
        max_v = 0
        for line in text.splitlines():
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError("Каждая строка должна содержать: from to weight")
            u, v, w = map(int, parts)
            graph.setdefault(u, []).append((v, w))
            max_v = max(max_v, u, v)
        n = max_v + 1
        return graph, n

    def set_default_graph(self):
        self.graph_input.setPlainText("0 1 2\n0 2 4\n1 2 1\n1 3 7\n2 4 3\n3 4 1")
        self.start_spin.setValue(0)
        self.target_spin.setValue(4)
        self.reset_display()

    def random_graph(self):
        n = random.randint(3, 6)
        edges = []
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.3:
                    w = random.randint(1, 10)
                    edges.append(f"{i} {j} {w}")
        self.graph_input.setPlainText("\n".join(edges))
        self.start_spin.setValue(random.randint(0, n-1))
        self.target_spin.setValue(random.randint(0, n-1))
        self.reset_display()

    def reset_display(self):
        try:
            graph, n = self.parse_graph()
            self.visualizer.set_graph(graph, n)
            self.log_text.clear()
            self.clear_code_highlight()
        except Exception as e:
            self.log_text.append(f"Ошибка графа: {e}")

    def start_path(self):
        try:
            graph, n = self.parse_graph()
        except Exception as e:
            self.log_text.append(f"Ошибка: {e}")
            return
        src = self.start_spin.value()
        tgt = self.target_spin.value()
        if src >= n or tgt >= n:
            self.log_text.append("Старт или цель вне диапазона вершин")
            return
        algo_name = self.algo_combo.currentText()
        if algo_name not in self.algorithms:
            return
        algo_class, _ = self.algorithms[algo_name]
        self.current_solver = algo_class(graph, src, tgt, n)
        self.current_generator = self.current_solver.run()
        self.visualizer.set_graph(graph, n)
        self.log_text.clear()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.step_timer.start(self.speed_slider.value() * 10)
        self.next_step()

    def next_step(self):
        if self.current_generator is None:
            return
        try:
            result = next(self.current_generator)
            # Ожидаем 7 элементов: msg, vertex, dist, dist_list, path, edge, line_num
            if len(result) == 7:
                msg, vertex, dist, dist_list, path, edge, line_num = result
                if line_num != -1:
                    self.highlight_code_line(line_num)
            else:
                # fallback для старых версий (без line_num)
                msg, vertex, dist, dist_list, path, edge = result
            self.log_text.append(msg)
            self.log_text.ensureCursorVisible()
            if vertex != -1:
                self.visualizer.highlight_vertex(vertex, "lightgreen")
            if edge:
                self.visualizer.highlight_edge(edge[0], edge[1], "red")
            if path:
                self.visualizer.set_path(path)
        except StopIteration:
            self.stop_path()
            if self.loop_cb.isChecked():
                self.start_path()

    def stop_path(self):
        if self.current_solver:
            self.current_solver.stop()
        self.step_timer.stop()
        self.current_generator = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
