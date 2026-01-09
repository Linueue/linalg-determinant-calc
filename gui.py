import tkinter as tk
import customtkinter as ctk

FONT_NAME = "Arial"

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

        self.build_ui()

    def num_callback(self, P):
        return P.isdigit() or P == "" or (P.count("/") == 1) or (P.count(".") == 1)

    def on_size_change(self, sv):
        if not sv.get():
            return

        self.matrix_size = int(sv.get())

        vcmd = (self.register(self.num_callback), "%P")

        for entry in self.matrix_frame.winfo_children():
            entry.destroy()

        self.entries.clear()
        
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                entry = ctk.CTkEntry(
                    self.matrix_frame,
                    width=50,
                    validate="key",
                    validatecommand=vcmd,
                )
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, "0")
                self.entries.append(entry)

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
        self.matrix_frame.grid(row=1, columnspan=10, padx=10, pady=(0, 10), sticky="nsew")

        size_input.insert(0, "3")

app = App()
app.mainloop()
