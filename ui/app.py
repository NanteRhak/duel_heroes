import tkinter as tk
from tkinter import ttk, messagebox
from core.game import Game
from .combat_log import CombatLog

class DuelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Duel de Héros")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.game = Game()
        self.create_widgets()
        self.show_character_selection()

    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Panneaux
        self.selection_frame = ttk.Frame(self.main_frame)
        self.combat_frame = ttk.Frame(self.main_frame)
        
        # Widgets de sélection
        ttk.Label(self.selection_frame, text="Joueur 1").grid(row=0, column=0)
        self.p1_name = ttk.Entry(self.selection_frame)
        self.p1_name.grid(row=1, column=0)
        self.p1_class = ttk.Combobox(self.selection_frame, values=["Guerrier", "Mage", "Archer"])
        self.p1_class.grid(row=2, column=0)
        self.p1_class.current(0)
        
        ttk.Label(self.selection_frame, text="Joueur 2").grid(row=0, column=1)
        self.p2_name = ttk.Entry(self.selection_frame)
        self.p2_name.grid(row=1, column=1)
        self.p2_class = ttk.Combobox(self.selection_frame, values=["Guerrier", "Mage", "Archer"])
        self.p2_class.grid(row=2, column=1)
        self.p2_class.current(1)
        
        self.start_btn = ttk.Button(self.selection_frame, text="Commencer le duel", command=self.start_duel)
        self.start_btn.grid(row=3, column=0, columnspan=2)

        # Widgets de combat
        self.p1_stats = ttk.Label(self.combat_frame, text="")
        self.p1_stats.grid(row=0, column=0)
        self.p2_stats = ttk.Label(self.combat_frame, text="")
        self.p2_stats.grid(row=0, column=1)
        
        self.action_frame = ttk.Frame(self.combat_frame)
        self.action_frame.grid(row=1, column=0, columnspan=2)
        
        self.attack_btn = ttk.Button(self.action_frame, text="Attaquer", command=lambda: self.execute_action("attaquer"))
        self.attack_btn.grid(row=0, column=0)
        self.special_btn = ttk.Button(self.action_frame, text="Spéciale", command=lambda: self.execute_action("special"))
        self.special_btn.grid(row=0, column=1)
        self.defend_btn = ttk.Button(self.action_frame, text="Défendre", command=lambda: self.execute_action("defendre"))
        self.defend_btn.grid(row=0, column=2)
        self.recharge_btn = ttk.Button(self.action_frame, text="Recharger", command=lambda: self.execute_action("recharger"))
        self.recharge_btn.grid(row=0, column=3)
        
        self.tour_label = ttk.Label(self.combat_frame, text="", font=('Arial', 12, 'bold'))
        self.tour_label.grid(row=2, column=0, columnspan=2)
        
        self.back_btn = ttk.Button(self.combat_frame, text="Nouveau duel", command=self.show_character_selection)
        self.back_btn.grid(row=3, column=0, columnspan=2)

        # Journal de combat
        self.log = CombatLog(self)
        self.log.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def show_character_selection(self):
        self.combat_frame.grid_remove()
        self.selection_frame.grid(row=0, column=0, sticky="nsew")

    def show_combat_interface(self):
        self.selection_frame.grid_remove()
        self.combat_frame.grid(row=0, column=0, sticky="nsew")
        self.update_combat_display()

    def start_duel(self):
        p1_name = self.p1_name.get().strip() or "Joueur 1"
        p2_name = self.p2_name.get().strip() or "Joueur 2"
        
        if not self.game.creer_personnage(self.p1_class.get().lower(), p1_name, 1):
            messagebox.showerror("Erreur", "Classe invalide pour le Joueur 1")
            return
            
        if not self.game.creer_personnage(self.p2_class.get().lower(), p2_name, 2):
            messagebox.showerror("Erreur", "Classe invalide pour le Joueur 2")
            return
            
        if not self.game.demarrer_combat():
            messagebox.showerror("Erreur", "Impossible de démarrer le combat")
            return
            
        self.log.clear()
        self.show_combat_interface()

    def execute_action(self, action):
        """Gère une action du joueur puis lance le tour de l'IA"""
        success, is_finished = self.game.executer_action(action)
        
        if not success:
            messagebox.showwarning("Action impossible", "Cette action n'est pas disponible maintenant")
            return
            
        self.update_combat_display()
        
        if is_finished:
            self.disable_actions()
            messagebox.showinfo("Combat terminé", f"{self.game.gagnant.nom} a gagné !")
        else:
            # Lancer le tour de l'IA après un délai
            self.after(1000, self.execute_ia_turn)

    def execute_ia_turn(self):
        """Exécute le tour de l'IA et met à jour l'interface"""
        success, is_finished = self.game.executer_action_ia()
        self.update_combat_display()
        
        if is_finished:
            self.disable_actions()
            messagebox.showinfo("Combat terminé", f"{self.game.gagnant.nom} a gagné !")

    def update_combat_display(self):
        state = self.game.get_etat_combat()
        
        # Mise à jour des stats
        self.p1_stats.config(text=f"{state['joueur1']['nom']}\nPV: {state['joueur1']['pv']}\nÉnergie: {state['joueur1']['energie']}")
        self.p2_stats.config(text=f"{state['joueur2']['nom']}\nPV: {state['joueur2']['pv']}\nÉnergie: {state['joueur2']['energie']}")
        
        # Mise à jour du journal
        for msg in state['historique']:
            self.log.add_message(msg)
        
        # Gestion des boutons et label de tour
        current_turn = state['tour']
        is_player_turn = (current_turn == 1)
        
        self.attack_btn.state(["!disabled" if is_player_turn else "disabled"])
        self.special_btn.state(["!disabled" if is_player_turn else "disabled"])
        self.defend_btn.state(["!disabled" if is_player_turn else "disabled"])
        self.recharge_btn.state(["!disabled" if is_player_turn else "disabled"])
        
        if current_turn == 1:
            self.tour_label.config(text=f"À vous de jouer !", foreground="green")
        else:
            self.tour_label.config(text=f"L'IA réfléchit...", foreground="red")

    def disable_actions(self):
        for btn in [self.attack_btn, self.special_btn, self.defend_btn, self.recharge_btn]:
            btn.state(["disabled"])

    def run(self):
        self.mainloop()
