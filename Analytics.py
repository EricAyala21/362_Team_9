
import customtkinter 
import sqlite3
import tkinter
from tkcalendar import Calendar 
from ctk_date_picker import CTkDatePicker


class AnalyticsPage(customtkinter.CTkFrame):
    def __init__(self, master, filename):
        super().__init__(master)

        try:
            self.con = sqlite3.connect(filename)
            self.cur = self.con.cursor()

        except:
            print("sql file connection failed: " + filename)
        self.rightFrame()
        self.leftFrame()    

    def rightFrame(self):
        self.graphFrame = customtkinter.CTkFrame(self)

        self.graphFrame.pack(expand = True, side = "right",fill="both",padx = 10, pady = 10)
    def leftFrame(self):
        

        self.calanderFrame()
        self.legendFrame()
    def calanderFrame(self):
        self.dateFrame = customtkinter.CTkFrame(self)
        self.dateFrame.pack(expand = "True", side = "top",fill = "both", padx = 5, pady = 5)
       
        self.startDate = CTkDatePicker(self.dateFrame)
        self.startDate.pack(pady=2)
        self.endDate = CTkDatePicker(self.dateFrame)
        self.endDate.pack(pady = 2)



    def legendFrame(self):
        self.legendFrame = customtkinter.CTkFrame(self)

        self.legendFrame.pack(expand = "True",side  = "bottom", fill = "both", padx = 5, pady = 5)

        self.drivingTime =  customtkinter.CTkCheckBox(self.legendFrame, text = "Driving Time",width = 10, height = 10)
        self.drivingTime.grid(row= 1, column = 10, padx = 10, pady = 20, sticky = "news")

        self.restingTime =  customtkinter.CTkCheckBox(self.legendFrame, text = "Resting Time",width = 10, height = 10)
        self.restingTime.grid(row= 2, column = 10, padx = 10, pady = 10, sticky = "news")

        #self.onDuty =  customtkinter.CTkCheckBox(self.legendFrame, text = "On Duty Time ",width = 10, height = 10)
       # self.onDuty.grid(row= 2, column = 10, padx = 10, pady = 10, sticky = "news")