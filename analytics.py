import customtkinter
import sqlite3
import tkinter
from tkcalendar import Calendar 
# from ctk_date_picker import CTkDatePicker  # Comment this out temporarily

class AnalyticsPage(customtkinter.CTkFrame):
    def __init__(self, master, filename):
        super().__init__(master)

        try:
            self.con = sqlite3.connect(filename)
            self.cur = self.con.cursor()
        except:
            print("SQL file connection failed: " + filename)

        self.rightFrame()
        self.leftFrame()

    def rightFrame(self):
        self.graphFrame = customtkinter.CTkFrame(self)
        self.graphFrame.pack(expand=True, side="right", fill="both", padx=10, pady=10)

    def leftFrame(self):
        # This method will contain the date picker, which we temporarily replace
        self.calanderFrame()
        self.legendFrame()

    def calanderFrame(self):
        self.dateFrame = customtkinter.CTkFrame(self)
        self.dateFrame.pack(expand=True, side="top", fill="both", padx=5, pady=5)
        
        # Temporarily replace CTkDatePicker with a placeholder label
        # from ctk_date_picker import CTkDatePicker  # Comment this line temporarily
        placeholder_label = customtkinter.CTkLabel(self.dateFrame, text="Date Picker (coming soon)")
        placeholder_label.grid(row=0, column=0, padx=10, pady=5)
        
        # If you want to add the end date as well, you can use another placeholder
        placeholder_label_end = customtkinter.CTkLabel(self.dateFrame, text="End Date Picker (coming soon)")
        placeholder_label_end.grid(row=0, column=1, padx=10, pady=5)

    def legendFrame(self):
        self.legendFrame = customtkinter.CTkFrame(self)
        self.legendFrame.pack(expand=True, side="bottom", fill="both", padx=5, pady=5)

        self.drivingTime = customtkinter.CTkCheckBox(self.legendFrame, text="Driving Time", width=10, height=10)
        self.drivingTime.grid(row=1, column=10, padx=10, pady=20, sticky="news")

        self.restingTime = customtkinter.CTkCheckBox(self.legendFrame, text="Resting Time", width=10, height=10)
        self.restingTime.grid(row=2, column=10, padx=10, pady=10, sticky="news")