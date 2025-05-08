import customtkinter
import datetime as dt
from custom_date_entry import CustomDateEntry
from log_entry import LogEntry
from sql_manager import SqlManager
from custom_window import SelectionWindow

class ViewPage(customtkinter.CTkFrame):
    ENTRY_COLOR = ["#eaeaea", "#3a3a3a"]
    ENTRY_COLOR2 = ["#aeaeae", "#111111"]
    ENTRY_HOVER_COLOR = ["#91c1f5", "#273366"]
    DELETE_BTN_COLOR = "transparent"
    DELETE_BTN_HOVER_COLOR = "black"
    DELETE_BTN_TEXT_COLOR = "#b20000"
    TRANSPARENT = "transparent"

    def __init__(self, master, sql_filename):
        super().__init__(master)
        self.columnconfigure(index=1, weight=1)
        self.rowconfigure(index=3, weight=1)

        try:
            self.sqlManager = SqlManager(sql_filename)
        except:
            print("Sql file open failed")
            return

        self.log_entries = self.sqlManager.get_timestamps()
        self.last_change = []
        self.selected_index = -1

        self.init_detail_display()
        self.init_list_display()

    def init_detail_display(self):
        self.detail_frame = customtkinter.CTkFrame(self)
        self.detail_frame.grid(row=0, rowspan=4, column=2, sticky="nswe", padx=(0, 10), pady=10)
        self.detail_frame.grid_rowconfigure((0, 2), weight=1)
        self.detail_frame.grid_rowconfigure((1, 3, 4), weight=2)
        self.detail_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.drive_time_label = customtkinter.CTkLabel(self.detail_frame, text="Driving Time")
        self.drive_time_label.grid(row=0, column=0, columnspan=2, sticky="sw")

        self.drive_time_input = customtkinter.CTkEntry(self.detail_frame)
        self.drive_time_input.grid(row=1, column=0, columnspan=2, sticky="nwe")

        self.rest_time_label = customtkinter.CTkLabel(self.detail_frame, text="Resting Time")
        self.rest_time_label.grid(row=0, column=2, columnspan=2, sticky="sw")

        self.rest_time_input = customtkinter.CTkEntry(self.detail_frame)
        self.rest_time_input.grid(row=1, column=2, columnspan=2, sticky="nwe")

        self.date_label = customtkinter.CTkLabel(self.detail_frame, text="Date")
        self.date_label.grid(row=2, column=0, columnspan=2, sticky="sw")

        self.date_input = CustomDateEntry(self.detail_frame)
        self.date_input.grid(row=3, column=0, columnspan=2, sticky="nwe")

        self.time_label = customtkinter.CTkLabel(self.detail_frame, text="Time")
        self.time_label.grid(row=2, column=2, columnspan=2, sticky="sw")

        self.time_input = customtkinter.CTkEntry(self.detail_frame)
        self.time_input.grid(row=3, column=2, columnspan=2, sticky="nwe")

        self.update_btn = customtkinter.CTkButton(self.detail_frame, text="UPDATE", command=self.update_button_click)
        self.update_btn.grid(row=4, column=3, sticky="we")

        self.delete_btn = customtkinter.CTkButton(
            self.detail_frame,
            text="delete",
            text_color=self.DELETE_BTN_TEXT_COLOR,
            fg_color=self.DELETE_BTN_COLOR,
            hover_color=self.DELETE_BTN_HOVER_COLOR,
            command=self.delete_button_click
        )
        self.delete_btn.grid(row=4, column=0, padx=(10, 0), pady=10, sticky="w")

    def init_list_display(self):
        self.begin_date_label = customtkinter.CTkLabel(self, text="From")
        self.begin_date_label.grid(row=0, column=0, padx=(5, 0), pady=(10, 0), sticky="e")

        self.begin_date_input = CustomDateEntry(self)
        self.begin_date_input.grid(row=0, column=1, padx=5, pady=(10, 0), sticky="w")

        self.end_date_label = customtkinter.CTkLabel(self, text="To")
        self.end_date_label.grid(row=1, column=0, padx=(5, 0), pady=(0, 5), sticky="e")

        self.end_date_input = CustomDateEntry(self)
        self.end_date_input.grid(row=1, column=1, padx=5, pady=(0, 5), sticky="w")

        self.search_button = customtkinter.CTkButton(self, text="Search", command=self.search_button_click)
        self.search_button.grid(row=2, column=1, padx=(0, 10), pady=(0, 5), sticky="ew")

        self.clear_button = customtkinter.CTkButton(self, text="Clear", command=self.clear_button_click)
        self.clear_button.grid(row=2, column=0, padx=(10, 5), pady=(0, 5), sticky="w")

        self.list_frame = customtkinter.CTkScrollableFrame(self)
        self.list_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nswe")
        self.list_frame.columnconfigure(0, weight=1)

        for idx, entry in enumerate(self.log_entries):
            btn = self.create_entry_button(LogEntry.to_str(entry[0]))
            btn.grid(row=idx, column=0, sticky="ew")
            entry.append(btn)

    def create_entry_button(self, entry_datetime: str):
        btn = customtkinter.CTkButton(
            self.list_frame,
            text=entry_datetime,
            fg_color=self.ENTRY_COLOR,
            hover_color=self.ENTRY_HOVER_COLOR,
            text_color="black",
            corner_radius=0
        )
        btn.configure(command=lambda b=btn: self.entry_button_clicked(b))
        return btn

    def entry_button_clicked(self, btn):
        self.deselect_current_entry()
        self.select_entry(self.find_index(btn.cget("text")))

    def deselect_current_entry(self):
        if self.selected_index == -1:
            return
        self.log_entries[self.selected_index][1].configure(fg_color=self.ENTRY_COLOR)

    def select_entry(self, idx):
        self.selected_index = idx
        self.display_entry()
        self.log_entries[idx][1].configure(fg_color=self.ENTRY_COLOR2)

    def display_entry(self):
        self.date_input.set_date(self.log_entries[self.selected_index][0])
        entry = self.sqlManager.get_entry(self.log_entries[self.selected_index][0])
        self.time_input.delete(0, "end")
        self.drive_time_input.delete(0, "end")
        self.rest_time_input.delete(0, "end")
        self.time_input.insert(0, entry.get_time_str())
        self.drive_time_input.insert(0, entry.drivetime)
        self.rest_time_input.insert(0, entry.resttime)

    def update_button_click(self):
        print("UPDATE button clicked")

    def delete_button_click(self):
        print("DELETE button clicked")

    def search_button_click(self):
        print("SEARCH button clicked")

    def clear_button_click(self):
        print("CLEAR button clicked")


