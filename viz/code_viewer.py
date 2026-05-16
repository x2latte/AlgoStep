import tkinter as tk
from tkinter import ttk
import re

class CodeViewer(tk.Frame):
    def __init__(self, parent, code_text="", **kwargs):
        super().__init__(parent, **kwargs)
        self.code_text = code_text
        self.lines = code_text.split('\n')
        self.current_line = -1
        
        self.text = tk.Text(self, wrap=tk.NONE, font=('Courier', 10), bg='#1e1e1e', fg='#d4d4d4')
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(self, command=self.text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scroll.set)
        
        self.update_code(code_text)
        self.text.tag_configure("current_line", background="#264f78", foreground="white")
        self.text.tag_configure("keyword", foreground="#569cd6")
        self.text.tag_configure("comment", foreground="#6a9955")
        self.text.tag_configure("string", foreground="#ce9178")
        
        self.highlight_syntax()
    
    def update_code(self, code_text):
        self.text.delete(1.0, tk.END)
        lines = code_text.split('\n')
        for i, line in enumerate(lines, 1):
            self.text.insert(tk.END, f"{i:3}  {line}\n")
        self.lines = lines
        self.highlight_syntax()
    
    def highlight_syntax(self):
        keywords = ['int', 'for', 'if', 'else', 'while', 'return', 'break', 'continue', 'void', 'bool', 'true', 'false', 'swap']
        for kw in keywords:
            start = "1.0"
            while True:
                pos = self.text.search(rf'\m{kw}\M', start, tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(kw)}c"
                self.text.tag_add("keyword", pos, end)
                start = end
    
    def highlight_line(self, line_num):
        self.text.tag_remove("current_line", "1.0", tk.END)
        if line_num >= 1 and line_num <= len(self.lines):
            start = f"{line_num}.0"
            end = f"{line_num}.end"
            self.text.tag_add("current_line", start, end)
            self.text.see(start)
