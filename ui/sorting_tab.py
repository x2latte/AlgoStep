from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextEdit, QComboBox, QCheckBox, QSlider, QLabel)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from visualizers.sorting_visualizer import SortingVisualizer
from algorithms.sorting import (BubbleSort, SelectionSort, InsertionSort,
                                QuickSort, MergeSort, CountingSort)
import random
import os

class SortingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.algorithms = {
            "Пузырьковая": (BubbleSort, "bubble_sort.cpp"),
            "Выбором": (SelectionSort, "selection_sort.cpp"),
            "Вставками": (InsertionSort, "insertion_sort.cpp"),
            "Быстрая": (QuickSort, "quick_sort.cpp"),
            "Слиянием": (MergeSort, "merge_sort.cpp"),
            "Подсчётом": (CountingSort, "counting_sort.cpp"),
        }
        self.current_solver = None
        self.current_generator = None
        self.step_timer = QTimer()
        self.step_timer.timeout.connect(self.next_step)
        self.init_ui()
        self.reset_array()
        self.update_code()

    def init_ui(self):
        main_layout = QHBoxLayout()
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.array_input = QTextEdit()
        self.array_input.setPlainText("64 25 12 22 11 90 5 33")
        left_layout.addWidget(QLabel("Массив (числа через пробел):"))
        left_layout.addWidget(self.array_input)

        btn_layout = QHBoxLayout()
        self.random_btn = QPushButton("🎲 Случайный массив")
        self.random_btn.clicked.connect(self.random_array)
        self.reset_btn = QPushButton("⟳ Сброс к исходному")
        self.reset_btn.clicked.connect(self.reset_array)
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
        self.start_btn.clicked.connect(self.start_sorting)
        self.stop_btn.clicked.connect(self.stop_sorting)
        btn_layout2.addWidget(self.start_btn)
        btn_layout2.addWidget(self.stop_btn)
        left_layout.addLayout(btn_layout2)

        left_layout.addWidget(QLabel("Лог:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        left_layout.addWidget(self.log_text)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.visualizer = SortingVisualizer()
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
        # Сохраняем позицию прокрутки
        scrollbar = self.code_edit.verticalScrollBar()
        scroll_pos = scrollbar.value()
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
        # Восстанавливаем прокрутку
        scrollbar.setValue(scroll_pos)

    def random_array(self):
        arr = [random.randint(5, 99) for _ in range(10)]
        self.array_input.setPlainText(' '.join(map(str, arr)))
        self.reset_array()

    def reset_array(self):
        text = self.array_input.toPlainText().strip()
        try:
            arr = list(map(int, text.split()))
            self.visualizer.set_array(arr)
            self.log_text.clear()
            self.current_array = arr
            self.clear_code_highlight()
        except:
            self.log_text.append("Ошибка: введите целые числа через пробел")

    def start_sorting(self):
        text = self.array_input.toPlainText().strip()
        try:
            arr = list(map(int, text.split()))
        except:
            self.log_text.append("Ошибка ввода массива")
            return
        algo_name = self.algo_combo.currentText()
        if algo_name not in self.algorithms:
            return
        algo_class, _ = self.algorithms[algo_name]
        self.current_solver = algo_class(arr)
        self.current_generator = self.current_solver.run()
        self.visualizer.set_array(arr)
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
            if len(result) == 5:
                new_arr, msg, idx1, idx2, line_num = result
                if line_num != -1:
                    self.highlight_code_line(line_num)
            else:
                new_arr, msg, idx1, idx2 = result
            self.visualizer.set_array(new_arr)
            self.visualizer.set_highlight(idx1, idx2)
            self.log_text.append(msg)
            self.log_text.ensureCursorVisible()
        except StopIteration:
            self.stop_sorting()
            if self.loop_cb.isChecked():
                self.start_sorting()

    def stop_sorting(self):
        if self.current_solver:
            self.current_solver.stop()
        self.step_timer.stop()
        self.current_generator = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
