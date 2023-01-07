import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pickle
import sqlite3
import shutil
import datetime

database_id = 'unique_id'

try:
    with open("./databases/database_data.dat", "rb") as file:
        database_name = pickle.load(file)
except:
    database_name = ''


def check_database_id(selected_database):
    connection = sqlite3.connect(selected_database)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM database_id")
    check_id = cursor.fetchone()
    cursor.close()
    connection.close()
    if check_id[0] == database_id:
        return True


def database_backup():
    database_path = filedialog.askopenfilename(title="Select database to export", defaultextension="db", initialdir=f'{os.path.abspath(database_name)}')
    if database_path:
        path = filedialog.askdirectory(title='Select folder')
        try:
            shutil.copyfile(database_path, f"{path}/{datetime.datetime.now().strftime('%Y%m%d')}_database_backup.db")
        except FileNotFoundError:
            pass


class DatabaseManager(tk.Frame):
    def __init__(self, container, cm=None, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.cm = cm

        self.columnconfigure(0, minsize=500, weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.config(bg='white')
        self.grid(row=0, column=0, sticky='NEWS')

        self.sqlite_logo = tk.PhotoImage(file="./assets_database/logo_sqlite.png")
        self.label_logo_sqlite = tk.Label(self, image=self.sqlite_logo, bg='white', height=304)
        self.label_logo_sqlite.grid(row=0, column=0, sticky='s', padx=50, pady=50)

        self.buttons_frame = tk.Frame(self, bg='white')
        self.buttons_frame.grid(row=1, column=0, sticky='n')
        self.buttons_frame.columnconfigure((0, 1), weight=1)

        self.create_image = tk.PhotoImage(file="./assets_database/database_open.png")
        self.button_sqlite_create = tk.Button(self.buttons_frame, image=self.create_image, compound="top", text="OPEN", width=150, bg='white', relief='flat')
        self.button_sqlite_create["command"] = lambda: self.database_open()
        self.button_sqlite_create.grid(row=0, column=0, sticky="ew")

        self.open_image = tk.PhotoImage(file="./assets_database/database_add.png")
        self.button_sqlite_open = tk.Button(self.buttons_frame, image=self.open_image, compound="top", text="CREATE", width=150, bg='white', relief='flat',)
        self.button_sqlite_open["command"] = lambda: self.database_create()
        self.button_sqlite_open.grid(row=0, column=1, sticky="ew")

        self.status_label_database_name = tk.Label(self.buttons_frame, text='', bg='white', fg="black")
        self.status_label_database_name.grid(row=2, column=0, sticky="WE", columnspan=2)

        if self.cm is not None:
            self.start_app_image = tk.PhotoImage(file="./assets_database/apply.png")
            self.button_start_app = tk.Button(self.buttons_frame, text='Launch app', compound="left", bg='white', relief='flat', image=self.start_app_image, state='disabled')
            self.button_start_app["command"] = self.cm
            self.button_start_app.grid(row=3, column=0, pady=20, sticky="ew", columnspan=2)

        if database_name != '':
            self.status_label_database_name.config(text=f"Selected database: {os.path.basename(database_name)}", fg='#0f80cc')
            self.button_start_app['state'] = 'normal'

    def database_create(self):
        global database_name
        try:
            database_path = filedialog.asksaveasfilename(title="Create Database", initialdir="./databases/", defaultextension="db", filetypes=(("Database files *.db", "*.db"), ("All files", "*.*")))
        except (AttributeError, FileNotFoundError):
            return

        if len(database_path) != 0:
            database_name = database_path
            try:
                with sqlite3.connect(database_path) as connection:
                    cursor = connection.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS database_id(d_id text)")
                    cursor.execute("INSERT INTO database_id VALUES(?)", (database_id,))
                    with open("./databases/database_data.dat", "wb") as dumpfile:
                        pickle.dump(database_name, dumpfile)
                    self.status_label_database_name.config(text=f"Selected database: {os.path.basename(database_name)}", fg='#0f80cc')
                    self.button_start_app['state'] = 'normal'
                    ##############################################################################################################
                    create_tables = "CREATE TABLE IF NOT EXISTS sample (name TEXT NOT NULL, date TEXT NOT NULL, description TEXT)"
                    ##############################################################################################################
                    cursor.execute(create_tables)
                    cursor.close()
                    connection.commit()
            except sqlite3.Error as error:
                messagebox.showerror(title='Database Error', message=f"{os.path.basename(database_name).capitalize()} ERROR:\n{error}")

    def database_open(self):
        global database_name
        try:
            database_to_import = filedialog.askopenfilename(title="Select database file to open", filetypes=(("Database files", "*.db"), ("All files", "*.*")))
        except (AttributeError, FileNotFoundError):
            messagebox.showinfo(title='Error', message="Error opening database, please try again.")
            return
        if len(database_to_import) != 0:
            if database_to_import != '':
                if check_database_id(database_to_import):
                    database_name = database_to_import
                    with open("./databases/database_data.dat", "wb") as dumpfile:
                        pickle.dump(database_name, dumpfile)
                    self.status_label_database_name.config(text=f"Selected database: {os.path.basename(database_name)}", fg='#0f80cc')
                    self.button_start_app['state'] = 'normal'
                else:
                    messagebox.showinfo(title='Database Error', message=f"{os.path.basename(database_to_import).capitalize()} doesn't belong to this app.")

def check_database():
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM database_id")
        dbcheck = cursor.fetchone()
        cursor.close()
        return dbcheck