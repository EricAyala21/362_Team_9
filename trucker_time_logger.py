import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import daily_log
import viewpage
import sqlite3



class file_manage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("650x350")
        self.root.minsize(630, 300)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        
        self.file_Names = []
        self.con = None # sql connection
        self.cur = None # sql cursor
        self.setup_data()

        self.frame = ""
        self.setup_gui()


    def setup_data(self):
        #TODO look through available data file / ask user for file input
        # temporary database for test and development purpose
        self.file_Names = ["temp.db", "test.db"]
        self.con = sqlite3.connect(self.file_Names[0])
        self.cur = self.con.cursor()
        # create a table named logs if not exists. datetime set to primary key for fast lookup
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS logs(
                         timestamp TEXT PRIMARY KEY, 
                         drivetime FLOAT, 
                         resttime FLOAT)""")
        # create an index for logs based on the datetime to enhance sorting
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp)")

        # starting entries for test only
        # store the entries data we have
        self.log_entries=[["2025/02/26 12:35", 12, 10],
                         ["2025/02/25 09:16", 8, 9],
                         ["2025/02/24 22:33", 10, 12],
                         ["2025/01/18 08:43", 5, 7],
                         ["2024/12/07 18:00", 12, 9],
                         ["2024/12/01 16:26", 8, 5],
                         ["2024/11/30 17:53", 8, 13],
                         ["2024/10/13 15:00", 5, 10],
                         ["2024/09/06 11:27", 13, 9],
                         ["2024/05/27 06:28", 8, 9]]
        self.cur.executemany("INSERT OR IGNORE INTO logs VALUES(?, ?, ?)", self.log_entries)
        self.con.commit()

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

        page = viewpage.ViewPage(self.frame, self.file_Names[1]) # TODO maybe can change to the selected file?
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
        page = daily_log.Daily_Log(self.frame, self.file_Names[0]) # temporarily use the first file
        page.grid(row=2, column=0, columnspan=3, padx = 10, pady = (0,10), sticky="nswe")

        
        
    def clearWindow(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
            
root = customtkinter.CTk()
app = file_manage(root)
root.mainloop()
