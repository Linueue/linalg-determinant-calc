import tkinter as tk
import customtkinter as ctk
import numpy as np
from determinant import determinant_cofactor

FONT_NAME = "TkDefaultFont"
MAX_MATRIX_SIZE = 10

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand=True, fill="both")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.font = ctk.CTkFont(
            family=FONT_NAME,
            size=16,
        )
        self.title_font = ctk.CTkFont(
            family=FONT_NAME,
            size=23,
        )

        self.matrix_size = 3
        self.entries = []

        print(tk.font.families())

        self.build_ui()

    def num_callback(self, P):
        return P.isdigit() or P == "" or (P.count("/") == 1) or (P.count(".") == 1)

    def focus_next_entry(self, i, j):
        next_i = i
        next_j = j + 1
        if next_j % self.matrix_size == 0:
            next_i += 1
            next_j = 0

        if next_i >= self.matrix_size:
            return

        self.entries[next_i][next_j].focus_set()

    def build_matrix(self):
        vcmd = (self.register(self.num_callback), "%P")

        for i in range(MAX_MATRIX_SIZE):
            entries = []

            for j in range(MAX_MATRIX_SIZE):
                entry = ctk.CTkEntry(
                    self.matrix_frame,
                    width=50,
                    validate="key",
                    validatecommand=vcmd,
                )
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.bind("<Return>", lambda e, i=i, j=j: self.focus_next_entry(i, j))
                entry.insert(0, "0")
                entries.append(entry)

            self.entries.append(entries)

    def on_size_change(self, sv):
        if not sv.get():
            return

        self.matrix_size = int(sv.get())
        
        for i in range(MAX_MATRIX_SIZE):
            for j in range(MAX_MATRIX_SIZE):
                if i >= self.matrix_size or j >= self.matrix_size:
                    self.entries[i][j].delete(0, "end")
                    self.entries[i][j].insert(0, "0")
                    self.entries[i][j].grid_forget()
                    continue
                self.entries[i][j].grid(row=i, column=j, padx=5, pady=5)
    
    def parse(self, v):
        a = ""
        b = ""

        is_fraction = False

        for c in v:
            if is_fraction:
                b += c
                continue
            if c == "/":
                is_fraction = True
                continue
            a += c

        if is_fraction:
            return float(a) / float(b)

        return a

    def calculate(self):
        n = self.matrix_size
        mat = np.identity(n)

        for i in range(n):
            for j in range(n):
                value = self.entries[i][j].get()

                if not value or (value and value[-1] == "/"):
                    print("ERROR - HANDLE THIS")
                    return

                mat[i, j] = self.parse(value)

        det = determinant_cofactor(mat)

        print(mat)
        print(det)

    def build_ui(self):
        label = ctk.CTkLabel(
            self.frame,
            text="Determinant",
            font=self.title_font,
            justify=ctk.LEFT
        )
        label.grid(row=0, padx=20, pady=10, sticky="nw")
        
        input_frame = ctk.CTkFrame(self.frame)
        input_frame.grid(row=1, padx=20, pady=(0, 20), sticky="nsew")
        input_frame.columnconfigure(8, weight=1)
        input_frame.rowconfigure(1, weight=1)

        size_input_label = ctk.CTkLabel(
            input_frame,
            text="n =",
            font=self.font
        )
        size_input_label.grid(
            row=0,
            column=0,
            padx=(15, 10),
            pady=10
        )

        def callback_size(P):
            return (P.isdigit() and int(P) <= 10) or P == ""

        vcmd = (self.register(callback_size), "%P")

        text_size_var = tk.StringVar()
        text_size_var.trace_add("write", lambda *args: self.on_size_change(text_size_var))

        size_input = ctk.CTkEntry(
            input_frame,
            width=50,
            font=self.font,
            validate="key",
            validatecommand=vcmd,
            textvariable=text_size_var
        )
        size_input.grid(row=0, column=1, padx=0, pady=10)

        size_hint_label = ctk.CTkLabel(
            input_frame,
            text="(n <= 10)",
            font=self.font,
            text_color=("gray50", "gray60")
        )
        size_hint_label.grid(row=0, column=2, padx=(10, 10), pady=10)

        self.matrix_frame = ctk.CTkFrame(
            input_frame,
            fg_color="transparent"
        )
        self.matrix_frame.grid(row=1, columnspan=10, padx=10, pady=(0, 10), sticky="n")
        self.build_matrix()

        size_input.insert(0, "3")

        button = ctk.CTkButton(
            input_frame,
            text="Calculate",
            width=100,
            font=self.font,
            command=self.calculate,
        )
        button.grid(row=2, columnspan=10, padx=10, pady=10, ipadx=10, ipady=5, sticky="n")

app = App()
app.mainloop()
