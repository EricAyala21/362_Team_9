import customtkinter as ctk
from Analytics import AnalyticsPage   # or from Analytics import AnalyticsPage if you renamed

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")


    root = ctk.CTk()
    root.geometry("800x450")         #your window size
    
    header = ctk.CTkLabel(
        root,
        text="Truck Time Logger",
        font=("Arial", 24)
    )
    header.pack(pady=20)  # font name and size
    page = AnalyticsPage(root, "truck_time_logs.db")
    page.pack(fill="both", expand=True)
    root.mainloop()
