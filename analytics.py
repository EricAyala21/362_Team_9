import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
from custom_date_entry import CustomDateEntry
import datetime
import os

class AnalyticsPage(ctk.CTkFrame):
    # Simple analytics frame showing driving vs resting times
    def __init__(self, master, db_file):
        super().__init__(master)
        # connect to our SQLite logs database
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

        # set up grid: sidebar on left, charts on right
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # build UI panels
        self._make_sidebar()
        self._make_charts()

    def _make_sidebar(self):
        # sidebar for date pickers and buttons
        side = ctk.CTkFrame(self, width=240, fg_color="#ECECEC", corner_radius=8)
        side.grid(row=0, column=0, sticky="ns", padx=(10,5), pady=10)
        side.grid_propagate(False)

        # title label
        title = ctk.CTkLabel(side, text="Select Date Range",
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.grid(row=0, column=0, padx=10, pady=(10,5), sticky="w")

        # start date picker
        self.start_picker = CustomDateEntry(side)
        self.start_picker.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # end date picker
        self.end_picker = CustomDateEntry(side)
        self.end_picker.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # button to refresh charts
        btn_refresh = ctk.CTkButton(side, text="Generate Graphs",
                                    command=self.update_graphs, height=40,
                                    fg_color="#3B8ED0", hover_color="#273366")
        btn_refresh.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # button to save charts
        btn_export = ctk.CTkButton(side, text="Export Graphs",
                                   command=self.export_graphs, height=40,
                                   fg_color="#3B8ED0", hover_color="#273366")
        btn_export.grid(row=4, column=0, padx=10, pady=(0,10), sticky="ew")

    def _make_charts(self):
        # main area for two charts
        frame = ctk.CTkFrame(self, fg_color="#ECECEC", corner_radius=8)
        frame.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=10)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure((0,1), weight=1)

        # line chart: daily driving vs resting
        self.fig1 = Figure(dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_title("Driving vs Resting Time")
        self.ax1.set_xlabel("Date")
        self.ax1.set_ylabel("Hours")
        canvas1 = FigureCanvasTkAgg(self.fig1, master=frame)
        canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas1 = canvas1

        # bar chart: total driving vs resting
        self.fig2 = Figure(dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_title("Total Driving vs Resting Time")
        self.ax2.set_ylabel("Total Hours")
        canvas2 = FigureCanvasTkAgg(self.fig2, master=frame)
        canvas2.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas2 = canvas2

    def update_graphs(self):
        # clear old data
        self.ax1.clear()
        self.ax2.clear()
        # redraw axes titles
        self.ax1.set_title("Driving vs Resting Time")
        self.ax1.set_xlabel("Date")
        self.ax1.set_ylabel("Hours")
        self.ax2.set_title("Total Driving vs Resting Time")
        self.ax2.set_ylabel("Total Hours")

        # get dates from pickers
        start = self.start_picker.get_date()
        end   = self.end_picker.get_date()
        if not start or not end:
            # show message if dates invalid
            self.ax1.text(0.5, 0.5, "Please pick valid dates.", ha='center')
            self.fig1.tight_layout(pad=3)
            self.canvas1.draw()
            return

        # query between those dates
        s = start.strftime("%Y-%m-%d")
        e = end.strftime("%Y-%m-%d")
        sql = ("SELECT timestamp, drivetime, resttime FROM logs "
               "WHERE date(timestamp) BETWEEN ? AND ? ORDER BY timestamp;")
        rows = self.cur.execute(sql, (s, e)).fetchall()

        if not rows:
            # no data case
            self.ax1.text(0.5, 0.5, "No data in this range.", ha='center')
            self.fig1.tight_layout(pad=3)
            self.canvas1.draw()
            return

        # split data
        dates = [datetime.datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S").date() for r in rows]
        drive = [r[1] for r in rows]
        rest  = [r[2] for r in rows]

        # plot line chart
        self.ax1.plot(dates, drive, label="Driving", color="#3B8ED0", linewidth=2)
        self.ax1.plot(dates, rest,  label="Resting", color="#FF6F61", linewidth=2)
        self.ax1.legend()
        self.fig1.tight_layout(pad=3)
        self.canvas1.draw()

        # plot bar chart of totals
        self.ax2.bar(["Driving", "Resting"], [sum(drive), sum(rest)],
                     color=["#3B8ED0", "#FF6F61"], edgecolor="#333")
        self.fig2.tight_layout(pad=3)
        self.canvas2.draw()

    def export_graphs(self):
        # save both figures as PNGs
        folder = os.path.join(os.getcwd(), "exports")
        os.makedirs(folder, exist_ok=True)
        path1 = os.path.join(folder, "driving_vs_resting_time.png")
        self.fig1.savefig(path1)
        path2 = os.path.join(folder, "total_driving_vs_resting_time.png")
        self.fig2.savefig(path2)
        # let the user know
        tk.messagebox.showinfo("Export Complete",
                               f"Saved:\n{path1}\n{path2}")
