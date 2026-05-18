from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen

class KnapsackVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.items = []
        self.taken = []
        self.capacity = 0
        self.current_weight = 0
        self.current_value = 0
        self.setMinimumHeight(300)

    def set_problem(self, items, capacity):
        self.items = items
        self.capacity = capacity
        self.taken = [False] * len(items)
        self.current_weight = 0
        self.current_value = 0
        self.update()

    def update_state(self, taken, current_weight, current_value):
        self.taken = taken[:] if taken else [False]*len(self.items)
        self.current_weight = current_weight
        self.current_value = current_value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        # Рисуем рюкзак
        bag_x0 = 20
        bag_y0 = 20
        bag_w = w//2 - 30
        bag_h = h - 60
        bag_x1 = bag_x0 + bag_w
        bag_y1 = bag_y0 + bag_h
        painter.fillRect(QRectF(bag_x0, bag_y0, bag_w, bag_h), QColor(253, 245, 230))
        painter.setPen(QPen(Qt.GlobalColor.darkRed, 3))
        painter.drawRect(QRectF(bag_x0, bag_y0, bag_w, bag_h))
        painter.drawText(QRectF(bag_x0, bag_y0-20, bag_w, 20), Qt.AlignmentFlag.AlignCenter, "Рюкзак")
        # Заливка заполненности
        fill_ratio = min(1.0, self.current_weight / self.capacity) if self.capacity > 0 else 0
        fill_h = int(bag_h * fill_ratio)
        if fill_h > 0:
            painter.fillRect(QRectF(bag_x0, bag_y1-fill_h, bag_w, fill_h), QColor(165, 214, 165))
        # Текст веса/ценности
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(QRectF(bag_x0, bag_y1+5, bag_w, 20), Qt.AlignmentFlag.AlignCenter,
                         f"Вес: {self.current_weight}/{self.capacity} | Ценность: {self.current_value}")
        # Список предметов справа
        items_x = bag_x1 + 15
        items_y = bag_y0
        item_h = 40
        item_w = 140
        for i, it in enumerate(self.items):
            color = QColor(200, 230, 201) if self.taken[i] else QColor(255, 205, 210)
            painter.fillRect(QRectF(items_x, items_y, item_w, item_h), color)
            painter.drawRect(QRectF(items_x, items_y, item_w, item_h))
            text = f"{'✓ ' if self.taken[i] else ''}{it.name} ({it.weight},{it.value})"
            painter.drawText(QRectF(items_x, items_y, item_w, item_h), Qt.AlignmentFlag.AlignCenter, text)
            items_y += item_h + 5
            if items_y + item_h > bag_y1:
                items_y = bag_y0
                items_x += item_w + 10
