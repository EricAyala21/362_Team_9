import customtkinter

class ViewPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.initDetailDisplay()
        self.logEntries=["02/21/2025", "02/25/2025", "02/26/2025"]
        self.initListDisplay(self.logEntries)
        
    
    # right side of the view page will show the detail of a log entry and provide the ability to edit it
    def initDetailDisplay(self):
        self.logDetail = customtkinter.CTkFrame(self)
        self.logDetail.pack(side="right", fill="both", padx=(0,10), pady=10)
        self.logDetail.grid_rowconfigure((0,2), weight=1)
        self.logDetail.grid_rowconfigure((1,3,4), weight=2)
        self.logDetail.grid_columnconfigure((0,1,2,3), weight=1)

        self.DTLabel = customtkinter.CTkLabel(self.logDetail, text="Driving Time")
        self.DTLabel.grid(row=0, column=0, columnspan=2, padx=5, sticky="sw")

        self.DTInput = customtkinter.CTkEntry(self.logDetail)
        self.DTInput.grid(row=1, column=0, columnspan=2, padx=5, sticky="nwe")

        self.RTLabel = customtkinter.CTkLabel(self.logDetail, text="Resting Time")
        self.RTLabel.grid(row=0, column=2, columnspan=2, padx=5, sticky="sw")

        self.RTInput = customtkinter.CTkEntry(self.logDetail)
        self.RTInput.grid(row=1, column=2, columnspan=2, padx=5, sticky="nwe")

        self.dateLabel = customtkinter.CTkLabel(self.logDetail, text="Date")
        self.dateLabel.grid(row=2, column=0, columnspan=2, padx=5, sticky="sw")

        self.dateInput = customtkinter.CTkEntry(self.logDetail)
        self.dateInput.grid(row=3, column=0, columnspan=2, padx=5, sticky="nwe")

        self.timeLabel = customtkinter.CTkLabel(self.logDetail, text="Time")
        self.timeLabel.grid(row=2, column=2, columnspan=2, padx=5, sticky="sw")
        
        self.timeInput = customtkinter.CTkEntry(self.logDetail)
        self.timeInput.grid(row=3, column=2, columnspan=2, padx=5, sticky="nwe")

        self.updateBtn = customtkinter.CTkButton(self.logDetail, 
                                                 text="UPDATE",
                                                 width=50, 
                                                 command=self.updateDetail)
        self.updateBtn.grid(row=4, column=3, columnspan=1, padx=5, sticky="e")

        self.resetBtn = customtkinter.CTkButton(self.logDetail, 
                                                width=70, 
                                                height=14, 
                                                command=self.resetDetail,
                                                text="reset", 
                                                text_color="white", 
                                                fg_color="transparent", 
                                                hover_color="Red")
        self.resetBtn.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    # initiate left side for search and select from a list of log entries
    def initListDisplay(self, entries):
        self.searchbox = customtkinter.CTkEntry(self, placeholder_text="Enter Date")
        self.searchbox.pack(fill="x", side="top", padx=10, pady=(10,0))

        self.selectionFrame = customtkinter.CTkScrollableFrame(self)
        self.selectionFrame.pack(fill="both", side="left", padx=10, pady=10, expand=True)

        self.entryBtns = []
        for entry in self.logEntries:
            self.btn = customtkinter.CTkButton(self.selectionFrame, 
                                          text=entry, 
                                          command=lambda: self.entryDisplay(self.btn),
                                          corner_radius=0,
                                          hover_color="#275c55")
            self.btn.pack(pady=2, fill="x")
            self.entryBtns.append(self.btn)

    def updateDetail(self):
        print("update log ")
    
    def resetDetail(self):
        print("reset")

    def entryDisplay(self, btn):
        print(btn.cget("text"))
