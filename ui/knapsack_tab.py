from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextEdit, QComboBox, QCheckBox, QSlider, QLabel,
                             QSpinBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from visualizers.knapsack_visualizer import KnapsackVisualizer
from algorithms.knapsack import (GreedyKnapsack, DPKnapsack, BruteForceKnapsack,
                                 BacktrackingKnapsack, BranchAndBoundKnapsack)
import random
import os

class KnapsackTab(QWidget):
    def __init__(self):
        super().__init__()
        self.algorithms = {
            "Жадный": (GreedyKnapsack, "knapsack_greedy.cpp"),
            "Динамическое программирование": (DPKnapsack, "knapsack_dp.cpp"),
            "Полный перебор": (BruteForceKnapsack, "knapsack_bruteforce.cpp"),
            "Backtracking": (BacktrackingKnapsack, "knapsack_backtracking.cpp"),
            "Ветви и границы": (BranchAndBoundKnapsack, "knapsack_branchbound.cpp"),
        }
        self.current_solver = None
        self.current_generator = None
        self.step_timer = QTimer()
        self.step_timer.timeout.connect(self.next_step)
        self.init_ui()
        self.set_default()
        self.update_code()

    def init_ui(self):
        main_layout = QHBoxLayout()
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        cap_layout = QHBoxLayout()
        cap_layout.addWidget(QLabel("Вместимость:"))
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setRange(1, 100)
        self.capacity_spin.setValue(10)
        cap_layout.addWidget(self.capacity_spin)
        left_layout.addLayout(cap_layout)

        left_layout.addWidget(QLabel("Предметы (название вес ценность):"))
        self.items_input = QTextEdit()
        self.items_input.setPlainText("Книга 3 5\nНоутбук 4 8\nРучка 1 2\nФлешка 2 4")
        left_layout.addWidget(self.items_input)

        btn_layout = QHBoxLayout()
        self.random_btn = QPushButton("🎲 Случайные данные")
        self.random_btn.clicked.connect(self.random_items)
        self.reset_btn = QPushButton("⟳ Сброс")
        self.reset_btn.clicked.connect(self.set_default)
        btn_layout.addWidget(self.random_btn)
        btn_layout.addWidget(self.reset_btn)
        left_layout.addLayout(btn_layout)

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
        self.start_btn.clicked.connect(self.start_knapsack)
        self.stop_btn.clicked.connect(self.stop_knapsack)
        btn_layout2.addWidget(self.start_btn)
        btn_layout2.addWidget(self.stop_btn)
        left_layout.addLayout(btn_layout2)

        left_layout.addWidget(QLabel("Лог:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        left_layout.addWidget(self.log_text)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.visualizer = KnapsackVisualizer()
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

    def parse_items(self):
        from algorithms.knapsack.solver import Item
        lines = self.items_input.toPlainText().strip().splitlines()
        items = []
        for line in lines:
            parts = line.split()
            if len(parts) != 3:
                raise ValueError("Каждая строка: название вес ценность")
            name = parts[0]
            w = int(parts[1])
            v = int(parts[2])
            items.append(Item(name, w, v))
        return items, self.capacity_spin.value()

    def set_default(self):
        self.items_input.setPlainText("Книга 3 5\nНоутбук 4 8\nРучка 1 2\nФлешка 2 4")
        self.capacity_spin.setValue(10)
        self.reset_display()

    def random_items(self):
        n = random.randint(3, 6)
        cap = random.randint(10, 30)
        self.capacity_spin.setValue(cap)
        items = []
        names = ["Книга", "Ручка", "Ноутбук", "Телефон", "Флешка", "Часы", "Кофе", "Зонт", "Очки", "Блокнот"]
        for i in range(n):
            name = random.choice(names) + str(i)
            w = random.randint(1, 10)
            v = random.randint(1, 20)
            items.append(f"{name} {w} {v}")
        self.items_input.setPlainText("\n".join(items))
        self.reset_display()

    def reset_display(self):
        try:
            items, cap = self.parse_items()
            self.visualizer.set_problem(items, cap)
            self.log_text.clear()
            self.clear_code_highlight()
        except Exception as e:
            self.log_text.append(f"Ошибка: {e}")

    def start_knapsack(self):
        try:
            items, cap = self.parse_items()
        except Exception as e:
            self.log_text.append(f"Ошибка: {e}")
            return
        algo_name = self.algo_combo.currentText()
        if algo_name not in self.algorithms:
            return
        algo_class, _ = self.algorithms[algo_name]
        self.current_solver = algo_class(items, cap)
        self.current_generator = self.current_solver.run()
        self.visualizer.set_problem(items, cap)
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
            # Ожидаем 5 элементов: msg, taken, cur_val, left, line_num
            if len(result) == 5:
                msg, taken, cur_val, left, line_num = result
                if line_num != -1:
                    self.highlight_code_line(line_num)
            else:
                msg, taken, cur_val, left = result
            self.log_text.append(msg)
            self.log_text.ensureCursorVisible()
            self.visualizer.update_state(taken, cur_val, left)
        except StopIteration:
            self.stop_knapsack()
            if self.loop_cb.isChecked():
                self.start_knapsack()

    def stop_knapsack(self):
        if self.current_solver:
            self.current_solver.stop()
        self.step_timer.stop()
        self.current_generator = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
