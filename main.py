import tkinter as tk
from tkinter import ttk
import sqlite3

import database as db

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class Window(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="NEWS")

        ttk.Label(self, text=f"Database connected successfuly").grid(row=0, column=0, sticky="NEWS", pady=150, padx=150, columnspan=2)
        ttk.Button(self, text="Database manager", command=lambda: db.DatabaseManager(root, cm=lambda: start_app())).grid(row=1, column=0, sticky="E", pady=50, padx=5)
        ttk.Button(self, text="Export database", command=lambda: db.database_backup()).grid(row=1, column=1, sticky="W", pady=50, padx=5)

def start_app():
    try:
        db.check_database()
        Window(root)
    except sqlite3.OperationalError:
        db.DatabaseManager(root, cm=lambda: start_app())

root = tk.Tk()

start_app()

root.mainloop()
