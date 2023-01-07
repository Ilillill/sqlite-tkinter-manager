# sqlite-tkinter-manager
Simple SQLite database manager for Python applications with a Tkinter GUI

This SQLite Database Manager is a simple and easy-to-use tool for managing SQLite databases within Python applications.

The GUI was written in TKInter

Should handle database-related errors

It allows not only to create and select databases, but also includes a feature that checks for issues with connected databases upon app start. The manager window will automatically open whenever a problem is detected with a connected database.



INSTRUCTIONS


Replace in main.py:


Line 27: Window(root)

    Here you can create your main window


Replace in database.py:



Line 10: database_id = 'unique_id'

    This ID can be anything, it is here to ensure the database is compatible with this app


Line 100: create_tables = 

    Create your own tables
