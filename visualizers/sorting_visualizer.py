from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QFont

class SortingVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.array = []
        self.highlight1 = -1
        self.highlight2 = -1
        self.setMinimumHeight(300)

    def set_array(self, arr):
        self.array = arr[:] if arr else []
        self.highlight1 = -1
        self.highlight2 = -1
        self.update()

    def set_highlight(self, i1, i2):
        self.highlight1 = i1
        self.highlight2 = i2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        if not self.array or len(self.array) == 0:
            painter.drawText(QRectF(0, 0, w, h), Qt.AlignmentFlag.AlignCenter, "Нет данных")
            return
        n = len(self.array)
        max_val = max(self.array)
        if max_val == 0:
            max_val = 1
        margin = 40
        bar_width = (w - 2*margin) / n
        base_y = h - 30
        for i, val in enumerate(self.array):
            x0 = margin + i * bar_width
            bar_height = (val / max_val) * (h - 60)
            y0 = base_y - bar_height
            color = QColor(74, 144, 226)
            if i == self.highlight1:
                color = QColor(255, 107, 107)
            elif i == self.highlight2:
                color = QColor(255, 179, 71)
            painter.fillRect(QRectF(x0, y0, bar_width-1, bar_height), color)
            painter.setPen(Qt.GlobalColor.white)
            painter.setFont(QFont("Arial", 8))
            painter.drawText(QRectF(x0, y0-15, bar_width-1, 15), Qt.AlignmentFlag.AlignCenter, str(val))
