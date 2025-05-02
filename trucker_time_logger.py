import customtkinter
from tkinter import *
import fileSelector


class file_manage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("650x350")
        self.root.minsize(630, 300) 
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        
        self.con = None # sql connection
        self.cur = None # sql cursor

        self.setup_gui()


    def setup_gui(self):
        self.page = fileSelector.Users(master = root)
        self.page.pack(pady = 20, padx= 60,fill = "both", expand = True )
        self.page.grid_columnconfigure((0,1,2),weight = 1)
        self.page.grid_rowconfigure(1,weight = 1)
        self.page.grid_rowconfigure(2,weight = 6)          
root = customtkinter.CTk()
app = file_manage(root)
root.mainloop()