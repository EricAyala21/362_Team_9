import customtkinter
from daily_log    import DailyLog
from viewpage     import ViewPage
from analytics    import AnalyticsPage
from fileSelector import Users  
import sqlite3

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x600")
        self.root.minsize(900, 500)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")

        self.file_names = []
        self.db_conn    = None
        self.db_cursor  = None

        self.user_screen()

    def user_screen(self):
        # show user-selection screen
        self.page = Users(master=self.root, callback=self.launch_main_app)
        self.page.pack(padx=20, pady=20, fill="both", expand=True)

    def launch_main_app(self, db_filename):
        # after picking DB, tear down user selector
        self.page.destroy()
        self.file_names = [db_filename]
        self.db_conn    = sqlite3.connect(db_filename)
        self.db_cursor  = self.db_conn.cursor()
        self.ensure_logs_table_exists()
        self.create_tabs()

    def ensure_logs_table_exists(self):
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                timestamp TEXT PRIMARY KEY,
                drivetime REAL,
                resttime  REAL
            );
        """)
        self.db_conn.commit()

    def create_tabs(self):
        # build the tabview container
        self.tab_view = customtkinter.CTkTabview(self.root)
        self.tab_view.pack(fill="both", expand=True)

        # add tabs by name (no assignment)
        for name in ["Daily Log", "View", "Analytics", "Log Out"]:
            self.tab_view.add(name)

        # --- Daily Log tab ---
        print("→ Adding Daily Log")
        dl_frame = self.tab_view.tab("Daily Log")
        DailyLog(master=dl_frame, filename=self.file_names[0])\
            .pack(fill="both", expand=True)

        # --- View tab ---
        print("→ Adding View Page")
        vp_frame = self.tab_view.tab("View")
        ViewPage(master=vp_frame, filename=self.file_names[0])\
            .pack(fill="both", expand=True)

        # --- Analytics tab ---
        print("→ Adding Analytics Page")
        ap_frame = self.tab_view.tab("Analytics")
        AnalyticsPage(master=ap_frame, filename=self.file_names[0])\
            .pack(fill="both", expand=True)

        # --- Log Out tab ---
        print("→ Adding Log Out label")
        lo_frame = self.tab_view.tab("Log Out")

        # configure a 1×1 grid that expands
        lo_frame.grid_columnconfigure(0, weight=1)
        lo_frame.grid_rowconfigure(0, weight=1)

        # clear any leftover widgets
        for w in lo_frame.winfo_children():
            w.destroy()

        # place the exit message in the center
        customtkinter.CTkLabel(
            lo_frame,
            text="Click the 'X' to close the app.",
            anchor="center"
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def return_to_user_screen(self):
        # go back to user file selector
        self.tab_view.destroy()
        self.user_screen()


if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Trucker Time Logger")
    FileManager(root)
    root.mainloop()
