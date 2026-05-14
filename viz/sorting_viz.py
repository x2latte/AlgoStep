import tkinter as tk
import time

class SortingCanvas(tk.Canvas):
    def __init__(self, parent, width=600, height=300, **kwargs):
        super().__init__(parent, width=width, height=height, bg='#2c3e50', bd=2, relief='flat', **kwargs)
        self.width = width
        self.height = height
        self.values = []
        self.bars = []
        self.bar_heights = []
        self.bar_x0 = []
        self.margin_left = 40
        self.margin_right = 40
        self.animate = True
        self.animation_speed = 0.05
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.draw()

    def set_animation(self, enabled):
        self.animate = enabled

    def set_data(self, values):
        self.values = values[:]
        self.draw()

    def draw(self, highlight_indices=None):
        self.delete("all")
        self.bars = []
        if not self.values:
            return
        n = len(self.values)
        if n == 0:
            return
        available_width = self.width - self.margin_left - self.margin_right
        bar_width = available_width / n
        max_val = max(self.values) if self.values else 1
        base_y = self.height - 30
        self.bar_heights = []
        self.bar_x0 = []
        for i, val in enumerate(self.values):
            x0 = self.margin_left + i * bar_width
            x1 = x0 + bar_width - 2
            bar_height = (val / max_val) * (self.height - 60)
            y0 = base_y - bar_height
            y1 = base_y
            color = '#4a90e2'
            if highlight_indices:
                if i == highlight_indices[0]:
                    color = '#ff6b6b'
                elif len(highlight_indices) > 1 and i == highlight_indices[1]:
                    color = '#ffb347'
            rect = self.create_rectangle(x0, y0, x1, y1, fill=color, outline='white', width=1)
            self.bars.append(rect)
            self.bar_heights.append(bar_height)
            self.bar_x0.append(x0)
            if bar_width > 12:
                self.create_text((x0+x1)//2, y0-5, text=str(val), fill='white', font=('Arial',9,'bold'))
        self.update()

    def animate_swap(self, idx1, idx2, callback_after=None):
        if not self.animate or idx1 == idx2 or idx1 < 0 or idx2 < 0:
            self.values[idx1], self.values[idx2] = self.values[idx2], self.values[idx1]
            self.draw()
            if callback_after:
                callback_after()
            return
        val1, val2 = self.values[idx1], self.values[idx2]
        x01, x02 = self.bar_x0[idx1], self.bar_x0[idx2]
        bar_width = x02 - x01 if idx2 > idx1 else x01 - x02
        steps = 10
        for step in range(1, steps+1):
            t = step / steps
            new_x1 = x01 + (x02 - x01) * t
            new_x2 = x02 + (x01 - x02) * t
            self.coords(self.bars[idx1], new_x1, self.get_y0(idx1), new_x1+bar_width, self.get_y1(idx1))
            self.coords(self.bars[idx2], new_x2, self.get_y0(idx2), new_x2+bar_width, self.get_y1(idx2))
            self.update()
            time.sleep(self.animation_speed / steps)
        self.values[idx1], self.values[idx2] = val2, val1
        self.draw()
        if callback_after:
            callback_after()

    def get_y0(self, idx):
        base_y = self.height - 30
        return base_y - self.bar_heights[idx]

    def get_y1(self, idx):
        return self.height - 30

    def update_state(self, new_values, highlight_idx1=None, highlight_idx2=None):
        self.values = new_values[:]
        self.draw(highlight_indices=(highlight_idx1, highlight_idx2) if highlight_idx2 is not None else (highlight_idx1,))
