#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
from ui.app import DuelApp

def main():
    """Point d'entrée principal de l'application"""
    try:
        app = DuelApp()
        app.run()
    except Exception as e:
        print(f"A critical error occurred: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
