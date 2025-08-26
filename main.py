#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from ui.app import DuelApp

def main():
    """Point d'entrée principal de l'application"""
    try:
        app = DuelApp()
        app.run()
    except Exception as e:
        print(f"Une erreur critique est survenue : {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
