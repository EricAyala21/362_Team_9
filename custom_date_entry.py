import datetime as dt
import customtkinter as ctk
import tkinter as tk
import tkcalendar
import sys
from ctk_date_picker import CTkDatePicker

class CustomDateEntry (ctk.CTkFrame):
    BUTTON_COLOR = "#3B8ED0"
    HOVER_COLOR = "#273366"
    WEEKEND_COLOR = "#e8f4fa"
    CTK_DATE_FORMAT = "%m/%d/%Y"

    def __init__(self, master, **args):
        """Initialize the data entry widget within a CTkFrame"""
        super().__init__(master, **args)

        self.is_win = sys.platform.startswith("win")
        self.configure(fg_color = "transparent")
        self.columnconfigure(0, weight = 1)
        # convert the current font from customtkinter to the Font in tkinter
        self.cur_font = ctk.CTkLabel(self).cget("font")
        self.SIZE = self.cur_font.cget("size")
        self.FAMILY = self.cur_font.cget("family")
        self.WEIGHT = self.cur_font.cget("weight")
        self.tk_font = tk.font.Font(family = self.FAMILY, size = self.SIZE, weight = self.WEIGHT)
        # declare the name for the date entry box
        self.date_entry = None
        self.previous = None
        self.dummy = ctk.CTkEntry(self)
        self.dummy.grid(row = 0, column = 0, sticky="nswe", padx = (0, 5))
        self.clear()
    
    def create_date_entry(self):
        """generate a new date entry box, if exists already, will delete it before create new box."""
        if self.is_win:
            if self.date_entry != None and self.date_entry._top_cal.winfo_exists():
                self.date_entry.pack_forget()
                if(self.previous is not None and self.previous.winfo_exists()):
                    self.previous.destroy()
                self.previous = self.date_entry
            self.date_entry = tkcalendar.DateEntry(self, font = self.tk_font
                                                    , corner_radius = 6
                                                    , foreground = "white"
                                                    , background = self.HOVER_COLOR
                                                    , selectbackground = self.BUTTON_COLOR
                                                    , weekendbackground = self.WEEKEND_COLOR
                                                    , height = 28)
            self.date_entry.bind("<<DateEntrySelected>>", self.refresh)
        else:
            if self.date_entry != None:
                self.date_entry.destroy()
            self.date_entry = CTkDatePicker(self)
            self.date_entry.set_allow_manual_input(True)
            self.date_entry.set_allow_change_month(True)
            self.date_entry.set_date_format(self.CTK_DATE_FORMAT)
            self.date_entry.date_entry.configure(width = 100)
            self.date_entry.date_entry.grid_forget()
            self.date_entry.date_entry.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
            self.date_entry.calendar_button.grid_forget()
            self.date_entry.calendar_button.grid(row=0, column=1, sticky="ew", padx=0, pady=0)
        self.date_entry.grid(row = 0, column = 0, sticky="nswe", padx = (0, 5))


    def get_date(self):
        """get the current date input and refresh the date entry box to the input date.
        If input is empty or invalid, will return None"""
        if self.is_win:
            if(not self.date_entry.get().strip()):
                return None
            result = self.date_entry.get_date()
            self.set_date(result)
            return result
        else:
            if(len(self.date_entry.get_date()) == 0):
                return None
            return dt.datetime.strptime(self.date_entry.get_date(), self.CTK_DATE_FORMAT).date()
            
    
    def set_date(self, date : dt.datetime):
        """Refresh the date entry box and set its content to the input date (a datetime.datetime instance),
        update the calendar widget to input date"""
        if self.is_win:
            self.create_date_entry()
            self.date_entry.set_date(date)
        else:
            self.create_date_entry()
            self.date_entry.date_entry.insert(0, date.strftime(self.CTK_DATE_FORMAT))


    def clear(self):
        """Delete the content within the date entry box"""
        self.create_date_entry()
        if self.is_win:
            self.date_entry.delete(0, 'end')


    def refresh(self, event):
        """Refresh the date entry box"""
        self.get_date()
