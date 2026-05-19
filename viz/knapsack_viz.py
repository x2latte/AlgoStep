import tkinter as tk

class KnapsackCanvas(tk.Canvas):
    def __init__(self, parent, width=400, height=250, **kwargs):
        super().__init__(parent, width=width, height=height, bg='#fef9e6', bd=2, relief='groove', **kwargs)
        self.capacity = 0
        self.items = []
        self.taken = []
        self.current_weight = 0
        self.current_value = 0

    def set_problem(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.taken = [False]*len(items)
        self.current_weight = 0
        self.current_value = 0
        self.redraw()

    def update_state(self, taken, current_weight, current_value):
        self.taken = taken.copy() if taken else [False]*len(self.items)
        self.current_weight = current_weight
        self.current_value = current_value
        self.redraw()

    def redraw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return
        bag_x0, bag_y0 = 20, 20
        bag_w = w//2 - 30
        bag_h = h - 60
        bag_x1 = bag_x0 + bag_w
        bag_y1 = bag_y0 + bag_h
        self.create_rectangle(bag_x0, bag_y0, bag_x1, bag_y1, outline='#8B5A2B', fill='#FDF5E6', width=3)
        self.create_text((bag_x0+bag_x1)//2, bag_y0-8, text="🎒 РЮКЗАК", font=('Arial',12,'bold'))
        fill_ratio = min(1.0, self.current_weight / self.capacity) if self.capacity>0 else 0
        fill_h = int(bag_h * fill_ratio)
        if fill_h>0:
            self.create_rectangle(bag_x0, bag_y1-fill_h, bag_x1, bag_y1, fill='#A5D6A5', outline='')
        self.create_text((bag_x0+bag_x1)//2, bag_y1+10, text=f"Вес: {self.current_weight}/{self.capacity}  |  Ценность: {self.current_value}", font=('Arial',9))
        items_x = bag_x1 + 20
        items_y = bag_y0
        for i, it in enumerate(self.items):
            color = '#C8E6C9' if self.taken[i] else '#FFCDD2'
            self.create_rectangle(items_x, items_y, items_x+120, items_y+30, fill=color, outline='black')
            self.create_text(items_x+60, items_y+15, text=f"{it.name} ({it.weight},{it.value})", font=('Arial',8))
            items_y += 35
            if items_y > bag_y1-30:
                items_y = bag_y0
                items_x += 130
        self.update()
