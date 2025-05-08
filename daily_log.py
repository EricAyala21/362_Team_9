import customtkinter as ctk
import sqlite3
from time import strftime

import custom_methods
from log_entry   import LogEntry
from sql_manager import SqlManager
from tkinter import messagebox


class DailyLog(ctk.CTkFrame):
    def __init__(self, master, filename):
        super().__init__(master)
        self.filename = filename

        # try to hook up to sqlite db file
        try:
            self.con = sqlite3.connect(filename)
            self.cur = self.con.cursor()
        except Exception:
            print(f"ugh, couldn’t open DB: {filename}")
            return

        # main grid: 2 equal columns
        self.grid_columnconfigure((0, 1), weight=1, uniform="col")
        self.grid_rowconfigure(0, weight=1)

        # build left/right sides
        self._build_left_panel()
        self._build_right_panel()


    def _build_left_panel(self):
        # left side = driving/resting inputs + Save
        left = ctk.CTkFrame(self, fg_color="transparent")
        left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        # Driving time label + entry
        ctk.CTkLabel(left, text="Driving Time", font=("Helvetica", 16))\
            .grid(row=0, column=0, sticky="w", pady=(0,5))
        self.dt_entry = ctk.CTkEntry(left, width=200, height=36)
        self.dt_entry.grid(row=1, column=0, sticky="ew", pady=(0,15))

        # Resting time label + entry
        ctk.CTkLabel(left, text="Resting Time", font=("Helvetica", 16))\
            .grid(row=2, column=0, sticky="w", pady=(0,5))
        self.rt_entry = ctk.CTkEntry(left, width=200, height=36)
        self.rt_entry.grid(row=3, column=0, sticky="ew", pady=(0,20))

        # Save button
        ctk.CTkButton(
            left,
            text="Save",
            width=120,
            height=36,
            corner_radius=8,
            command=self._on_save
        ).grid(row=4, column=0, pady=(0,10))


    def _build_right_panel(self):
        # right side = time/date display + custom checkbox
        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        # Time label + entry (readonly by default)
        ctk.CTkLabel(right, text="Time", font=("Helvetica", 16))\
            .grid(row=0, column=0, sticky="w", pady=(0,5))
        self.time_entry = ctk.CTkEntry(right, width=200, height=36, justify="center")
        self.time_entry.grid(row=1, column=0, sticky="ew", pady=(0,15))
        self._set_current_time()

        # Date label + entry (readonly by default)
        ctk.CTkLabel(right, text="Date", font=("Helvetica", 16))\
            .grid(row=2, column=0, sticky="w", pady=(0,5))
        self.date_entry = ctk.CTkEntry(right, width=200, height=36, justify="center")
        self.date_entry.grid(row=3, column=0, sticky="ew", pady=(0,15))
        self._set_current_date()

        # checkbox to allow custom time/date
        self.custom_cb = ctk.CTkCheckBox(right, text="Custom Time", command=self._toggle_custom)
        self.custom_cb.grid(row=4, column=0, sticky="w")


    def _set_current_time(self):
        # slap current time into entry
        now = strftime("%H:%M")
        self.time_entry.insert(0, now)
        self.time_entry.configure(state="readonly")


    def _set_current_date(self):
        # slap current date into entry
        today = strftime("%m/%d/%Y")
        self.date_entry.insert(0, today)
        self.date_entry.configure(state="readonly")


    def _toggle_custom(self):
        # allow user to edit time/date if box is ticked
        new_state = "normal" if self.custom_cb.get() else "readonly"
        self.time_entry.configure(state=new_state)
        self.date_entry.configure(state=new_state)


    def _validate_inputs(self):
        # get values from entries
        t = self.time_entry.get()
        d = self.date_entry.get()
        dt = self.dt_entry.get()
        rt = self.rt_entry.get()

        # check time format
        if not custom_methods.checkTime(t):
            messagebox.showerror("Invalid Time", "Please enter time as HH:MM")
            return False

        # check date format
        if not custom_methods.checkDate(d):
            messagebox.showerror("Invalid Date", "Please enter date as MM/DD/YYYY")
            return False

        # check numeric inputs
        try:
            float(dt)
            float(rt)
        except ValueError:
            # change the title/text to your custom time‑format message
            messagebox.showerror("Invalid Time", "Please enter time as HH:MM")
            return False

        return True



    def _on_save(self):
        # do nothing if validation fails
        if not self._validate_inputs():
            return

        # build and save a LogEntry
        ts = f"{self.date_entry.get()} {self.time_entry.get()}"
        entry = LogEntry(
            timestamp=LogEntry.create_timestamp(ts),
            drivetime=float(self.dt_entry.get()),
            resttime=float(self.rt_entry.get())
        )
        SqlManager(self.filename).add_entry(entry)

        messagebox.showinfo(
            "Your data was saved","Saved",
            parent=self.master  
     )
            

        # clear fields for next entry
        self.dt_entry.delete(0, ctk.END)
        self.rt_entry.delete(0, ctk.END)

        if not self.custom_cb.get():
            self.time_entry.configure(state="normal")
            self.date_entry.configure(state="normal")
            self.time_entry.delete(0, ctk.END)
            self.date_entry.delete(0, ctk.END)
            self._set_current_time()
            self._set_current_date()
        else:
            # uncheck and lock again
            self.custom_cb.deselect()
            self._toggle_custom()


       

        


        