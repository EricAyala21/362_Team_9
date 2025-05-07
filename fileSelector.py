import customtkinter
import daily_log
import viewpage
import Analytics
import sqlite3

class Users(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.sqlManager = None
        self.file_Names = ["TestingFile.db"]

        self.leftFrame()
        #self.setup_Files()
    def leftFrame(self):
      

        self.button = customtkinter.CTkButton(self,text = "Add User",command = self.inputFunction)
        self.button.grid(row  = 3, column = 1,padx = 5,pady=2,  sticky = "ew")


        self.list_frame = customtkinter.CTkScrollableFrame(self)
        self.list_frame.grid(row = 2 , column = 1, padx = 2,  pady=10 , sticky = "news")

        self.title = customtkinter.CTkLabel(self,text = "Choose a user:",font=("Helvetica",28))
        self.title.grid(row = 0, column = 1, padx = 5, pady = (5,0), sticky ="news")
        n = 0
        for entry in self.file_Names:
            btn = self.create_entry_button(entry.replace(".db",""))
            btn.grid(row = n, column = 0,padx=50,pady =(0,0.8), sticky = "nsew")
            n += 1
    def inputFunction(self):
        self.after_idle(self.show_dialog)
    def show_dialog(self):
        dialog = customtkinter.CTkInputDialog(text="Enter user name:", title="Add User")

        user_input = dialog.get_input()
        if user_input is None or user_input.strip() == "":
            print("Dialog canceled or no input.")
            return
        self.user_input = user_input.strip()
        print("User input:", self.user_input)
        self.addUser()



    def create_entry_button(self,fileName):
        btn = customtkinter.CTkButton(self.list_frame,text = fileName,corner_radius = 5,width = 280, height= 50)
        btn.configure(command = (lambda b = btn: self.entry_button_clicked(fileName)))
        return btn
        
    def entry_button_clicked(self,fileName):
        for indx, entry in enumerate(self.file_Names):
            if fileName == entry.replace(".db", ""):
                self.position = indx

                print(fileName)
                print(entry)
                print(self.position)
                print("Entered daily log")
                self.DailyLog()

    def login(self):
        print("Entered")
    def view(self):

        self.clearWindow()

  

        button1 = customtkinter.CTkButton(self,
                                          text = "Daily Log",
                                          command = self.DailyLog,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button1.grid (row = 1, column = 0, padx = 10, pady = (10, 5))

        button2 = customtkinter.CTkButton(self,
                                          text = "View",
                                          command = self.login,
                                          height = 30,
                                          width = 120,
                                          fg_color = "#d7c5db",
                                          corner_radius = 25)
        button2.grid (row = 1, column = 1, padx = 10, pady = (10, 5))


        button3 = customtkinter.CTkButton(self,
                                          text = "Analytics",
                                          command = self.Analytics,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button3.grid (row = 1, column = 2, padx = 10, pady = (10, 5))

        button4 = customtkinter.CTkButton(self,
                                          text = "Log Out",
                                          command = self.createLogout,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button4.grid (row = 1, column = 3, padx = 10, pady = (10, 5))


        page = viewpage.ViewPage(self, self.file_Names[self.position]) # TODO maybe can change to the selected file?
        page.grid(row=2, column=0, columnspan=5, padx = (50,0), pady = (0,10), sticky="nswe")


    def Analytics(self):
        self.clearWindow()
        print(self.position)

  
        button1 = customtkinter.CTkButton(self,
                                          text = "Daily Log",
                                          command = self.DailyLog,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button1.grid (row = 1, column = 0, padx = 10, pady = (10, 5))

        button2 = customtkinter.CTkButton(self,
                                          text = "View",
                                          command = self.view,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button2.grid (row = 1, column = 1, padx = 10, pady = (10, 5))


        button3 = customtkinter.CTkButton(self,
                                          text = "Analytics",
                                          command = self.login,
                                          height = 30,
                                          width = 120,
                                          fg_color = "#d7c5db",
                                          corner_radius = 25)
        button3.grid (row = 1, column = 2, padx = 10, pady = (10, 5))


        button4 = customtkinter.CTkButton(self,
                                          text = "Log Out",
                                          command = self.createLogout,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button4.grid (row = 1, column = 5, padx = 10, pady = (10, 5))

        page = Analytics.AnalyticsPage(self, self.file_Names[self.position]) # TODO maybe can change to the selected file?
        page.grid(row=3, column=0, columnspan=4, padx = (50,0), pady = (0,10), sticky="nswe")

    def DailyLog(self):
        self.clearWindow()
        self.setup_data()


        button1 = customtkinter.CTkButton(self,
                                          text = "Daily Log",
                                          command = self.login,
                                          height = 30,
                                          width = 120,
                                          fg_color = "#d7c5db",
                                          corner_radius = 25)
        button1.grid (row = 1, column = 0, padx = 10, pady = 10)

        button2 = customtkinter.CTkButton(self,
                                          text = "View",
                                          command = self.view,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button2.grid (row = 1, column = 1, padx = 10, pady = 10)


        button3 = customtkinter.CTkButton(self,
                                          text = "Analytics",
                                          command = self.Analytics,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button3.grid (row = 1, column = 2, padx = 10, pady = 10)


        button4 = customtkinter.CTkButton(self,
                                          text = "Log Out",
                                          command = self.createLogout,
                                          height = 30,
                                          width = 120,
                                          corner_radius = 25)
        button4.grid (row = 1, column = 5, padx = 10, pady = (10, 5))


        page = daily_log.Daily_Log(self, self.file_Names[self.position]) # temporarily use the first file
        page.grid(row=2, column=0, columnspan=4, padx = (50,0), pady = (0,10), sticky="nswe")

        
        
    def clearWindow(self):
        for widgets in self.winfo_children():
            widgets.destroy()

    def setup_data(self):
      
        #TODO look through available data file / ask user for file input
        # temporary database for test and development purpose
        self.con = sqlite3.connect(self.file_Names[self.position])
        print(self.file_Names[self.position])
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
        self.log_entries=[]
        self.cur.executemany("INSERT OR IGNORE INTO logs VALUES(?, ?, ?)", self.log_entries)
        self.con.commit()
   
    def setup_Files(self):
        self.connect = sqlite3.connect("UserFiles.db")
        self.cursor = self.connect.cursor()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS users_files(
                         filename TEXT PRIMARY KEY)""")
        self.files = [("temp2.db")]
        self.cursor.executemany("INSERT OR IGNORE INTO users_files VALUES(?)",self.files,)
        self.connect.commit()

    def addUser(self):
        usersFiles = self.user_input + ".db" 
        self.file_Names.append(usersFiles)
        print(self.file_Names)

        self.reorderButtons()       
        #print(usersFiles)
   
    def reorderButtons(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        n = 0
        for entry in self.file_Names:
            btn = self.create_entry_button(entry.replace(".db",""))
            btn.grid(row = n, column = 0,padx=50,pady =(0,0.8), sticky = "nsew")
            n += 1

    def createLogout(self):
        self.clearWindow()
        self.leftFrame()