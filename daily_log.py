import customtkinter
from time import strftime
import sqlite3
import custom_methods
import viewpage

from log_entry import LogEntry
from sql_manager import SqlManager

class Daily_Log(customtkinter.CTkFrame):
    def __init__(self, master, filename):

        super().__init__(master)
        self.filename = filename
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
        self.date_string = strftime('%m/%d/%Y')

        self.logDetail = customtkinter.CTkFrame(self)

        self.logDetail.pack(expand=True, side="left", fill="both", padx=10, pady=10)
        #amount of rows in the grid evenly distributed
        self.logDetail.grid_rowconfigure((0,1,2,3), weight=1)
        self.logDetail.grid_rowconfigure((4), weight=2)

        #amount of columns in the grid with two different sizes
        self.logDetail.grid_columnconfigure(0, weight=3)


        #label for Driving time
        self.DTLabel = customtkinter.CTkLabel(self.logDetail, text="Driving Time",font = ("Helvetica",18),justify = "center",padx = 50,pady=10)
        self.DTLabel.grid(row=0, column=0, padx=5, sticky="s")
        #Input box for driving time
        self.DTInput = customtkinter.CTkEntry(self.logDetail,width = 250,height = 20)
        self.DTInput.grid(row=1, column=0, padx=2,pady=5, sticky="n")
        #Label for Resting Time
        self.RTLabel = customtkinter.CTkLabel(self.logDetail, text="Resting Time",font = ("Helvetica",18),justify = "center",padx = 50,pady=10)
        self.RTLabel.grid(row=2, column=0,  padx=5, sticky="s")
        #Text box for resting Time
        self.RTInput = customtkinter.CTkEntry(self.logDetail,width = 250,height = 20)
        self.RTInput.grid(row=3, column=0,  padx=2, sticky="n")

        
 
        #save Botton and check box
        self.saveButton = customtkinter.CTkButton(self.logDetail, text = "Save",command = lambda:self.save())
        self.saveButton.grid(column = 0, row =4 ,padx = 10, pady = 5, sticky = "ns")
        self.logDetail.bind('<Configure>',self.resizeUpperDisplay)




        


    #Is the bottom half of the frame
    def lowerDisplay(self):
        self.logTime = customtkinter.CTkFrame(self)
        self.logTime.pack(expand=True, side="right", fill="both", padx=10, pady=(10,10))
        self.logTime.grid_columnconfigure((0,1), weight=1)
        self.logTime.grid_rowconfigure((0,1,2,3,4),weight =1)

        #Label and input for Time
        self.customTime  =customtkinter.CTkLabel(self.logTime, text= "Time",font = ("arial",20),justify = "center", padx = 30,pady = 10)
        self.customTime.grid(row = 0,column=1,padx=(2,0),pady=2, sticky = "ns")

        self.timeInput = customtkinter.CTkEntry(self.logTime,justify = "center")
        self.timeInput.grid(row=1, column=1,  padx=(10,0),pady = (0,0), sticky="n")
        self.current_time()#gets the time in the entry box
        
        #Label and input for Date
        self.customDate  =customtkinter.CTkLabel(self.logTime, text= "Date",font = ("arial",20),justify = "center", padx = 30,pady = 10)
        self.customDate.grid(row = 2,column=1,padx=10,pady=(20,0), sticky = "ns")


        self.dateInput = customtkinter.CTkEntry(self.logTime,justify = "center")
        self.dateInput.grid(row=3, column=1,  padx=(10,0),pady = 2, sticky="s")
        self.current_day()#gets the date in the entrybox

        #check box for a custom time
        self.checkBox = customtkinter.CTkCheckBox(self.logTime,text  ="Custom Time",width = 10, height = 10,command = self.checked)
        self.checkBox.grid(row = 4, column  =1, padx=10,pady=(10,0),sticky = "ns")
        self.logTime.bind('<Configure>',self.resizeTimeView)
    

    # gets the time and sets the state of the entry to readonly
    def current_time(self):
        self.timeInput.insert(0, self.time_string)
        self.timeInput.configure(state = "readonly")
    #gets the date and sets the state of the entry to readonly      
    def current_day(self):
        self.dateInput.insert(0, self.date_string)
        self.dateInput.configure(state="readonly")

    #Will check if the time is in the right format and will output an error if it is wrong
    def checkTimes(self):
        self.TInput = self.timeInput.get()
  
        if custom_methods.checkTime(self.TInput) == True:
            return True
        else:
            print("Theres an error In check Time")
            viewpage.ViewPage.pop_msg(self,"Please input in xx:xx format") 
   
    def checkDates(self):
        self.DInput = self.dateInput.get()

        if custom_methods.checkDate(self.DInput) == True:
            return True
        else:

            viewpage.ViewPage.pop_msg(self,"Error please input in xx/xx/xxxx format") 
            print("Theres an error In check Dates")
            
        
    def checkDInput(self):
        self.dData = self.DTInput.get()
        try:
            if custom_methods.checkTimeInputs(float(self.dData)) == True:
                return True
        except:
            print("Theres an error In DrivingTime")
            viewpage.ViewPage.pop_msg(self,"Error please input a numerical value") 
    

    def checkRInput(self):
        self.RData = self.RTInput.get()
        try:
            if custom_methods.checkTimeInputs(float(self.RData)) == True:
                return True
        except:
            print("Theres an error In Resting Time")
            viewpage.ViewPage.pop_msg(self,"Please input a numerical value") 
        
    #will check if the box is checked so it can allow the user to edit the text boxs for time and date
    def checked(self):#once the check box is in the unchecked position 
        if self.checkBox.get() == 0:
            self.timeInput.configure(state = "disabled")
            self.dateInput.configure(state = "disabled")
            print(self.checkBox.get())
        else:
            self.dateInput.configure(state = "normal")
            self.timeInput.configure(state = "normal")

    #will save the information into the viewpage array
    def save(self):

        if self.checkDates() and self.checkDInput() and self.checkRInput() and self.checkTimes():
            self.timestamp = self.DInput + " "+ self.TInput
            entry = LogEntry(timestamp=LogEntry.create_timestamp(self.timestamp)
                             , drivetime=float(self.DTInput.get())
                             , resttime=float(self.RTInput.get()))
            manager = SqlManager(self.filename)
            manager.add_entry(entry)

            print("entry list after save: ", end='')
            print(self.cur.execute("SELECT timestamp FROM logs").fetchall())
            self.deleteInputs()
            self.checkBox.deselect()
            self.current_time()
            self.current_day()
            viewpage.ViewPage.pop_msg(self,"Your data was saved") 
        else:
            print("Error there is one wrong input")

        
    #deletes the data from the input boxes whether it is in a disabled and a enabled mode    
    def deleteInputs(self):
        if self.timeInput.cget("state") == "readonly":
            self.timeInput.configure(state="normal")
            self.dateInput.configure(state="normal")
            self.timeInput.delete(0,customtkinter.END)
            self.dateInput.delete(0,customtkinter.END)
            self.timeInput.configure(state="readonly")
            self.dateInput.configure(state="readonly")
            self.DTInput.delete(0,customtkinter.END)
            self.RTInput.delete(0,customtkinter.END)
        else:

            self.timeInput.delete(0,customtkinter.END)
            self.dateInput.delete(0,customtkinter.END)
            self.DTInput.delete(0,customtkinter.END)
            self.RTInput.delete(0,customtkinter.END)  
# Resizes the first window based off of the size of the application window

    def resizeTimeView(self,e):
        widgetWidth= e.width
        widgetHeight = e.height
        average = widgetWidth * widgetHeight
        self.timeInput.configure(height=int(widgetHeight) /5,width = int(widgetWidth)/1.5,font = ("Helvetica",int(widgetWidth/14)))
        self.dateInput.configure(height=int(widgetHeight) /5,width = int(widgetWidth)/1.5,font = ("Helvetica",int(widgetWidth/14)))
        self.customTime.configure(font=("Helvetica",int(widgetWidth)/12))
        self.customDate.configure(font=("Helvetica",int(widgetWidth)/12))

# Resizes the first window based off of the size of the application window
    def resizeUpperDisplay(self,e):
        widgetWidth = e.width
        widgetHeight = e.height

        self.DTInput.configure(height =int(widgetHeight)/5,font = ("Helvetica",int(widgetWidth/14)),width = int(widgetWidth)/1.5)
        self.RTInput.configure(height = int(widgetHeight)/5,font = ("Helvetica",int(widgetWidth/14)),width = int(widgetWidth)/1.5)
        self.DTLabel.configure(font=("Helvetica", int(widgetWidth)/16))
        self.RTLabel.configure(font=("Helvetica", int(widgetWidth)/16))
        self.saveButton.configure(width=int(widgetWidth)/2)




       

        


        