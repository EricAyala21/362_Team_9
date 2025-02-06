import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog







class file_manage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("560x350")
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        self.file_Names = []
        self.setup_gui()

    def setup_gui(self):
        
        frame = customtkinter.CTkFrame(master=root)

        frame.pack(pady =20,padx = 60, fill = "both", expand = True)



     

  

        button1 = customtkinter.CTkButton(master = frame,
                                          text = "Daily Log",
                                          command = self.login,
                                          height = 50,
                                          
                                          width = 120,
                                          corner_radius = 25)
        button1.grid (row = 1, column = 0, padx = 10, pady = 10)

        button2 = customtkinter.CTkButton(master = frame,
                                          text = "View",
                                          command = self.login,
                                          height = 50,
                                          width = 120,
                                          fg_color = "#d7c5db",
                                          corner_radius = 25)
        button2.grid (row = 1, column = 2, padx = 10, pady = 10)


        button3 = customtkinter.CTkButton(master = frame,
                                          text = "Analytics",
                                          command = self.login,
                                          height = 50,
                                          width = 120,
                                          corner_radius = 25)
        button3.grid (row = 1, column = 3, padx = 10, pady = 10)


    def login(self):
        print("Hello")
    
        
        

root = customtkinter.CTk()
app = file_manage(root)
root.mainloop()
