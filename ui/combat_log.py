import tkinter as tk
from tkinter import scrolledtext, font as tkfont

class CombatLog(tk.Frame):
    def __init__(self, master, **kwargs):
        """
        Widget personnalisé pour afficher le journal de combat
        Args:
            master: Widget parent
            **kwargs: Arguments supplémentaires pour Frame
        """
        super().__init__(master, **kwargs)
        self.configure(bg='#333')
        
        # Configuration de la grille
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Création du widget Text avec barre de défilement
        self.text_area = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            state='disabled',
            bg='#222',
            fg='white',
            insertbackground='white',
            selectbackground='#444',
            font=tkfont.Font(family='Consolas', size=10),
            padx=10,
            pady=10
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")
        
        # Tags pour le formatage
        self.text_area.tag_config('player1', foreground='#4fc3f7')
        self.text_area.tag_config('player2', foreground='#ff5252')
        self.text_area.tag_config('damage', foreground='#ff7043')
        self.text_area.tag_config('special', foreground='#ba68c8')
        self.text_area.tag_config('system', foreground='#aed581')
        self.text_area.tag_config('warning', foreground='#ff8a65')

    def add_message(self, message):
        """
        Ajoute un message au journal de combat avec formatage automatique
        Args:
            message (str): Message à afficher
        """
        self.text_area.configure(state='normal')
        
        # Détection automatique du type de message pour le formatage
        tags = self._detect_tags(message)
        
        self.text_area.insert(tk.END, message + "\n", tags)
        self.text_area.see(tk.END)  # Auto-scroll
        self.text_area.configure(state='disabled')

    def _detect_tags(self, message):
        """
        Détecte les tags appropriés en fonction du contenu du message
        Args:
            message (str): Message à analyser
        Returns:
            tuple: Tags à appliquer
        """
        tags = ()
        
        if any(x in message for x in ["strikes", "fires", "casts", "unleashes", "looses", "summons"]):
            if "Player 1" in message or "Warrior" in message or "Mage" in message:
                tags += ('player1',)
            elif "Player 2" in message or "Archer" in message:
                tags += ('player2',)
            
            if any(x in message for x in ["powerful", "storm", "precise"]):
                tags += ('special',)
            elif "-" in message:
                tags += ('damage',)
        
        elif "duel" in message or "turn" in message:
            tags += ('system',)
        elif "energy" in message or "defensive" in message:
            tags += ('system',)
        elif "not enough" in message or "unavailable" in message:
            tags += ('warning',)
            
        return tags if tags else ()

    def clear(self):
        """Efface tout le contenu du journal"""
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.configure(state='disabled')

    def get_content(self):
        """
        Récupère le contenu actuel du journal
        Returns:
            str: Contenu complet du journal
        """
        return self.text_area.get(1.0, tk.END)
