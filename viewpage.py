import tkinter
import customtkinter
import sqlite3
import tkcalendar
import re
from datetime import datetime as dt
import custom_methods

class ViewPage(customtkinter.CTkFrame):
    ENTRY_COLOR = "#3B8ED0"
    ENTRY_COLOR2 = "#273366"

    def __init__(self, master, sql_filename):
        super().__init__(master)

        # open sql file
        self.sql_filename = sql_filename
        self.con = None 
        self.cur = None
        try: 
            self.con = sqlite3.connect(sql_filename)
            self.cur = self.con.cursor()
        except: # TODO open sql file failed
            print("Sql file open failed")
            return
        
        # get the datetime list from data file, assume the table logs always exists
        sql_entries = self.cur.execute("SELECT datetime FROM logs ORDER BY datetime DESC").fetchall()
        self.log_entries = []
        for e in sql_entries:
            self.log_entries.append([e[0]])

        # record the last modification, at index 0, is the original date and time string;
        # 1 is the old driving time, 2 is old rest time, 3 is the new date and time string
        self.last_change = []

        # selected entry index in the list log_entries
        self.selected_index = -1

        self.init_detail_display() # initiate elements on the right side of the page
        self.init_list_display() # initiate elements on the left side of the page
    
    def __del__(self):
        self.cur.execute("DROP TABLE logs")
        self.con.close()
    
    # right side of the view page will show the detail of the selected log entry and provide the ability to edit it
    def init_detail_display(self):
        self.detail_frame = customtkinter.CTkFrame(self)
        self.detail_frame.pack(side="right", fill="both", padx=(0,10), pady=10)
        self.detail_frame.grid_rowconfigure((0,2), weight=1)
        self.detail_frame.grid_rowconfigure((1,3,4), weight=2)
        self.detail_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.drive_time_label = customtkinter.CTkLabel(self.detail_frame, text="Driving Time")
        self.drive_time_label.grid(row=0, column=0, columnspan=2, padx=5, sticky="sw")

        self.drive_time_input = customtkinter.CTkEntry(self.detail_frame)
        self.drive_time_input.grid(row=1, column=0, columnspan=2, padx=5, sticky="nwe")

        self.rest_time_label = customtkinter.CTkLabel(self.detail_frame, text="Resting Time")
        self.rest_time_label.grid(row=0, column=2, columnspan=2, padx=5, sticky="sw")

        self.rest_time_input = customtkinter.CTkEntry(self.detail_frame)
        self.rest_time_input.grid(row=1, column=2, columnspan=2, padx=5, sticky="nwe")

        self.date_label = customtkinter.CTkLabel(self.detail_frame, text="Date")
        self.date_label.grid(row=2, column=0, columnspan=2, padx=5, sticky="sw")

        self.date_input = customtkinter.CTkEntry(self.detail_frame)
        self.date_input.grid(row=3, column=0, columnspan=2, padx=5, sticky="nwe")

        self.time_label = customtkinter.CTkLabel(self.detail_frame, text="Time")
        self.time_label.grid(row=2, column=2, columnspan=2, padx=5, sticky="sw")
        
        self.time_input = customtkinter.CTkEntry(self.detail_frame)
        self.time_input.grid(row=3, column=2, columnspan=2, padx=5, sticky="nwe")

        self.update_btn = customtkinter.CTkButton(self.detail_frame, 
                                                 text="UPDATE",
                                                 width=50, 
                                                 command=self.update_button_click)
        self.update_btn.grid(row=4, column=3, columnspan=1, padx=(0,5), sticky="we")

        self.undo_btn = customtkinter.CTkButton(self.detail_frame, 
                                                width=40, 
                                                height=14, 
                                                command=self.undo_button_click,
                                                text="undo", 
                                                text_color="white", 
                                                fg_color="transparent", 
                                                hover_color="#555555")

        self.delete_btn = customtkinter.CTkButton(self.detail_frame, 
                                                width=40, 
                                                height=14, 
                                                command=self.delete_button_click,
                                                text="delete",
                                                text_color="white", 
                                                fg_color="gray", 
                                                hover_color="Red")
        self.delete_btn.grid(row=4, column=0, padx=(10,0), pady=10, sticky="w")


    # initiate left side for search and select from a list of log entries, it will interact
    def init_list_display(self):
        self.searchbox = customtkinter.CTkEntry(self, placeholder_text="Enter Date")
        self.searchbox.pack(fill="x", side="top", padx=10, pady=(10,5))
        self.searchbox.bind("<KeyRelease>", self.searchbox_on_key_press)

        self.list_frame = customtkinter.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", side="left", padx=10, pady=(0,10), expand=True)
        self.list_frame.columnconfigure(0, weight=1)

        # Initialize the list of buttons with all available log entries, the button will be stored in log_entries[1]
        n = 0
        for entry in self.log_entries:
            btn = self.create_entry_button(entry[0])
            btn.grid(row=n, column = 0, sticky = "ew")
            n += 1
            entry.append(btn)

    
    def create_entry_button(self, entry_datetime: str):
        btn = customtkinter.CTkButton(self.list_frame, 
                                      text = entry_datetime,
                                      corner_radius = 0,
                                      hover_color = self.ENTRY_COLOR2)      
        btn.configure(command = (lambda b = btn: self.entry_button_clicked(b)))
        return btn

    
    def update_list_display(self, starting_str=""):
        """ Show entry buttons with text starting with starting_str, hide otherwise """
        n = 0
        for i in range(len(self.log_entries)):
            if self.log_entries[i][0].startswith(starting_str) or i == self.selected_index:
                self.log_entries[i][1].grid(row = n, sticky="we")
                n += 1
            else:
                self.log_entries[i][1].grid_forget()
        

    
    def reorder_entries(self, idx):
        """ 
        Maintain the descending order of the log_entries when there is a change at index idx.
        Meanwhile, update selected_index and detail display to be the entry of the selected_indx
        """
        # change the color of currently selected entry (if any)
        self.deselect_current_entry()

        # swapping toward the front
        while(idx > 0 and self.log_entries[idx][0] > self.log_entries[idx-1][0]):
            temp = self.log_entries[idx]
            self.log_entries[idx] = self.log_entries[idx - 1]
            self.log_entries[idx-1] = temp
            idx -= 1
        # swapping toward the back of the list
        while(idx + 1 < len(self.log_entries) and self.log_entries[idx][0] < self.log_entries[idx + 1][0]):
            temp = self.log_entries[idx]
            self.log_entries[idx] = self.log_entries[idx + 1]
            self.log_entries[idx+1] = temp
            idx += 1

        # update list display
        self.update_list_display(self.searchbox.get())
        # select the newly ordered entry
        self.select_entry(idx)

    
    def update_button_click(self):
        """ update button event that update selected entry and corresponding display """
        if(self.selected_index == -1):
            return

        # old string for date and time
        old_datetime = self.log_entries[self.selected_index][0]
        # new string for date and time
        datetime_str = ""
        # datetime object generated from user input
        current_datetime = None
        try:
            current_datetime = custom_methods.str_to_datetime(self.date_input.get() + " " + self.time_input.get())
            datetime_str = custom_methods.datetime_to_str(current_datetime)
        except ValueError:
            self.display_entry()
            #TODO error message or popup error window for invalid
            return
        
        # the user changed the date&time and currently contains a different entry with the same date&time
        if(datetime_str != old_datetime
        and self.find_index(datetime_str) != -1):
            #TODO error message for trying to generate duplicate entry with the same date&time
            return
        
        # convert drive time and rest time input to floats
        dt_str = self.drive_time_input.get().strip()
        rt_str = self.rest_time_input.get().strip()
        dt = 0
        rt = 0
        try:
            if dt_str == "":
                dt = 0
            else:
                dt = float(dt_str)
            if rt_str == "":
                rt = 0
            else:
                rt = float(rt_str)
        except:
            #TODO error message or popup error window for invalid
            return
        
        # save the change made to self.last_change and show the undo button
        self.last_change = [old_datetime]
        self.last_change.extend(self.cur.execute("SELECT drivetime, resttime FROM logs WHERE datetime = ?", 
                                self.last_change).fetchone())
        self.last_change.append(datetime_str)
        self.show_undo_btn()

        # update the new entry information in sql file
        self.cur.execute("UPDATE logs SET datetime = ?, drivetime = ?, resttime = ? WHERE datetime = ?",
                         [datetime_str, dt, rt, old_datetime])
        self.con.commit()

        # update the new entry information in log_entries
        self.log_entries[self.selected_index][0] = datetime_str
        self.log_entries[self.selected_index][1].configure(text=datetime_str)

        # adjust any display needed
        self.reorder_entries(self.selected_index)

        print("update button click on entry: " + str(self.selected_index))
        print("  previous content: ", end="")
        print(self.last_change)
    

    def delete_button_click(self):
        """ 
        delete currently selected entry and update UI 
        """
        if(self.selected_index == -1): # if nothing selected
            return
        print("delete button clicked for entry " + str(self.selected_index))
        #TODO popup window to confirm delete, set cofirmed[0] to true if user confirmed deletion
        confirmed = [True]
        if confirmed[0] == False:
            return
        
        # store the change made
        self.last_change = [self.log_entries[self.selected_index][0]]
        self.last_change.extend(self.cur.execute("SELECT drivetime, resttime FROM logs WHERE datetime = ?",
                                                 self.last_change).fetchone())
        self.show_undo_btn()

        # delete it from database file
        self.last_change.extend(self.cur.execute("DELETE FROM logs WHERE datetime = ?",
                                                 (self.last_change[0],)))
        self.con.commit()

        # remove the deleted entry from log_entries and corresponding display
        self.log_entries.pop(self.selected_index)[1].destroy()
        self.selected_index = -1
        self.remove_detail()

        print("delete button clicked, # of entry after delete: " + str(len(self.log_entries)))
        print("  deleted content: ", end = "")
        print(self.last_change)


    
    def find_index(self, s: str):
        """ return the index of the first entry that start with input string s """
        for i in range(len(self.log_entries)):
            if self.log_entries[i][0].startswith(s):
                return i
        return -1
    
    def entry_button_clicked(self, btn: customtkinter.CTkButton):
        self.deselect_current_entry()
        self.select_entry(self.find_index(btn.cget("text")))

    def deselect_current_entry(self):
        """change currently selected entry button color back to original.
        note: does not remove its detail or change selected index to -1"""
        if self.selected_index == -1:
            return
        self.log_entries[self.selected_index][1].configure(fg_color=self.ENTRY_COLOR)
    
    def select_entry(self, idx: int):
        """ update button color and detail display to select the entry with index idx"""
        # upate selected_index
        self.selected_index = idx
        # update corresponding detail display
        self.display_entry()
        # update the newly selected button color
        self.log_entries[idx][1].configure(fg_color=self.ENTRY_COLOR2)

    
    def remove_detail(self):
        """ remove content in entry detail input boxes """
        self.date_input.delete(0, len(self.date_input.get()))
        self.time_input.delete(0, len(self.time_input.get()))
        self.drive_time_input.delete(0, len(self.drive_time_input.get()))
        self.rest_time_input.delete(0, len(self.rest_time_input.get()))


    def display_entry(self):
        """ update the content in entry detail input boxes depends on self.selected_entry """
        self.remove_detail()

        date_and_time = re.split(r" ", self.log_entries[self.selected_index][0])
        self.date_input.insert(0, date_and_time[0])
        self.time_input.insert(0, date_and_time[1])
        
        date_and_time = (self.log_entries[self.selected_index][0],)
        query = self.cur.execute("SELECT drivetime, resttime FROM logs WHERE datetime = ?", 
                                 date_and_time).fetchone()
        self.drive_time_input.insert(0, query[0])
        self.rest_time_input.insert(0, query[1])


    def searchbox_on_key_press(self, event):
        """ search box event that show the matching entry buttons """
        self.update_list_display(self.searchbox.get())

    
    def show_undo_btn(self):
        """ show the undo button """
        self.undo_btn.grid(row=4, column=1, padx=(0,10), pady=10, sticky="w")


    def undo_button_click(self):
        """ action when undo button is click, restore to before the last change were made"""
        print("undo button clicked, last_change in record: ", end='')
        print(self.last_change)
        # the last change made is a delete
        if (len(self.last_change) == 3):
            btn = self.create_entry_button(self.last_change[0])
            btn.grid(row = len(self.log_entries), column=0, sticky="ew")
            self.log_entries.append([self.last_change[0], btn])
            self.cur.execute("INSERT OR IGNORE INTO logs VALUES (?, ?, ?)", self.last_change)
            self.con.commit()
            self.reorder_entries(len(self.log_entries) - 1)
            self.update_list_display(self.searchbox.get())
        # the last change made is a modification
        elif (len(self.last_change) == 4):
            idx = self.find_index(self.last_change[3])
            self.log_entries[idx][0] = self.last_change[0]
            self.log_entries[idx][1].configure(text = self.last_change[0])
            self.cur.execute("UPDATE logs SET datetime = ?, drivetime = ?, resttime = ? WHERE datetime = ?", self.last_change)
            self.con.commit()
            self.reorder_entries(idx)

        self.last_change = []
        self.undo_btn.grid_forget()
        