import tkinter as tk
import math

class GraphCanvas(tk.Canvas):
    def __init__(self, parent, width=500, height=400, **kwargs):
        super().__init__(parent, width=width, height=height, bd=2, relief='sunken', bg='white', **kwargs)
        self.graph = {}
        self.vertex_positions = {}
        self.radius = 20
        self.highlighted_vertices = set()
        self.highlighted_edges = set()
        self.path = []
        self.n = 0
        self.bind("<Configure>", self.on_resize)

    def set_graph(self, graph, n_vertices):
        self.graph = graph
        self.n = n_vertices
        self.layout_circle()
        self.redraw()

    def layout_circle(self):
        if self.n == 0:
            return
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 50 or h < 50:
            w, h = 500, 400
        center_x = w//2
        center_y = h//2
        rad = min(center_x, center_y) - 50
        self.vertex_positions.clear()
        for i in range(self.n):
            angle = 2*math.pi*i/self.n
            x = center_x + rad*math.cos(angle)
            y = center_y + rad*math.sin(angle)
            self.vertex_positions[i] = (x,y)

    def highlight_vertex(self, v, color='lightgreen'):
        self.highlighted_vertices.add((v, color))
        self.redraw()

    def highlight_edge(self, u, v, color='red'):
        self.highlighted_edges.add((u,v,color))
        self.redraw()

    def set_path(self, path):
        self.path = path
        self.redraw()

    def clear_highlights(self):
        self.highlighted_vertices.clear()
        self.highlighted_edges.clear()
        self.path = []
        self.redraw()

    def on_resize(self, event):
        self.layout_circle()
        self.redraw()

    def redraw(self):
        self.delete("all")
        if not self.vertex_positions:
            return
        # Рёбра
        for u in self.graph:
            if u not in self.vertex_positions:
                continue
            x1,y1 = self.vertex_positions[u]
            for v,w in self.graph[u]:
                if v not in self.vertex_positions:
                    continue
                x2,y2 = self.vertex_positions[v]
                color = '#555555'
                width = 2
                if (u,v,'red') in self.highlighted_edges or (v,u,'red') in self.highlighted_edges:
                    color = '#E63946'
                    width = 4
                elif self.path and u in self.path and v in self.path and abs(self.path.index(u)-self.path.index(v))==1:
                    color = '#1E88E5'
                    width = 4
                self.create_line(x1,y1,x2,y2, fill=color, width=width, arrow=tk.LAST, arrowshape=(8,10,5))
                # Позиция для текста веса – смещённая от середины перпендикулярно
                mx, my = (x1+x2)/2, (y1+y2)/2
                dx, dy = x2-x1, y2-y1
                length = math.hypot(dx, dy)
                if length > 0:
                    offset = 15
                    nx = -dy/length * offset
                    ny = dx/length * offset
                    mx += nx
                    my += ny
                # Создаём текст без фона (bg не поддерживается, используем fill)
                self.create_text(mx, my, text=str(w), fill='#1A1A1A', font=('Arial',12,'bold'))
        # Вершины
        for i,(x,y) in self.vertex_positions.items():
            fill = '#FFB6C1'
            for (v,col) in self.highlighted_vertices:
                if v==i:
                    fill = col
            if self.path and i in self.path:
                fill = '#90EE90'
            self.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill=fill, outline='#2C3E50', width=2)
            self.create_text(x, y, text=str(i), font=('Arial',12,'bold'), fill='black')
        self.update()
