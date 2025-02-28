import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import viewpage




class file_manage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("650x350")
        self.root.minsize(630, 300)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        self.file_Names = []
        self.frame = ""
        self.setup_gui()

    def setup_gui(self):
        
        self.frame = customtkinter.CTkFrame(master=root)

        self.frame.pack(pady =20,padx = 60, fill = "both", expand = True)
        self.frame.grid_columnconfigure((0,1,2), weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=6)
     

  

        button1 = customtkinter.CTkButton(master = self.frame,
                                          text = "Daily Log",
                                          command = self.DailyLog,
                                          height = 50,
                                          width = 120,
                                          corner_radius = 25)
        button1.grid (row = 1, column = 0, padx = 10, pady = 10)

        button2 = customtkinter.CTkButton(master = self.frame,
                                          text = "View",
                                          command = self.view,
                                          height = 50,
                                          width = 120,
                                          corner_radius = 25)
        button2.grid (row = 1, column = 1, padx = 10, pady = 10)


        button3 = customtkinter.CTkButton(master = self.frame,
                                          text = "Analytics",
                                          command = self.Analytics,
                                          height = 50,
                                          width = 120,
                                          corner_radius = 25)
        button3.grid (row = 1, column = 2, padx = 10, pady = 10)


    def login(self):
        print("Hello")
    
    def view(self):

        self.clearWindow()

  

        button1 = customtkinter.CTkButton(master = self.frame,
                                          text = "Daily Log",
                                          command = self.DailyLog,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button1.grid (row = 1, column = 0, padx = 10, pady = (10, 5))

        button2 = customtkinter.CTkButton(master = self.frame,
                                          text = "View",
                                          command = self.login,
                                          height = 30,
                                          width = 120,
                                          fg_color = "#d7c5db",
                                          corner_radius = 25)
        button2.grid (row = 1, column = 1, padx = 10, pady = (10, 5))


        button3 = customtkinter.CTkButton(master = self.frame,
                                          text = "Analytics",
                                          command = self.Analytics,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button3.grid (row = 1, column = 2, padx = 10, pady = (10, 5))

        page = viewpage.ViewPage(self.frame)
        page.grid(row=2, column=0, columnspan=3, padx = 10, pady = (0,10), sticky="nswe")


    def Analytics(self):
        self.clearWindow()


  
        button1 = customtkinter.CTkButton(master = self.frame,
                                          text = "Daily Log",
                                          command = self.DailyLog,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button1.grid (row = 1, column = 0, padx = 10, pady = (10, 5))

        button2 = customtkinter.CTkButton(master = self.frame,
                                          text = "View",
                                          command = self.view,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button2.grid (row = 1, column = 1, padx = 10, pady = (10, 5))


        button3 = customtkinter.CTkButton(master = self.frame,
                                          text = "Analytics",
                                          command = self.login,
                                          height = 30,
                                          width = 120,
                                          fg_color = "#d7c5db",
                                          corner_radius = 25)
        button3.grid (row = 1, column = 2, padx = 10, pady = (10, 5))


    def DailyLog(self):
        self.clearWindow()
     


        button1 = customtkinter.CTkButton(master = self.frame,
                                          text = "Daily Log",
                                          command = self.login,
                                          height = 30,
                                          width = 120,
                                          fg_color = "#d7c5db",
                                          corner_radius = 25)
        button1.grid (row = 1, column = 0, padx = 10, pady = 10)

        button2 = customtkinter.CTkButton(master = self.frame,
                                          text = "View",
                                          command = self.view,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button2.grid (row = 1, column = 1, padx = 10, pady = 10)


        button3 = customtkinter.CTkButton(master = self.frame,
                                          text = "Analytics",
                                          command = self.Analytics,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button3.grid (row = 1, column = 2, padx = 10, pady = 10)

        
        
    def clearWindow(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
            
root = customtkinter.CTk()
app = file_manage(root)
root.mainloop()
