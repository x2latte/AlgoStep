import tkinter as tk

class SortingCanvas(tk.Canvas):
    def __init__(self, parent, width=600, height=300, **kwargs):
        super().__init__(parent, width=width, height=height, bg='#2c3e50', bd=2, relief='flat', **kwargs)
        self.width = width
        self.height = height
        self.values = []
        self.margin_left = 40
        self.margin_right = 40
        self.animate = True
        self.animation_speed = 10
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
        if not self.values:
            return
        n = len(self.values)
        available_width = self.width - self.margin_left - self.margin_right
        bar_width = max(2, available_width / n)
        max_val = max(self.values) if self.values else 1
        base_y = self.height - 30
        for i, val in enumerate(self.values):
            x0 = self.margin_left + i * bar_width
            x1 = x0 + bar_width - 1
            bar_height = (val / max_val) * (self.height - 60)
            y0 = base_y - bar_height
            y1 = base_y
            color = '#4a90e2'
            if highlight_indices:
                if i == highlight_indices[0]:
                    color = '#ff6b6b'
                elif len(highlight_indices) > 1 and i == highlight_indices[1]:
                    color = '#ffb347'
            self.create_rectangle(x0, y0, x1, y1, fill=color, outline='white', width=1)
            if bar_width > 12:
                self.create_text((x0+x1)//2, y0-5, text=str(val), fill='white', font=('Arial',8,'bold'))
        self.update()

    def animate_swap(self, idx1, idx2, callback=None):
        self.values[idx1], self.values[idx2] = self.values[idx2], self.values[idx1]
        self.draw(highlight_indices=(idx1, idx2))
        if callback:
            callback()

    def update_state(self, new_values, highlight_idx1=None, highlight_idx2=None):
        self.values = new_values[:]
        if highlight_idx1 is not None:
            self.draw(highlight_indices=(highlight_idx1, highlight_idx2) if highlight_idx2 is not None else (highlight_idx1,))
        else:
            self.draw()
