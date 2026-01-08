import tkinter as tk
import customtkinter as ctk

FONT_NAME = ("Consolas", "Menlo", "Arial")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand=True, fill="both")
        self.font = ctk.CTkFont(
            family=FONT_NAME,
            size=16,
        )

        self.build_ui()

    def build_ui(self):
        self.font.configure(size=20)
        label = ctk.CTkLabel(self.frame, text="Determinant Calculator", font=self.font)
        label.pack(padx=20, pady=20)

app = App()
# root.tk.call("tk", "scaling", 1.25)
app.mainloop()
