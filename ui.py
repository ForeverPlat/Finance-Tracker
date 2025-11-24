import customtkinter as ctk
from settings import *


class App(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        self.db = db

        # ---- global CTk config ----
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Finance Tracker")
        self.geometry("460x675")
        self.configure(fg_color=BG)
        self.resizable(False, False)

        # State
        self.mode = None         # "add" or "sub"
        self.category = None     # string

        # Build UI
        self._build_header()
        self._build_amount_panel()
        self._build_category_panel()
        self._build_comment_panel()
        self._build_save_panel()

        self._refresh_total()

    # UI SECTIONS
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=BG)
        header.pack(fill="x", pady=(25, 0))

        self.total_label = ctk.CTkLabel(
            header,
            text="Balance: $0.00",
            font=ctk.CTkFont(FONT, MAIN_TEXT_SIZE, "bold"),
            text_color=ACCENT,
        )
        self.total_label.pack()

        self.status_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(FONT, SUB_TEXT_SIZE),
            text_color=MUTED,
        )
        self.status_label.pack(pady=(2, 0))

    def _build_amount_panel(self):
        panel = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=12)
        panel.pack(fill="x", padx=20, pady=10)

        self.amount_label = ctk.CTkLabel(
            panel,
            text="1) Enter amount",
            font=ctk.CTkFont(FONT, SUB_TEXT_SIZE, "bold"),
            text_color=WHITE,
        )
        self.amount_label.pack(anchor="w", padx=12, pady=(10, 0))

        self.amount_entry = ctk.CTkEntry(
            panel,
            height=40,
            font=ctk.CTkFont(FONT, ENTRY_TEXT_SIZE),
            fg_color="#111315",
            text_color=WHITE,
        )
        self.amount_entry.pack(fill="x", padx=12, pady=8)

        # mode buttons: Add / Subtract
        mode_frame = ctk.CTkFrame(panel, fg_color="transparent")
        mode_frame.pack(pady=(4, 10))

        self.add_button = ctk.CTkButton(
            mode_frame,
            text="Add",
            width=120,
            fg_color=GREEN,
            text_color="black",
            font=ctk.CTkFont(FONT, BUTTON_TEXT_SIZE, "bold"),
            command=lambda: self._set_mode("add"),
        )
        self.add_button.pack(side="left", padx=8)

        self.sub_button = ctk.CTkButton(
            mode_frame,
            text="Subtract",
            width=120,
            fg_color=RED,
            text_color="black",
            font=ctk.CTkFont(FONT, BUTTON_TEXT_SIZE, "bold"),
            command=lambda: self._set_mode("sub"),
        )
        self.sub_button.pack(side="left", padx=8)

    def _build_category_panel(self):
        panel = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=12)
        panel.pack(fill="x", padx=20, pady=10)

        label = ctk.CTkLabel(
            panel,
            text="2) Choose category",
            font=ctk.CTkFont(FONT, SUB_TEXT_SIZE, "bold"),
            text_color=WHITE,
        )
        label.pack(anchor="w", padx=12, pady=(10, 0))

        self.category_frame = ctk.CTkFrame(panel, fg_color="transparent")
        self.category_frame.pack(padx=8, pady=8)

        self.category_buttons = {}
        categories = [
            "Work", "Allowance", "Gifts",
            "Food", "School", "Clothes",
            "Other",
        ]

        for i, cat in enumerate(categories):
            btn = ctk.CTkButton(
                self.category_frame,
                text=cat,
                width=120,
                fg_color=ACCENT,
                text_color="black",
                font=ctk.CTkFont(FONT, BUTTON_TEXT_SIZE),
                command=lambda c=cat: self._set_category(c),
            )
            btn.grid(row=i // 2, column=i % 2, padx=6, pady=4)
            self.category_buttons[cat] = btn

    def _build_comment_panel(self):
        panel = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=12)
        panel.pack(fill="x", padx=20, pady=10)

        label = ctk.CTkLabel(
            panel,
            text="3) Comment (optional, letters & numbers only)",
            font=ctk.CTkFont(FONT, SUB_TEXT_SIZE, "bold"),
            text_color=WHITE,
        )
        label.pack(anchor="w", padx=12, pady=(10, 0))

        self.comment_entry = ctk.CTkEntry(
            panel,
            height=40,
            font=ctk.CTkFont(FONT, SUB_TEXT_SIZE),
            fg_color="#111315",
            text_color=WHITE,
        )
        self.comment_entry.pack(fill="x", padx=12, pady=8)

        # Live filter: allow only [A-Za-z0-9 ] and max length 40
        self.comment_entry.bind("<KeyRelease>", self._filter_comment)

    def _build_save_panel(self):
        panel = ctk.CTkFrame(self, fg_color=BG)
        panel.pack(pady=16)

        self.save_button = ctk.CTkButton(
            panel,
            text="4) Save transaction",
            width=220,
            height=46,
            fg_color=ACCENT,
            text_color="black",
            font=ctk.CTkFont(FONT, BUTTON_TEXT_SIZE, "bold"),
            command=self._save_transaction,
        )
        self.save_button.pack()

    # STATE / LOGIC
    def _refresh_total(self):
        total = self.db.get_current_total()
        self.total_label.configure(text=f"Balance: ${total:.2f}")

    def _set_mode(self, mode: str):
        self.mode = mode

        # visual feedback
        if mode == "add":
            self.add_button.configure(fg_color=GREEN)
            self.sub_button.configure(fg_color="#444444")
        else:
            self.sub_button.configure(fg_color=RED)
            self.add_button.configure(fg_color="#444444")

        self.status_label.configure(text=f"Mode: {mode.capitalize()}")

    def _set_category(self, category: str):
        self.category = category

        # highlight selected, reset others
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(fg_color=ACCENT)
            else:
                btn.configure(fg_color="#3a3f47")

        self.status_label.configure(text=f"Category: {category}")

    def _filter_comment(self, event=None):
        text = self.comment_entry.get()
        # keep only letters, numbers, space
        filtered = "".join(ch for ch in text if ch.isalnum() or ch.isspace())
        filtered = filtered[:40]  # max length 40

        if filtered != text:
            self.comment_entry.delete(0, "end")
            self.comment_entry.insert(0, filtered)

    def _save_transaction(self):
        # Clear previous status
        self.status_label.configure(text="", text_color=MUTED)

        # ammount is allowed
        raw_amount = self.amount_entry.get().strip()
        if not raw_amount:
            self._set_error("Enter an amount first.")
            return

        try:
            amount = float(raw_amount)
        except ValueError:
            self._set_error("Amount must be a valid number.")
            return

        if amount <= 0:
            self._set_error("Amount must be greater than zero.")
            return

        # Validate mode
        if self.mode not in ("add", "sub"):
            self._set_error("Choose Add or Subtract.")
            return

        # Validate category
        if not self.category:
            self._set_error("Choose a category.")
            return

        # prep signed amount
        signed_amount = amount if self.mode == "add" else -amount

        # sanitized comment
        comment = self.comment_entry.get().strip()
        # double-sanitize
        comment = "".join(ch for ch in comment if ch.isalnum() or ch.isspace())[:40]

        # save to DB
        new_total = self.db.add_transaction(signed_amount, self.category, comment)

        # Update UI, clear fields & state
        self._refresh_total()
        self.amount_entry.delete(0, "end")
        self.comment_entry.delete(0, "end")
        self.mode = None
        self.category = None

        # reset button colors
        self.add_button.configure(fg_color=GREEN)
        self.sub_button.configure(fg_color=RED)
        for btn in self.category_buttons.values():
            btn.configure(fg_color=ACCENT)

        self.status_label.configure(
            text=f"Saved {('+' if signed_amount >= 0 else '')}{signed_amount:.2f} {self.category or '(Unknown)'}",
            text_color=GREEN if signed_amount >= 0 else RED,
        )

    def _set_error(self, msg: str):
        self.status_label.configure(text=msg, text_color=RED)
