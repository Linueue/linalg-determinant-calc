import tkinter as tk
from tkinter import ttk
import sys

FONT = ("Consolas", )

class Window(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ttk.Label(self, text="Determinant Calculator")
        label.pack()
        label.bind("<1>", self.quit)

    def quit(self, _=None):
        sys.exit()

root = tk.Tk()
root.tk.call("tk", "scaling", 1.25)
style = ttk.Style()
root.geometry("800x600")
style.configure("TLabel", font=(*FONT, 25))
Window(root).pack()
root.mainloop()
