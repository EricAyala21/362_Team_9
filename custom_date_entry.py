import datetime as dt
import customtkinter as ctk
import tkinter as tk
import tkcalendar

class CustomDateEntry (ctk.CTkFrame):
    BUTTON_COLOR = "#3B8ED0"
    HOVER_COLOR = "#273366"
    WEEKEND_COLOR = "#e8f4fa"

    def __init__(self, master, **args):
        super().__init__(master, **args)

        self.cur_font = ctk.CTkLabel(self).cget("font")
        self.SIZE = self.cur_font.cget("size")
        self.FAMILY = self.cur_font.cget("family")
        self.WEIGHT = self.cur_font.cget("weight")
        self.tk_font = tk.font.Font(family = self.FAMILY, size = self.SIZE, weight = self.WEIGHT)
        self.date_entry = None
        self.clear()
    
    def create_date_entry(self):
        if self.date_entry != None:
            self.date_entry.pack_forget()
        self.date_entry = tkcalendar.DateEntry(self, font = self.tk_font
                                                , corner_radius = 6
                                                , foreground = "white"
                                                , background = self.HOVER_COLOR
                                                , selectbackground = self.BUTTON_COLOR
                                                , weekendbackground = self.WEEKEND_COLOR)
        self.date_entry.bind("<<DateEntrySelected>>", self.refresh)
        self.date_entry.pack()

    def get_date(self):
        if(not self.date_entry.get().strip()):
            return None
        result = self.date_entry.get_date()
        self.set_date(result)
        return result
    
    def set_date(self, date : dt.datetime):
        self.create_date_entry()
        self.date_entry.set_date(date)

    def clear(self):
        self.create_date_entry()
        self.date_entry.delete(0, 'end')

    def refresh(self, event):
        self.get_date()


        

# ctk.set_appearance_mode("light")
# ctk.set_default_color_theme("blue")
# app = ctk.CTk()
# app.geometry ("300x300")
# app.columnconfigure(1, weight = 3)
# input_box = CustomDateEntry(app)
# input_box.grid(row = 0, column = 0)
# btn1 = ctk.CTkButton(app, text = "get", command=lambda a = None : print(input_box.get_date()))
# btn1.grid(row = 1, column = 1, sticky = "ewns")
# btn2 = ctk.CTkButton(app, text = "clear", command=input_box.clear)
# btn2.grid(row = 1, column = 0)
# btn3 = ctk.CTkButton(app, text = "set", command=lambda a = dt.date(2025,3,15): input_box.set_date(a))
# btn3.grid(row = 2, column = 0)
# app.mainloop()