import customtkinter
import datetime as dt
from custom_date_entry import CustomDateEntry
from log_entry import LogEntry
from sql_manager import SqlManager
from custom_window import SelectionWindow

class ViewPage(customtkinter.CTkFrame):
    ENTRY_COLOR = ["#eaeaea","#3a3a3a"]
    ENTRY_COLOR2 = ["#aeaeae","#111111"]
    ENTRY_HOVER_COLOR = ["#91c1f5","#273366"]
    DELETE_BTN_COLOR = "transparent"
    DELETE_BTN_HOVER_COLOR = "black"
    DELETE_BTN_TEXT_COLOR = "#b20000"
    TRANSPARENT = "transparent"

    def __init__(self, master, sql_filename):
        super().__init__(master)

        self.columnconfigure(index = 1, weight = 1)
        self.rowconfigure(index = 3, weight = 1)

        # open sql file
        self.sqlManager = None
        try: 
            self.sqlManager = SqlManager(sql_filename)
        except: # open sql file failed
            self.pop_msg("ViewPage: Sql db file open failed.")
            print("Sql file open failed")
            return
        
        # get the timestamp list from database
        self.log_entries = self.sqlManager.get_timestamps()

        # record the last modification, at index 0, is the original LogEntry. 
        # index 1 is the new timestamp if last change made is an update. nothing if it is a delete
        self.last_change = []

        # selected entry index in the list log_entries
        self.selected_index = -1

        self.init_detail_display() # initiate elements on the right side of the page
        self.init_list_display() # initiate elements on the left side of the page
    
    # right side of the view page will show the detail of the selected log entry and provide the ability to edit it
    def init_detail_display(self):
        self.detail_frame = customtkinter.CTkFrame(self)
        self.detail_frame.grid(row = 0, rowspan = 4, column = 2, sticky = "nswe", padx=(0,10), pady=10)
        self.detail_frame.grid_rowconfigure((0,2), weight=1)
        self.detail_frame.grid_rowconfigure((1,3,4), weight=2)
        self.detail_frame.grid_columnconfigure((0,1,2,3), weight=1)
        #a loading display that cover the detail area to prevent modification while changing content
        self.detail_cover = customtkinter.CTkFrame(self) 
        self.detail_cover.grid(row = 0, rowspan = 4, column = 2, sticky = "nswe", padx=(0,10), pady=10)
        self.detail_cover.grid_remove()
        loading_label = customtkinter.CTkLabel(self.detail_cover, text = "Loading...")
        loading_label.pack(expand = True, fill = "both")


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

        self.date_input = CustomDateEntry(self.detail_frame)
        self.date_input.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nw")

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
                                                text_color="black", 
                                                fg_color=self.TRANSPARENT, 
                                                hover_color="#ffffff")

        self.delete_btn = customtkinter.CTkButton(self.detail_frame, 
                                                width=40, 
                                                height=14, 
                                                command=self.delete_button_click,
                                                text="delete",
                                                text_color=self.DELETE_BTN_TEXT_COLOR, 
                                                fg_color=self.DELETE_BTN_COLOR, 
                                                hover_color=self.DELETE_BTN_HOVER_COLOR)
        self.delete_btn.grid(row=4, column=0, padx=(10,0), pady=10, sticky="w")


    # initiate left side for search and select from a list of log entries, it will interact
    def init_list_display(self):
        self.begin_date_label = customtkinter.CTkLabel(self, text = "From")
        self.begin_date_label.grid(row = 0, column = 0, padx=(5,0), pady=(10,0), sticky="e")

        self.begin_date_input = CustomDateEntry(self)
        self.begin_date_input.grid(row = 0, column = 1, padx=5, pady=(10,0), sticky="w")

        self.end_date_label = customtkinter.CTkLabel(self, text = "To")
        self.end_date_label.grid(row = 1, column = 0, padx=(5,0), pady=(0,5), sticky="e")

        self.end_date_input = CustomDateEntry(self)
        self.end_date_input.grid(row = 1, column = 1, padx=5, pady=(0,5), sticky="w")

        self.search_button = customtkinter.CTkButton(self, text="Search"
                                                     , command=self.search_button_click, width=70)
        self.search_button.grid(row = 2, column = 1, padx = (0,10), pady=(0,5), sticky = "ew")

        self.clear_button = customtkinter.CTkButton(self, text="clear"
                                                     , command=self.clear_button_click
                                                     , width=20)
        self.clear_button.grid(row = 2, column = 0, padx = (10,5), pady=(0,5))

        self.list_frame = customtkinter.CTkScrollableFrame(self)
        self.list_frame.grid(row = 3, column = 0, columnspan = 2, padx=10, pady=(0,10), sticky = "nswe")
        self.list_frame.columnconfigure(0, weight=1)
        self.list_cover = customtkinter.CTkFrame(self)
        self.list_cover.grid(row = 3, column = 0, columnspan = 2, padx=10, pady=(0,10), sticky = "nswe")
        self.list_cover.grid_remove()
        loading_label = customtkinter.CTkLabel(self.list_cover, text = "Loading...")
        loading_label.pack(expand = True, fill = "both")

        # Initialize the list of buttons with all available log entries, the button will be stored in log_entries[1]
        n = 0
        for entry in self.log_entries:
            btn = self.create_entry_button(LogEntry.to_str(entry[0]))
            btn.grid(row=n, column = 0, sticky = "ew")
            entry.append(btn)
            n += 1
        
    
    def create_entry_button(self, entry_datetime: str):
        """ create a new entry in the entry list UI """
        btn = customtkinter.CTkButton(self.list_frame, 
                                      text = entry_datetime,
                                      text_color= "black",
                                      corner_radius = 0,
                                      fg_color = self.ENTRY_COLOR,
                                      hover_color = self.ENTRY_HOVER_COLOR)      
        btn.configure(command = (lambda b = btn: self.entry_button_clicked(b)))
        return btn

    def cover(self):
        """cover the list part with a frame called list_cover"""
        # cover the list frame to show it is loading
        self.remove_cover()
        self.list_cover.grid()
        self.detail_cover.grid()

    def remove_cover(self):
        """remove the list cover"""
        self.list_cover.grid_remove()
        self.detail_cover.grid_remove()


    def update_list_display(self, date_range : tuple[dt.datetime]):
        """ Show entry buttons that has a date at or after begin_date and also at or before the end_date,
        from future date to down to current date."""
        n = 0
        begin_date = date_range[0]
        end_date = date_range[1]
        for i in range(len(self.log_entries)):
            if ((begin_date == None or self.log_entries[i][0] >= begin_date) 
                and (end_date == None or self.log_entries[i][0] <= end_date)
                or i == self.selected_index):
                self.log_entries[i][1].grid(row = n, sticky="we")
                n += 1
            else:
                self.log_entries[i][1].grid_forget()

    def reorder_entries(self, idx: int):
        """ 
        Maintain the descending order of the log_entries when there is a change at index idx.
        Meanwhile, update selected_index and detail display to be the entry of the selected_indx
        """      
        self.update()  
        # change the color of currently selected entry (if any)
        self.deselect_current_entry()
        # swapping toward the front
        while(idx > 0 and self.log_entries[idx][0] > self.log_entries[idx-1][0]):
            temp = self.log_entries[idx]
            self.log_entries[idx] = self.log_entries[idx - 1]
            self.log_entries[idx-1] = temp
            idx -= 1
        # swapping toward the back of the list
        while(idx < len(self.log_entries) - 1 and self.log_entries[idx][0] < self.log_entries[idx + 1][0]):
            temp = self.log_entries[idx]
            self.log_entries[idx] = self.log_entries[idx + 1]
            self.log_entries[idx+1] = temp
            idx += 1

        # update list display
        self.update_list_display(self.get_date_range())
        # select the newly ordered entry
        self.select_entry(idx)
        

    
    def update_button_click(self):
        """ update button event that update selected entry and corresponding display """
        if(self.selected_index == -1):
            return
        self.cover()
        # old timestamp
        old_timestamp = self.log_entries[self.selected_index][0]
        # new entry
        new_entry = LogEntry()
        try:
            new_entry.timestamp = LogEntry.from_date_and_time(self.date_input.get_date()
                                                              , self.time_input.get().strip())
        except:
            self.pop_msg("Invalid date or time."
                         +"\nDate format mm/dd/yyyy."
                         +"\nTime uses the 24 hour format HH:MM.")
            self.display_entry()
            self.remove_cover()
            return
        
        #error message for trying to generate duplicate entry with the same date&time
        if(new_entry.timestamp != old_timestamp 
           and self.find_index(LogEntry.to_str(new_entry.timestamp)) != -1):
            self.pop_msg("Entry with the same date & time already exist!"
                         +"\nChange cancelled.")
            self.display_entry()
            self.remove_cover()
            return
        
        # convert drive time and rest time input to floats
        dt_str = self.drive_time_input.get().strip()
        rt_str = self.rest_time_input.get().strip()
        try:
            if dt_str != "":
                new_entry.drivetime = float(dt_str)
            if rt_str != "":
                new_entry.resttime = float(rt_str)
        except:
            #TODO error message or popup error window for invalid
            self.pop_msg("Drive time and Rest time error. Decimal numbers only.")
            self.display_entry()
            self.remove_cover()
            return
        
        old_entry = self.sqlManager.get_entry(old_timestamp)
        #No change is made
        if(new_entry.timestamp == old_entry.timestamp
           and new_entry.drivetime == old_entry.drivetime
           and new_entry.resttime == old_entry.resttime):
            self.pop_msg("No Change Made.")
            self.remove_cover()
            return

        #Get user confirmation
        msg_list = [
            ["Update to the new entry?"]
            , ["", "Old", "New"]
            , ["Date & Time:", str(LogEntry.to_str(old_timestamp))
               , str(LogEntry.to_str(new_entry.timestamp))]
            , ["Drive Time:", str(old_entry.drivetime), str(new_entry.drivetime)]
            , ["Rest Time:", str(old_entry.resttime), str(new_entry.resttime)]
        ]
        if(not self.get_action_confirm(msg_list)):
            self.pop_msg("Update Cancelled.")
            self.remove_cover()
            return
        
        # save the change made to self.last_change and show the undo button
        self.last_change = [old_entry, new_entry.timestamp]
        self.show_undo_btn()

        # update the new entry information in sql file
        self.sqlManager.update_entry(old_timestamp, new_entry)

        # update the new entry information in log_entries
        self.log_entries[self.selected_index][0] = new_entry.timestamp
        self.log_entries[self.selected_index][1].configure(text=new_entry.get_timestamp_str())

        # adjust any display needed
        self.reorder_entries(self.selected_index)

        print("update button click on entry: " + str(self.selected_index))
        print("  previous content: ", end="")
        print(self.last_change)
        self.remove_cover()
    

    def delete_button_click(self):
        """ 
        delete currently selected entry and update UI 
        """
        if(self.selected_index == -1): # if nothing selected
            return
        print("delete button clicked for entry " + str(self.selected_index))
        self.display_entry()
        self.cover()
        #popup window to confirm delete
        msg_list = [
                     ["Delete the following entry?"]
                     , ["Date:", str(LogEntry.to_str(self.date_input.get_date())).split()[0]]
                     , ["Time:", self.time_input.get()]
                     , ["Drive Time:", self.drive_time_input.get()]
                     , ["Rest Time:", self.rest_time_input.get()]
                ]
        if(not self.get_action_confirm(msg_list=msg_list)):
            # Notify the user the deletion is cancelled
            self.pop_msg("Delete Cancelled")
            self.remove_cover()
            return

        
        # delete it from database file and store the deleted entry
        self.last_change = [self.sqlManager.delete_entry(self.log_entries[self.selected_index][0])]
        self.show_undo_btn()

        # remove the deleted entry from log_entries and corresponding display
        self.log_entries.pop(self.selected_index)[1].destroy()
        self.selected_index = -1
        self.remove_detail()

        self.pop_msg("Entry Removed")
        print("delete button clicked, # of entry after delete: " + str(len(self.log_entries)))
        print("  deleted content: ", end = "")
        print(self.last_change)
        self.remove_cover()


    def find_index(self, s: str):
        """ return the index of the first entry that contain string s """
        s = LogEntry.create_timestamp(s)
        low = 0
        high = len(self.log_entries) - 1
        while(low <= high):
            mid = int(low + (high - low) / 2)
            if s == self.log_entries[mid][0]:
                return mid
            elif s < self.log_entries[mid][0]:
                low = mid + 1
            else:
                high = mid - 1
        return -1
    
    def entry_button_clicked(self, btn: customtkinter.CTkButton):
        """ reponse when an entry button btn in the entry list is clicked """
        self.deselect_current_entry()
        self.select_entry(self.find_index(btn.cget("text")))


    def deselect_current_entry(self):
        """change currently selected entry button color back to original.
        note: does not remove its detail or change selected index to -1"""
        if self.selected_index == -1:
            return
        self.log_entries[self.selected_index][1].configure(fg_color=self.ENTRY_COLOR)
    
    def select_entry(self, idx: int):
        """ update selected button color and detail display to select the entry with index idx"""
        # upate selected_index
        self.selected_index = idx
        # update corresponding detail display
        self.display_entry()
        # update the newly selected button color
        self.log_entries[idx][1].configure(fg_color=self.ENTRY_COLOR2)

    
    def remove_detail(self):
        """ remove content in entry detail input boxes """
        self.date_input.clear()
        self.time_input.delete(0, len(self.time_input.get()))
        self.drive_time_input.delete(0, len(self.drive_time_input.get()))
        self.rest_time_input.delete(0, len(self.rest_time_input.get()))


    def display_entry(self):
        """ update the content in entry detail input boxes depends on self.selected_entry """
        self.remove_detail()

        entry = self.sqlManager.get_entry(self.log_entries[self.selected_index][0])
        print("display entry: " + str(entry))

        self.date_input.set_date(entry.timestamp)
        self.time_input.insert(0, entry.get_time_str())
        self.drive_time_input.insert(0, entry.drivetime)
        self.rest_time_input.insert(0, entry.resttime)
        
    def get_date_range(self):
        """Return start date and end date as datetime instance separately"""
        start_date = self.begin_date_input.get_date()
        if(start_date != None):
            start_date = LogEntry.from_date_and_time(start_date, "0:0")
        end_date = self.end_date_input.get_date()
        if(end_date != None):
            end_date = LogEntry.from_date_and_time(end_date, "0:0")
        return (start_date, end_date)
    

    def search_button_click(self):
        """ search and display matching entry buttons within the range defined """
        self.cover()
        self.update_list_display(self.get_date_range())
        self.remove_cover()

    
    def show_undo_btn(self):
        """ show the undo button """
        self.undo_btn.grid(row=4, column=1, padx=(0,10), pady=10, sticky="w")


    def undo_button_click(self):
        """ action when undo button is click, restore to before the last change were made"""
        print("undo button clicked, last_change in record: ", end='')
        print(self.last_change)
        self.cover()
        # the last change made is a delete
        if (len(self.last_change) == 1):
            #popup window to confirm the change
            msg_list = [
                ["Restore the following entry?" ]
                , ["Date & time:", str(LogEntry.to_str(self.last_change[0].timestamp))]
                , ["Drive time:", str(self.last_change[0].drivetime)]
                , ["Rest time:", str(self.last_change[0].resttime)]
            ]
            print("Undo button: confirm to undo last delete.")
            if(not self.get_action_confirm(msg_list=msg_list)):
                self.pop_msg("Undo Cancelled.")
                self.remove_cover()
                return # do nothing if the action is cancelled
            
            btn = self.create_entry_button(LogEntry.to_str(self.last_change[0].timestamp))
            btn.grid(row = len(self.log_entries), column=0, sticky="ew")
            self.log_entries.append([self.last_change[0].timestamp, btn])
            self.sqlManager.add_entry(self.last_change[0])
            self.reorder_entries(len(self.log_entries) - 1)
            self.update_list_display(self.get_date_range())

        # the last change made is a modification
        elif (len(self.last_change) == 2):
            # find and display the entry that we are going to make change
            idx = self.find_index(LogEntry.to_str(self.last_change[1]))
            self.deselect_current_entry()
            self.select_entry(idx)
            # popup window to compare and confirm the change
            msg_list = [
                ["Restore the following entry to before its last update?"]
                , ["","Entry","Previous"]
                , ["Date & Time:", str(self.log_entries[idx][1].cget("text"))
                   , str(self.last_change[0].get_timestamp_str())]
                , ["Drive time:", str(self.drive_time_input.get())
                   , str(self.last_change[0].get_drivetime())]
                , ["Rest time:", str(self.rest_time_input.get())
                   , str(self.last_change[0].get_resttime())]
            ]
            print("Undo button: store from previous update")

            if(not self.get_action_confirm(msg_list)):
                self.pop_msg("Undo Cancelled.")
                self.remove_cover() # remove the loading screen
                return # action cancelled
            
            # Made the change in UI and database
            self.sqlManager.update_entry(timestamp=self.last_change[1], entry=self.last_change[0])
            self.log_entries[idx][0] = self.last_change[0].timestamp
            self.log_entries[idx][1].configure(text = LogEntry.to_str(self.log_entries[idx][0]))
            self.reorder_entries(idx)

        self.last_change = []
        self.undo_btn.grid_forget()
        self.pop_msg("Undo Complete.")
        self.remove_cover()

    def clear_button_click(self):
        """Methods when clear button on the list sections is clicked, will remove all the content in range selection
        and show all the entries, 
        and will remove the right-side display details and deselect all entries"""
        self.cover()
        self.begin_date_input.clear()
        self.end_date_input.clear()
        self.update_list_display(self.get_date_range())
        self.deselect_current_entry()
        self.remove_detail()
        self.selected_index = -1
        self.remove_cover()

    def pop_msg(self, msg : str, width = 350, height = 150):
        """Pop up window to show a message"""
        popup = SelectionWindow(title = "Message", options=["Done"], var=customtkinter.StringVar())
        popup.geometry(f'{width}x{height}')
        popup.center()
        popup.set_content([[msg]],[1])
        popup.focus()
        popup.grab_set()
        self.wait_window(popup)

    def get_action_confirm(self, msg_list : list[list[str]]):
        """generate a popup window with equally-spaced button of options to select.
        msg_list is a 2D list of string that each string will be organized in row and column 
        in the popup window. If the first row is a list of single string, that single string 
        will occupies the whole row.
        Return True if the yes button is clicked, 
        False if thescancel button is clicked or no selection is made."""
        confirmation = customtkinter.StringVar()
        confirmation.set("Cancel")
        popup = None
        #construct the column weight list needed for msg_list
        columns = []
        for row in msg_list:
            while len(columns) < len(row):
                columns.append(1)
        #popup window until a selection is made by the user
        header = None
        if(len(msg_list[0]) == 1):
            header = msg_list[0][0]
            msg_list = msg_list[1:]
        if(popup == None or not popup.winfo_exists()):
            popup = SelectionWindow(title="Action Confirm"
                                    , options = ["Yes", "Cancel"]
                                    , var = confirmation)
            popup.set_content(msg_list, columns, header)
            popup.center()
            popup.focus()
            popup.grab_set()
            self.wait_window(popup)
        else:
            popup.focus()
        print("Confirmation: " + confirmation.get())
        return confirmation.get() == "Yes"
        