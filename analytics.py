import customtkinter as ctk

class AnalyticsPage(ctk.CTkFrame):
    def __init__(self, master, db_file):
        super().__init__(master)

        label = ctk.CTkLabel(
            self,
            text="Analytics Page (Graphs Not Loaded Yet)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(padx=20, pady=20)
