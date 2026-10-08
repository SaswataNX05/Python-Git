import random
import customtkinter as ctk

# Configure theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NumberGuessingGame(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Number Guessing Game")
        self.geometry("420x460")
        self.resizable(False, False)

        # Game Configuration
        self.min_val = 1
        self.max_val = 100
        self.max_lives = 7

        # Game State
        self.target_number = 0
        self.lives_left = self.max_lives
        self.history = []

        self._build_ui()
        self.start_new_game()

    def _build_ui(self):
        # 1. Top Bar: Mode and Lives
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=25, pady=(20, 10))

        self.mode_label = ctk.CTkLabel(
            self.top_frame,
            text=f"Mode: 1-{self.max_val}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#A0AEC0",
        )
        self.mode_label.pack(side="left")

        self.lives_label = ctk.CTkLabel(
            self.top_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#F56565",
        )
        self.lives_label.pack(side="right")

        # 2. Input Field
        self.guess_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter your guess...",
            font=ctk.CTkFont(size=16),
            height=45,
            justify="center",
            corner_radius=10,
        )
        self.guess_entry.pack(fill="x", padx=25, pady=(5, 10))
        self.guess_entry.bind("<Return>", lambda e: self.check_guess())

        # 3. Submit / Action Button
        self.action_button = ctk.CTkButton(
            self,
            text="SUBMIT GUESS ↵",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#B8860B",
            hover_color="#996515",
            command=self.check_guess,
        )
        self.action_button.pack(fill="x", padx=25, pady=(0, 15))

        # 4. Result Card
        self.result_card = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color="#1E293B",
            border_width=2,
            border_color="#334155",
        )
        self.result_card.pack(fill="x", padx=25, pady=5, ipady=12)

        # Proximity Hint Badge
        self.badge_label = ctk.CTkLabel(
            self.result_card,
            text="GUESS TO START",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#38BDF8",
            corner_radius=6,
            fg_color="#0F172A",
            padx=10,
            pady=3,
        )
        self.badge_label.pack(pady=(5, 8))

        # Big Feedback Text
        self.feedback_label = ctk.CTkLabel(
            self.result_card,
            text="Make your first guess!",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F8FAFC",
        )
        self.feedback_label.pack(pady=(0, 5))

        # 5. Bottom Status / History
        self.history_label = ctk.CTkLabel(
            self,
            text="History: None",
            font=ctk.CTkFont(size=12),
            text_color="#94A3B8",
        )
        self.history_label.pack(side="bottom", pady=15)

    def start_new_game(self):
        """Resets the state for a fresh match."""
        self.target_number = random.randint(self.min_val, self.max_val)
        self.lives_left = self.max_lives
        self.history.clear()

        self.guess_entry.configure(state="normal")
        self.guess_entry.delete(0, "end")
        self.action_button.configure(
            text="SUBMIT GUESS ↵",
            command=self.check_guess,
            fg_color="#B8860B",
            hover_color="#996515",
        )

        self.badge_label.configure(
            text="GUESS TO START", text_color="#38BDF8", fg_color="#0F172A"
        )
        self.feedback_label.configure(text="Make your first guess!")
        self.result_card.configure(border_color="#334155")
        self.history_label.configure(text="History: None")
        self._update_lives_ui()

    def _update_lives_ui(self):
        hearts = "♥ " * self.lives_left
        self.lives_label.configure(
            text=f"{hearts} ({self.lives_left} lives left)"
        )

    def check_guess(self):
        raw_val = self.guess_entry.get().strip()

        # Validate input
        if not raw_val.isdigit():
            self.feedback_label.configure(text="Enter a positive number!")
            return

        guess = int(raw_val)
        if not (self.min_val <= guess <= self.max_val):
            self.feedback_label.configure(
                text=f"Must be between {self.min_val} and {self.max_val}!"
            )
            return

        # Deduct life & save to history
        self.lives_left -= 1
        delta = abs(guess - self.target_number)

        # Update History display
        suffix = (
            "H"
            if guess > self.target_number
            else ("L" if guess < self.target_number else "★")
        )
        self.history.append(f"{guess}{suffix}")
        self.history_label.configure(
            text=f"History: [{', '.join(self.history)}]"
        )

        self._update_lives_ui()
        self.guess_entry.delete(0, "end")

        # Win Condition
        if guess == self.target_number:
            self._handle_game_over(
                won=True,
                badge_text="CONGRATULATIONS!",
                badge_color="#22C55E",
                card_color="#15803D",
                feedback=f"{guess} IS CORRECT!",
            )
            return

        # Loss Condition
        if self.lives_left <= 0:
            self._handle_game_over(
                won=False,
                badge_text="GAME OVER",
                badge_color="#EF4444",
                card_color="#991B1B",
                feedback=f"Target was {self.target_number}",
            )
            return

        # Intermediate Proximity & Direction Hints
        direction = "TOO HIGH!" if guess > self.target_number else "TOO LOW!"
        self.feedback_label.configure(text=f"{guess} IS {direction}")

        if delta <= 5:
            self.badge_label.configure(
                text="HINT: BURNING HOT!",
                text_color="#F97316",
                fg_color="#431407",
            )
            self.result_card.configure(border_color="#EA580C")
        elif delta <= 15:
            self.badge_label.configure(
                text="HINT: GETTING WARM",
                text_color="#FBBF24",
                fg_color="#451A03",
            )
            self.result_card.configure(border_color="#D97706")
        else:
            self.badge_label.configure(
                text="HINT: COLD", text_color="#38BDF8", fg_color="#082F49"
            )
            self.result_card.configure(border_color="#0284C7")

    def _handle_game_over(
        self, won, badge_text, badge_color, card_color, feedback
    ):
        self.badge_label.configure(
            text=badge_text, text_color=badge_color, fg_color="#0F172A"
        )
        self.feedback_label.configure(text=feedback)
        self.result_card.configure(border_color=card_color)

        # Transition button to reset mode
        self.guess_entry.configure(state="disabled")
        self.action_button.configure(
            text="PLAY AGAIN",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.start_new_game,
        )


if __name__ == "__main__":
    app = NumberGuessingGame()
    app.mainloop()
