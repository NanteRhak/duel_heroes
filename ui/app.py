import tkinter as tk
from tkinter import ttk, messagebox
import traceback
from core.game import Game
from .combat_log import CombatLog


class DuelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Duel of Heroes")
        self.geometry("800x600")
        self.resizable(False, False)

        self.game = Game()
        self._log_shown = 0
        self._ai_job = None
        self.create_widgets()
        self.show_character_selection()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.selection_frame = ttk.Frame(self.main_frame)
        self.combat_frame = ttk.Frame(self.main_frame)

        ttk.Label(self.selection_frame, text="Player 1").grid(row=0, column=0)
        self.p1_name = ttk.Entry(self.selection_frame)
        self.p1_name.grid(row=1, column=0)
        self.p1_class = ttk.Combobox(self.selection_frame, values=["Warrior", "Mage", "Archer"])
        self.p1_class.grid(row=2, column=0)
        self.p1_class.current(0)

        ttk.Label(self.selection_frame, text="Player 2").grid(row=0, column=1)
        self.p2_name = ttk.Entry(self.selection_frame)
        self.p2_name.grid(row=1, column=1)
        self.p2_class = ttk.Combobox(self.selection_frame, values=["Warrior", "Mage", "Archer"])
        self.p2_class.grid(row=2, column=1)
        self.p2_class.current(1)

        self.start_btn = ttk.Button(self.selection_frame, text="Start duel", command=self.start_duel)
        self.start_btn.grid(row=3, column=0, columnspan=2)

        self.p1_stats = ttk.Label(self.combat_frame, text="")
        self.p1_stats.grid(row=0, column=0)
        self.p2_stats = ttk.Label(self.combat_frame, text="")
        self.p2_stats.grid(row=0, column=1)

        self.action_frame = ttk.Frame(self.combat_frame)
        self.action_frame.grid(row=1, column=0, columnspan=2)

        self.attack_btn = ttk.Button(self.action_frame, text="Attack", command=lambda: self.execute_action("attack"))
        self.attack_btn.grid(row=0, column=0)
        self.special_btn = ttk.Button(self.action_frame, text="Special", command=lambda: self.execute_action("special"))
        self.special_btn.grid(row=0, column=1)
        self.defend_btn = ttk.Button(self.action_frame, text="Defend", command=lambda: self.execute_action("defend"))
        self.defend_btn.grid(row=0, column=2)
        self.recharge_btn = ttk.Button(self.action_frame, text="Recharge", command=lambda: self.execute_action("recharge"))
        self.recharge_btn.grid(row=0, column=3)

        self.turn_label = ttk.Label(self.combat_frame, text="", font=('Arial', 12, 'bold'))
        self.turn_label.grid(row=2, column=0, columnspan=2)

        self.back_btn = ttk.Button(self.combat_frame, text="New duel", command=self.show_character_selection)
        self.back_btn.grid(row=3, column=0, columnspan=2)

        self.log = CombatLog(self)
        self.log.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def show_character_selection(self):
        if self._ai_job is not None:
            self.after_cancel(self._ai_job)
            self._ai_job = None
        self.combat_frame.grid_remove()
        self.selection_frame.grid(row=0, column=0, sticky="nsew")

    def show_combat_interface(self):
        self.selection_frame.grid_remove()
        self.combat_frame.grid(row=0, column=0, sticky="nsew")
        self.update_combat_display()

    def start_duel(self):
        p1_name = self.p1_name.get().strip() or "Player 1"
        p2_name = self.p2_name.get().strip() or "Player 2"

        if not self.game.create_character(self.p1_class.get().lower(), p1_name, 1):
            messagebox.showerror("Error", "Invalid class for Player 1")
            return

        if not self.game.create_character(self.p2_class.get().lower(), p2_name, 2):
            messagebox.showerror("Error", "Invalid class for Player 2")
            return

        if not self.game.start_combat():
            messagebox.showerror("Error", "Cannot start the duel")
            return

        self.log.clear()
        self._log_shown = 0
        self.show_combat_interface()

    def execute_action(self, action):
        """Run the human action, then schedule the AI turn."""
        success, is_finished = self.game.perform_action(action)

        if not success:
            messagebox.showwarning("Action unavailable", "This action is not available right now")
            return

        self.update_combat_display()

        if is_finished:
            self.disable_actions()
            messagebox.showinfo("Combat over", f"{self.game.winner.name} wins!")
        else:
            self._ai_job = self.after(1000, self.execute_ai_turn)

    def execute_ai_turn(self):
        """Run the AI turn and refresh the interface."""
        self._ai_job = None
        _, is_finished = self.game.perform_ai_action()
        self.update_combat_display()

        if is_finished:
            self.disable_actions()
            messagebox.showinfo("Combat over", f"{self.game.winner.name} wins!")

    def update_combat_display(self):
        state = self.game.get_state()

        self.p1_stats.config(text=f"{state['player1']['name']}\nHP: {state['player1']['hp']}\nEnergy: {state['player1']['energy']}")
        self.p2_stats.config(text=f"{state['player2']['name']}\nHP: {state['player2']['hp']}\nEnergy: {state['player2']['energy']}")

        for msg in state['history'][self._log_shown:]:
            self.log.add_message(msg)
        self._log_shown = len(state['history'])

        current_turn = state['turn']
        is_player_turn = (current_turn == 1)

        self.attack_btn.state(["!disabled" if is_player_turn else "disabled"])
        self.special_btn.state(["!disabled" if is_player_turn else "disabled"])
        self.defend_btn.state(["!disabled" if is_player_turn else "disabled"])
        self.recharge_btn.state(["!disabled" if is_player_turn else "disabled"])

        if current_turn == 1:
            self.turn_label.config(text="Your turn!", foreground="green")
        else:
            self.turn_label.config(text="AI is thinking...", foreground="red")

    def disable_actions(self):
        for btn in [self.attack_btn, self.special_btn, self.defend_btn, self.recharge_btn]:
            btn.state(["disabled"])

    def report_callback_exception(self, exc, val, tb):
        traceback.print_exception(exc, val, tb)

    def run(self):
        self.mainloop()
