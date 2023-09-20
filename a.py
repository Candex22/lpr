import pathlib
import sys
import tkinter as tk
from tkinter import ttk
class TextFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.text = tk.Text(
            self,
            xscrollcommand=self.hscrollbar.set,
            yscrollcommand=self.vscrollbar.set,
            wrap=tk.NONE
        )
        self.hscrollbar.config(command=self.text.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscrollbar.config(command=self.text.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack()
root = tk.Tk()
root.geometry("400x300")
text_frame = TextFrame()
text_frame.text.insert(
    "1.0",
    # Si no funciona, cambiar por la ruta de algún archivo de texto largo.
)
text_frame.pack()
root.mainloop()