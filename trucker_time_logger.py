import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import daily_log
import viewpage
from analytics import AnalyticsPage 
import sqlite3
import os
import sys

# For Windows DPI scaling fix (prevents oversized UI on high DPI screens)
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(0)
except:
    pass  # This will only affect Windows, so skip if unsupported

# Main application class to handle file selection and page switching
class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x600")
        self.root.minsize(900, 500)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")

        self.file_names = []   # List of database file names
        self.db_conn = None    # Active database connection
        self.db_cursor = None  # Database cursor

        self.setup_data()
        self.create_tabs()

    def setup_data(self):
        # Check available .db files or create a default one
        files = [f for f in os.listdir() if f.endswith(".db")]
        if not files:
            with sqlite3.connect("default.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        timestamp TEXT PRIMARY KEY,
                        drivetime REAL,
                        resttime REAL
                    );
                """)
            files = ["default.db"]

        self.file_names = files
        self.db_conn = sqlite3.connect(self.file_names[0])
        self.db_cursor = self.db_conn.cursor()

    def create_tabs(self):
        # Create tab view
        self.tab_view = customtkinter.CTkTabview(self.root)
        self.tab_view.pack(fill="both", expand=True)

        # Add tabs for different pages
        self.daily_log_tab = self.tab_view.add("Daily Log")
        self.view_tab = self.tab_view.add("View")
        self.analytics_tab = self.tab_view.add("Analytics")
        self.logout_tab = self.tab_view.add("Logout")

        # Load pages into respective tabs
        daily_log.Daily_Log(self.daily_log_tab, self.file_names[0]).pack(fill="both", expand=True)
        viewpage.ViewPage(self.view_tab, self.file_names[0]).pack(fill="both", expand=True)
        AnalyticsPage(self.analytics_tab, self.file_names[0]).pack(fill="both", expand=True)

        # Optional logout message
        logout_label = customtkinter.CTkLabel(self.logout_tab, text="Click the 'X' to close the app.")
        logout_label.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Trucker Time Logger")
    app = FileManager(root)
    root.mainloop()
