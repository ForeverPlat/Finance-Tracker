import customtkinter as ctk
from settings import FONT, MAIN_TEXT_SIZE, ENTRY_TEXT_SIZE, GREEN, RED, WHITE, BG, BUTTON_COLOR, BUTTON_HOVER, FOREGROUND_COLOR


class App(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        self.db = db

        self.title("Finance Tracker v2")
        self.geometry("300x300")
        self.configure(fg_color=BG)
        self.resizable(False, False)

        self.total_label = ctk.CTkLabel(
            self, text=f"Balance: ${db.get_current_total():.2f}",
            font=ctk.CTkFont(FONT, MAIN_TEXT_SIZE), text_color=WHITE
        )
        self.total_label.pack(pady=20)

        self.entry = ctk.CTkEntry(
            self, font=ctk.CTkFont(FONT, ENTRY_TEXT_SIZE),
            text_color=WHITE, fg_color=FOREGROUND_COLOR
        )
        self.entry.pack(pady=10)

        self.add_button = ctk.CTkButton(
            self, text="+", text_color=GREEN, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER,
            command=self.add_money
        )
        self.add_button.pack(pady=5)

        self.sub_button = ctk.CTkButton(
            self, text="-", text_color=RED, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER,
            command=self.subtract_money
        )
        self.sub_button.pack()

    def add_money(self):
        try:
            amount = float(self.entry.get())
        except:
            return
        new_total = self.db.add_transaction(amount, "Add", "")
        self.total_label.configure(text=f"Balance: ${new_total:.2f}")

    def subtract_money(self):
        try:
            amount = float(self.entry.get())
        except:
            return
        new_total = self.db.add_transaction(-amount, "Subtract", "")
        self.total_label.configure(text=f"Balance: ${new_total:.2f}")
