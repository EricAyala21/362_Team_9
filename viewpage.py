import customtkinter

class ViewPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.logDetail = customtkinter.CTkFrame(self)
        self.logDetail.pack(expand=True, side="right", fill="both", padx=10, pady=10)
        self.logDetail.grid_rowconfigure((0,2), weight=1)
        self.logDetail.grid_rowconfigure((1,3,4), weight=2)
        self.logDetail.grid_columnconfigure((0,1,2,3), weight=1)

        self.DTLabel = customtkinter.CTkLabel(self.logDetail, text="Driving Time")
        self.DTLabel.grid(row=0, column=0, columnspan=2, padx=10, sticky="sw")

        self.DTInput = customtkinter.CTkEntry(self.logDetail)
        self.DTInput.grid(row=1, column=0, columnspan=2, padx=10, sticky="nswe")

        self.RTLabel = customtkinter.CTkLabel(self.logDetail, text="Resting Time")
        self.RTLabel.grid(row=0, column=2, columnspan=2, padx=10, sticky="sw")

        self.RTInput = customtkinter.CTkEntry(self.logDetail)
        self.RTInput.grid(row=1, column=2, columnspan=2, padx=10, sticky="nswe")

        self.dateLabel = customtkinter.CTkLabel(self.logDetail, text="Date")
        self.dateLabel.grid(row=2, column=0, columnspan=2, padx=10, sticky="sw")

        self.dateInput = customtkinter.CTkEntry(self.logDetail)
        self.dateInput.grid(row=3, column=0, columnspan=2, padx=10, sticky="nswe")

        self.timeLabel = customtkinter.CTkLabel(self.logDetail, text="Time")
        self.timeLabel.grid(row=2, column=2, columnspan=2, padx=10, sticky="sw")
        
        self.timeInput = customtkinter.CTkEntry(self.logDetail)
        self.timeInput.grid(row=3, column=2, columnspan=2, padx=10, sticky="nswe")

        self.updateBtn = customtkinter.CTkButton(self.logDetail, 
                                                 text="UPDATE", 
                                                 command=self.updateDetail)
        self.updateBtn.grid(row=4, column=1, columnspan=2)

        self.resetBtn = customtkinter.CTkButton(self.logDetail, 
                                                width=70, 
                                                height=14, 
                                                command=self.resetDetail,
                                                text="reset", 
                                                text_color="white", 
                                                fg_color="transparent", 
                                                hover_color="Red")
        self.resetBtn.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.selectionFrame = customtkinter.CTkScrollableFrame(self)
        self.selectionFrame.pack(fill="y", side="left", padx=10, pady=10)

        self.entrybtn1 = customtkinter.CTkButton(self.selectionFrame, 
                                                 text="02/26/2025 10:27AM", 
                                                 command=lambda: self.entryDisplay(self.entrybtn1))
        self.entrybtn1.pack(pady=5, fill="x")
        

    def updateDetail(self):
        print("update log ")
    
    def resetDetail(self):
        print("reset")

    def entryDisplay(self, btn):
        print(btn.cget("text"))
