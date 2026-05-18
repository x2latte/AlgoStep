from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QPolygonF
import math

class GraphVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.graph = {}
        self.n = 0
        self.vertex_positions = {}
        self.radius = 25
        self.highlighted_vertices = set()
        self.highlighted_edges = set()
        self.path = []
        self.setMinimumHeight(400)

    def set_graph(self, graph, n):
        self.graph = graph
        self.n = n
        self.layout_circle()
        self.clear_highlights()
        self.update()

    def layout_circle(self):
        w = self.width()
        h = self.height()
        if w == 0 or h == 0:
            w, h = 800, 600
        center_x = w / 2
        center_y = h / 2
        rad = min(center_x, center_y) - 60
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n
            x = center_x + rad * math.cos(angle)
            y = center_y + rad * math.sin(angle)
            self.vertex_positions[i] = QPointF(x, y)

    def clear_highlights(self):
        self.highlighted_vertices.clear()
        self.highlighted_edges.clear()
        self.path = []
        self.update()

    def highlight_vertex(self, v, color):
        self.highlighted_vertices.add((v, color))
        self.update()

    def highlight_edge(self, u, v, color):
        self.highlighted_edges.add((u, v, color))
        self.update()

    def set_path(self, path):
        self.path = path
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.vertex_positions:
            return
        # Рисуем рёбра
        for u, edges in self.graph.items():
            if u not in self.vertex_positions:
                continue
            p1 = self.vertex_positions[u]
            for v, w in edges:
                if v not in self.vertex_positions:
                    continue
                p2 = self.vertex_positions[v]
                # Определяем цвет и толщину
                if self.path and u in self.path and v in self.path and abs(self.path.index(u)-self.path.index(v))==1:
                    color = Qt.GlobalColor.blue
                    pen_width = 4
                elif (u, v, 'red') in self.highlighted_edges or (v, u, 'red') in self.highlighted_edges:
                    color = Qt.GlobalColor.red
                    pen_width = 4
                else:
                    color = Qt.GlobalColor.gray
                    pen_width = 2
                painter.setPen(QPen(color, pen_width))
                painter.drawLine(p1, p2)
                # Рисуем стрелку
                angle = math.atan2(p2.y() - p1.y(), p2.x() - p1.x())
                arrow_size = 10
                arrow_p1 = p2 - QPointF(arrow_size * math.cos(angle - math.pi/6), arrow_size * math.sin(angle - math.pi/6))
                arrow_p2 = p2 - QPointF(arrow_size * math.cos(angle + math.pi/6), arrow_size * math.sin(angle + math.pi/6))
                painter.drawPolygon(QPolygonF([p2, arrow_p1, arrow_p2]))
                # Вес ребра
                mx = (p1.x() + p2.x()) / 2
                my = (p1.y() + p2.y()) / 2
                painter.setPen(Qt.GlobalColor.black)
                painter.setFont(QFont("Arial", 10))
                painter.drawText(QRectF(mx-10, my-10, 20, 20), Qt.AlignmentFlag.AlignCenter, str(w))
        # Рисуем вершины
        for i, pos in self.vertex_positions.items():
            fill_color = QColor(255, 182, 193)  # розовый
            for (v, col) in self.highlighted_vertices:
                if v == i:
                    fill_color = QColor(col)
            if self.path and i in self.path:
                fill_color = QColor(144, 238, 144)  # салатовый для пути
            painter.setBrush(fill_color)
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.drawEllipse(pos, self.radius, self.radius)
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(QRectF(pos.x()-10, pos.y()-10, 20, 20), Qt.AlignmentFlag.AlignCenter, str(i))
