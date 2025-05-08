import customtkinter
import daily_log
import viewpage
import analytics
import sqlite3

class Users(customtkinter.CTkFrame):
    def __init__(self, master, callback=None):
        super().__init__(master)
        self.callback = callback  # Function to call when user is selected
        self.sqlManager = None
        self.file_Names = ["TestingFile.db"]
        self.position = 0

        # Center frame layout
        self.grid_columnconfigure((0, 2), weight=1)  # side spacing
        self.grid_columnconfigure(1, weight=2)       # center content
        self.grid_rowconfigure(1, weight=1)

        self.leftFrame()

    def leftFrame(self):
        self.title = customtkinter.CTkLabel(self, text="Choose a user:", font=("Helvetica", 28))
        self.title.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="new")

        self.list_frame = customtkinter.CTkScrollableFrame(self)
        self.list_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="Add User", command=self.inputFunction)
        self.button.grid(row=2, column=1, padx=10, pady=(10, 20), sticky="ew")

        self.reorderButtons()

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

    def create_entry_button(self, fileName):
        btn = customtkinter.CTkButton(self.list_frame, text=fileName, height=40)
        btn.configure(command=lambda b=btn: self.entry_button_clicked(fileName))
        return btn

    def entry_button_clicked(self, fileName):
        for indx, entry in enumerate(self.file_Names):
            if fileName == entry.replace(".db", ""):
                self.position = indx
                print(f"User '{fileName}' selected")
                if self.callback:
                    self.callback(self.file_Names[self.position])  # Pass db filename to callback

    def addUser(self):
        usersFile = self.user_input + ".db"
        self.file_Names.append(usersFile)
        print(self.file_Names)
        self.reorderButtons()

    def reorderButtons(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        for idx, entry in enumerate(self.file_Names):
            btn = self.create_entry_button(entry.replace(".db", ""))
            btn.grid(row=idx, column=0, padx=0, pady=5, sticky="ew")
        self.list_frame.grid_columnconfigure(0, weight=1)