import customtkinter
import re
from datetime import datetime as dt

class ViewPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.ENTRY_COLOR = "#3B8ED0"
        self.ENTRY_COLOR2 = "#273366"

        # store the entries data we have
        self.logEntries=["02/26/2025 12:35 12 10",
                         "02/25/2025 09:16 8 9",
                         "02/24/2025 22:33 10 12",
                         "01/18/2025 08:43 5 7",
                         "12/07/2024 18:00 12 9",
                         "12/01/2024 16:26 8 5",
                         "11/30/2024 17:53 8 13",
                         "10/13/2024 15:00 5 10",
                         "09/06/2024 11:27 13 9",
                         "05/27/2024 06:28 8 9"]
        # selected entry button from the list
        """self.btnSelected = None
        self.entrySelected = None"""
        self.indexSelected = -1

        self.initDetailDisplay()
        self.initListDisplay()
        
    
    # right side of the view page will show the detail of a log entry and provide the ability to edit it
    def initDetailDisplay(self):
        self.detailFrame = customtkinter.CTkFrame(self)
        self.detailFrame.pack(side="right", fill="both", padx=(0,10), pady=10)
        self.detailFrame.grid_rowconfigure((0,2), weight=1)
        self.detailFrame.grid_rowconfigure((1,3,4), weight=2)
        self.detailFrame.grid_columnconfigure((0,1,2,3), weight=1)

        self.DTLabel = customtkinter.CTkLabel(self.detailFrame, text="Driving Time")
        self.DTLabel.grid(row=0, column=0, columnspan=2, padx=5, sticky="sw")

        self.DTInput = customtkinter.CTkEntry(self.detailFrame)
        self.DTInput.grid(row=1, column=0, columnspan=2, padx=5, sticky="nwe")

        self.RTLabel = customtkinter.CTkLabel(self.detailFrame, text="Resting Time")
        self.RTLabel.grid(row=0, column=2, columnspan=2, padx=5, sticky="sw")

        self.RTInput = customtkinter.CTkEntry(self.detailFrame)
        self.RTInput.grid(row=1, column=2, columnspan=2, padx=5, sticky="nwe")

        self.dateLabel = customtkinter.CTkLabel(self.detailFrame, text="Date")
        self.dateLabel.grid(row=2, column=0, columnspan=2, padx=5, sticky="sw")

        self.dateInput = customtkinter.CTkEntry(self.detailFrame)
        self.dateInput.grid(row=3, column=0, columnspan=2, padx=5, sticky="nwe")

        self.timeLabel = customtkinter.CTkLabel(self.detailFrame, text="Time")
        self.timeLabel.grid(row=2, column=2, columnspan=2, padx=5, sticky="sw")
        
        self.timeInput = customtkinter.CTkEntry(self.detailFrame)
        self.timeInput.grid(row=3, column=2, columnspan=2, padx=5, sticky="nwe")

        self.updateBtn = customtkinter.CTkButton(self.detailFrame, 
                                                 text="UPDATE",
                                                 width=50, 
                                                 command=self.update_button_click)
        self.updateBtn.grid(row=4, column=3, columnspan=1, padx=(0,5), sticky="we")

        self.resetBtn = customtkinter.CTkButton(self.detailFrame, 
                                                width=40, 
                                                height=14, 
                                                command=self.entryDisplay,
                                                text="reset", 
                                                text_color="white", 
                                                fg_color="transparent", 
                                                hover_color="#555555")
        self.resetBtn.grid(row=4, column=1, padx=(0,10), pady=10, sticky="w")
        self.deleteBtn = customtkinter.CTkButton(self.detailFrame, 
                                                width=40, 
                                                height=14, 
                                                command=self.delete_button_click,
                                                text="delete",
                                                text_color="white", 
                                                fg_color="transparent", 
                                                hover_color="Red")
        self.deleteBtn.grid(row=4, column=0, padx=(10,0), pady=10, sticky="w")


    # initiate left side for search and select from a list of log entries
    def initListDisplay(self):
        self.searchbox = customtkinter.CTkEntry(self, placeholder_text="Enter Date")
        self.searchbox.pack(fill="x", side="top", padx=10, pady=(10,5))
        self.searchbox.bind("<KeyRelease>", self.searchbox_on_key_press)

        self.listFrame = customtkinter.CTkScrollableFrame(self)
        self.listFrame.pack(fill="both", side="left", padx=10, pady=(0,10), expand=True)

        # buttons for entries in listFrame
        self.entryBtns = []
        # Initialize the list of buttons with all available log entries
        for entry in self.logEntries:
            details = re.split(r" ", entry, maxsplit=3)
            btn = customtkinter.CTkButton(self.listFrame, 
                                          text = details[0] + " " + details[1],
                                          corner_radius = 0,
                                          hover_color = self.ENTRY_COLOR2)
            btn.configure(command = lambda b = btn: self.selectEntry(b))
            btn.pack(fill="x")
            self.entryBtns.append(btn)
    

    # Show buttons with index in entries, hide others
    def updateListDisplay(self, entryIndexes):
        for btn in self.entryBtns:
            btn.pack_forget()

        for i in entryIndexes:
            self.entryBtns[i].pack(fill="x")


    # update button event that update selected entry and corresponding display
    def update_button_click(self):
        if(self.indexSelected == -1):
            return

        timestamp_str = ""
        FORMAT_STR = "%m/%d/%Y %H:%M"
        timestamp = None
        try:
            timestamp = dt.strptime(self.dateInput.get() + " " + self.timeInput.get(), FORMAT_STR)
            timestamp_str = timestamp.strftime(FORMAT_STR)
        except ValueError:
            #TODO error message or popup error window for invalid
            return
        # the user changed the date&time and currently contains a different entry with the same date&time
        if(timestamp_str != self.entryBtns[self.indexSelected].cget("text") 
        and self.findIndex(timestamp_str) != -1):
            #TODO error message for trying to generate duplicate entry with the same date&time
            return

        dt_str = self.DTInput.get().strip()
        rt_str = self.RTInput.get().strip()
        try:
            if dt_str == "":
                dt_str = "0"
            elif int(dt_str) < 0:
                raise ValueError()
            if rt_str == "":
                rt_str = "0"
            elif int(rt_str) < 0:
                raise ValueError()
        except ValueError:
            #TODO error message or popup error window for invalid
            return
        
        entry = timestamp_str + " " + dt_str + " " + rt_str      
        self.logEntries[self.indexSelected] = entry
        self.entryBtns[self.indexSelected].configure(text=timestamp_str)

    
    # delete currently selected entry and update UI
    def delete_button_click(self):
        if(self.indexSelected == -1): # if nothing selected
            return
        print("delete button clicked for entry " + str(self.indexSelected))
        #TODO popup window to confirm delete, set cofirmed[0] to true if user confirmed deletion
        confirmed = [True]
        if confirmed[0] == False:
            return
        self.entryBtns[self.indexSelected].destroy()
        self.entryBtns.pop(self.indexSelected)
        self.logEntries.pop(self.indexSelected)
        self.indexSelected = -1
        self.removeDetail()

    # return the index of the first entry that start with input str
    def findIndex(self, str):
        print("finding index for string " + str)
        for i in range(len(self.logEntries)):
            print("checking " + self.logEntries[i])
            if self.logEntries[i].startswith(str):
                return i
        return -1
    
    # update UI and record when select an entry by clicking button btn
    def selectEntry(self, btn):
        # if there is a selected entry, change its color back like others
        if self.indexSelected != -1:
            self.entryBtns[self.indexSelected].configure(fg_color=self.ENTRY_COLOR)
        # upate indexSelected
        self.indexSelected = self.findIndex(btn.cget("text"))
        print("click on entry " + str(self.indexSelected) + btn.cget("text"))
        # update corresponding detail display
        self.entryDisplay()
        # update the newly selected button color
        btn.configure(fg_color=self.ENTRY_COLOR2)


    # remove content in entry detail input boxes
    def removeDetail(self):
        self.dateInput.delete(0, len(self.dateInput.get()))
        self.timeInput.delete(0, len(self.timeInput.get()))
        self.DTInput.delete(0, len(self.DTInput.get()))
        self.RTInput.delete(0, len(self.RTInput.get()))


    # update the content in entry detail input boxes depends on self.entrySelected
    def entryDisplay(self):
        elements = re.split(r" ", self.logEntries[self.indexSelected])
        self.removeDetail()
        self.dateInput.insert(0, elements[0])
        self.timeInput.insert(0, elements[1])
        self.DTInput.insert(0, elements[2])
        self.RTInput.insert(0, elements[3])


    # return a list entries in self.logEntries that start with str 
    def findEntries(self, str):
        result = []
        for i in range(len(self.logEntries)):
            if self.logEntries[i].startswith(str):
                result.append(i)
        return result


    # search box key press event that show the matching entry buttons
    def searchbox_on_key_press(self, event):
        self.updateListDisplay(self.findEntries(self.searchbox.get()))