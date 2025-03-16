import customtkinter
from time import strftime
import tkinter
import sqlite3

class Daily_Log(customtkinter.CTkFrame):
    def __init__(self, master, filename):

        super().__init__(master)

        # setup control of the sql database file, 
        # assume the table logs(datetime, drivetime, resttime) always exists
        try:
            self.con = sqlite3.connect(filename)
            self.cur = self.con.cursor()
        except:
            print("sql file connection failed: " + filename)
            return

        self.upperDisplay()
        self.lowerDisplay()

    #upper half of the frame    
    def upperDisplay(self):
        # will hold the current time
        self.time_string = strftime('%H:%M')
        self.date_string = strftime('%D')

        self.logDetail = customtkinter.CTkFrame(self)

        self.logDetail.pack(expand=True, side="left", fill="both", padx=10, pady=10)
        #amount of rows in the grid evenly distributed
        self.logDetail.grid_rowconfigure((0,1,2,3), weight=1)
        self.logDetail.grid_rowconfigure((4), weight=2)

        #amount of columns in the grid with two different sizes
        self.logDetail.grid_columnconfigure(0, weight=3)


        #label for Driving time
        self.DTLabel = customtkinter.CTkLabel(self.logDetail, text="Driving Time",font = ("arial",18),justify = "center",padx = 50,pady=10)
        self.DTLabel.grid(row=0, column=0, padx=5, sticky="s")
        #Input box for driving time
        self.DTInput = customtkinter.CTkEntry(self.logDetail,width = 250,height = 20)
        self.DTInput.grid(row=1, column=0, padx=5,pady=5, sticky="n")
        #Label for Resting Time
        self.RTLabel = customtkinter.CTkLabel(self.logDetail, text="Resting Time",font = ("arial",18),justify = "center",padx = 50,pady=10)
        self.RTLabel.grid(row=2, column=0,  padx=5, sticky="s")
        #Text box for resting Time
        self.RTInput = customtkinter.CTkEntry(self.logDetail,width = 250,height = 20)
        self.RTInput.grid(row=3, column=0,  padx=2, sticky="n")
        self.RTInput.grid(row=3, column=0,  padx=2,pady = 5, sticky="n")

        

        #save Botton and check box
        self.saveButton = customtkinter.CTkButton(self.logDetail, text = "Save",command = lambda:self.save(),height=20,width=100)
        self.saveButton.grid(column = 0, row =4 ,padx = 10, pady = 5, sticky = "ns")
  



        


    #Is the bottom half of the frame
    def lowerDisplay(self):
        self.logTime = customtkinter.CTkFrame(self)
        self.logTime.pack(expand=True, side="right", fill="both", padx=10, pady=(10,10))
        self.logTime.grid_columnconfigure((0,1), weight=1)
        self.logTime.grid_rowconfigure((0,1,2,3,4),weight =1)

        #Label and input for Time
        self.customTime  =customtkinter.CTkLabel(self.logTime, text= "Time",font = ("arial",20),justify = "center", padx = 30,pady = 10)
        self.customTime.grid(row = 0,column=1,padx=(2,0),pady=2, sticky = "ns")

        self.timeInput = customtkinter.CTkEntry(self.logTime)
        self.timeInput.grid(row=1, column=1,  padx=(10,0),pady = (0,0), sticky="n")
        self.current_time()#gets the time in the entry box
        
        #Label and input for Date
        self.customDate  =customtkinter.CTkLabel(self.logTime, text= "Date",font = ("arial",20),justify = "center", padx = 55,pady = 10)
        self.customDate.grid(row = 2,column=1,padx=10,pady=(20,0), sticky = "nse")


        self.dateInput = customtkinter.CTkEntry(self.logTime)
        self.dateInput.grid(row=3, column=1,  padx=(10,0),pady = 2, sticky="s")
        self.current_day()#gets the date in the entrybox

        #check box for a custom time
        self.checkBox = customtkinter.CTkCheckBox(self.logTime,text  ="Custom Time",width = 10, height = 10,command =self.checked)
        self.checkBox.grid(row = 4, column  =1, padx=10,pady=(10,0),sticky = "ns")

    

    # gets the time and sets the state of the entry to readonly
    def current_time(self):
        self.timeInput.insert(0, self.time_string)
        self.timeInput.configure(state = "readonly")
    #gets the date and sets the state of the entry to readonly      
    def current_day(self):
        self.dateInput.insert(0, self.date_string)
        self.dateInput.configure(state="readonly")
            


                

                
    #will check if the box is checked so it can allow the user to edit the text boxs for time and date
    def checked(self):
        if self.checkBox.cget("state") == "disabled":
            self.timeInput.configure(state = "disabled")
            self.dateInput.configure(state = "disabled")
        else:
            self.dateInput.configure(state = "normal")
            self.timeInput.configure(state = "normal")

    #will save the information into the database
    def save(self):
        size = len(viewpage.ViewPage(self).logEntries)    
        print(size)     





       

        


        

