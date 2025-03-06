import customtkinter
from time import strftime
import tkinter
import viewpage
class Daily_Log(customtkinter.CTkFrame):
    def __init__(self, master):

        super().__init__(master)
        self.upperDisplay()
        self.lowerDisplay()

    #upper half of the frame    
    def upperDisplay(self):
        # will hold the current time
        self.time_string = strftime('%H:%M:%S %p')

        self.logDetail = customtkinter.CTkFrame(self)

        self.logDetail.pack(expand=True, side="top", fill="both", padx=10, pady=10)
        #amount of rows in the grid evenly distributed
        self.logDetail.grid_rowconfigure((0,1,2,3), weight=1)
        #amount of columns in the grid with two different sizes
        self.logDetail.grid_columnconfigure(0, weight=6)
        self.logDetail.grid_columnconfigure(1, weight=4)

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
        self.RTInput.grid(row=3, column=0,  padx=2,pady = 5, sticky="n")

        #Time Display
        self.timeDetail = customtkinter.CTkLabel(self.logDetail, text = "Current Time and Date", font = ("arial",24), justify = "center",padx=50,pady = 10)
        self.timeDetail.grid(row = 0, column = 1,padx = 10)

        self.TimeLabel = customtkinter.CTkLabel(self.logDetail, text = self.time_string, font = ("arial",18), justify = "center",padx=50,pady = 10)
        self.TimeLabel.grid(row = 1, column = 1,padx = 10)
        

        #save Botton and check box
        self.saveButton = customtkinter.CTkButton(self.logDetail, text = "Save",command = self.save(),height=20,width=100)
        self.saveButton.grid(column = 1, row =3 ,padx = 10, pady = 5, sticky = "se")
        
        self.timeCheckBox = customtkinter.CTkCheckBox(self.logDetail, width = 5,height = 5,text = "Custom Time",command= self.checked())
        self.timeCheckBox.grid(column = 1, row =3 ,padx = (20,10), pady = 5, sticky = "sw")
        #auto update for the time
        self.TimeLabel.after(100,self.current_time())

    #Is the bottom half of the frame
    def lowerDisplay(self):
        self.logTime = customtkinter.CTkFrame(self)
        self.logTime.pack(expand=True, side="bottom", fill="both", padx=10, pady=(2,10))
        self.logTime.grid_columnconfigure((0,1,2,3), weight=1)
        self.logTime.grid_rowconfigure((0,1),weight =2)
        #Label and input for Time
        self.customTime  =customtkinter.CTkLabel(self.logTime, text= "Time",font = ("arial",20),justify = "center", padx = 30,pady = 10)
        self.customTime.grid(row = 0,column=1,padx=10,pady=2, sticky = "nw")

        self.timeInput = customtkinter.CTkEntry(self.logTime)
        self.timeInput.grid(row=1, column=1,  padx=2,pady = 2, sticky="nws")
        #Label and input for Date
        self.customDate  =customtkinter.CTkLabel(self.logTime, text= "Date",font = ("arial",20),justify = "center", padx = 55,pady = 10)
        self.customDate.grid(row = 0,column=2,padx=10,pady=2, sticky = "ne")

        self.dateInput = customtkinter.CTkEntry(self.logTime)
        self.dateInput.grid(row=1, column=2,  padx=2,pady = 2, sticky="nes")
    # Updates the Label to automatically update every 100 milliseconds
    def current_time(self):
        self.TimeLabel.configure(text = self.time_string)
            


                
            
    
    #will determine whether the check box is checked to determine whether to allow a custom time input
    def checked(self):
        print("Checked")

    #will save the information into the viewpage array
    def save(self):
        size = len(viewpage.ViewPage(self).logEntries)    
        print(size)     





       

        


        

