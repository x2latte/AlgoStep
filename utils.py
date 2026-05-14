import tkinter as tk
import time

def safe_callback(widget, func, *args):
    """Вызывает func только если виджет существует"""
    if widget and widget.winfo_exists():
        func(*args)
    else:
        # Попытка найти родительское окно
        try:
            root = widget.winfo_toplevel()
            if root.winfo_exists():
                func(*args)
        except:
            pass

def step_delay(step_mode, delay=0.3):
    if step_mode:
        time.sleep(delay)
