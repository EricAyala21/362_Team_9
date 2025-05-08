import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
from custom_date_entry import CustomDateEntry
import datetime
import os

class AnalyticsPage(ctk.CTkFrame):
    def __init__(self, master, db_file):
        super().__init__(master)

        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._make_sidebar()
        self._make_charts()

    def _make_sidebar(self):
        side = ctk.CTkFrame(self, width=200, fg_color="#ECECEC", corner_radius=6)
        side.grid(row=0, column=0, sticky="ns", padx=(8, 4), pady=8)
        side.grid_propagate(False)

        title = ctk.CTkLabel(side, text="Select Date Range", font=ctk.CTkFont(size=14, weight="bold"))
        title.grid(row=0, column=0, padx=8, pady=(8, 4), sticky="w")

        self.start_picker = CustomDateEntry(side, height=25)
        self.start_picker.grid(row=1, column=0, padx=8, pady=4, sticky="ew")

        self.end_picker = CustomDateEntry(side, height=25)
        self.end_picker.grid(row=2, column=0, padx=8, pady=4, sticky="ew")

        btn_refresh = ctk.CTkButton(
            side, text="Generate Graphs", command=self.update_graphs,
            height=30, fg_color="#3B8ED0", hover_color="#273366",
            font=ctk.CTkFont(size=12)
        )
        btn_refresh.grid(row=3, column=0, padx=8, pady=(6, 6), sticky="ew")

        btn_export = ctk.CTkButton(
            side, text="Export Graphs", command=self.export_graphs,
            height=30, fg_color="#3B8ED0", hover_color="#273366",
            font=ctk.CTkFont(size=12)
        )
        btn_export.grid(row=4, column=0, padx=8, pady=(0, 8), sticky="ew")

    def _make_charts(self):
        frame = ctk.CTkFrame(self, fg_color="#ECECEC", corner_radius=8)
        frame.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=8)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure((0, 1), weight=1)

        self.fig1 = Figure(dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        canvas1 = FigureCanvasTkAgg(self.fig1, master=frame)
        canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas1 = canvas1

        self.fig2 = Figure(dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        canvas2 = FigureCanvasTkAgg(self.fig2, master=frame)
        canvas2.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas2 = canvas2

    def update_graphs(self):
        # clear old data
        self.ax1.clear()
        self.ax2.clear()

        # get dates from pickers
        start = self.start_picker.get_date()
        end = self.end_picker.get_date()
        if not start or not end:
            self.ax1.text(0.5, 0.5, "Please pick valid dates.", ha='center')
            self.canvas1.draw()
            return

        s = start.strftime("%Y-%m-%d")
        e = end.strftime("%Y-%m-%d")
        sql = (
            "SELECT timestamp, drivetime, resttime FROM logs "
            "WHERE date(timestamp) BETWEEN ? AND ? ORDER BY timestamp;"
        )
        rows = self.cur.execute(sql, (s, e)).fetchall()

        if not rows:
            self.ax1.text(0.5, 0.5, "No data in this range.", ha='center')
            self.fig1.tight_layout(pad=3)
            self.canvas1.draw()
            return


        # Prepare data
        from collections import defaultdict
        daily = defaultdict(lambda: [0.0, 0.0])
        for r in rows:
           date = datetime.datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S").date()
           daily[date][0] += r[1] or 0
           daily[date][1] += r[2] or 0

        dates = sorted(daily.keys())
        drivetime = [daily[d][0] for d in dates]
        resttime = [daily[d][1] for d in dates]
        date_labels = [d.strftime("%a\n%m/%d") for d in dates]  # e.g. Mon 05/06

        # Chart 1: Daily stacked horizontal bars
        y_pos = range(len(dates))
        self.ax1.barh(y_pos, drivetime, label="Driving", color="#3B8ED0")
        self.ax1.barh(y_pos, resttime, left=drivetime, label="Resting", color="#FF6F61")
        self.ax1.set_yticks(y_pos)
        self.ax1.set_yticklabels(date_labels)
        self.ax1.invert_yaxis()  # recent dates on top
        self.ax1.set_xlabel("Hours")
        self.ax1.set_title("Daily Driving + Resting Time", fontsize=12)
        self.ax1.legend(loc="lower right")

        # Value labels
        for i, (d, r) in enumerate(zip(drivetime, resttime)):
            self.ax1.text(d / 2, i, f"{d:.1f}", va='center', ha='center', color="white", fontsize=8)
            self.ax1.text(d + r / 2, i, f"{r:.1f}", va='center', ha='center', color="white", fontsize=8)

        self.fig1.tight_layout()
        self.canvas1.draw()

        # Chart 2: Total comparison bar
        total_drive = sum(drivetime)
        total_rest = sum(resttime)
        categories = ["Driving", "Resting"]
        totals = [total_drive, total_rest]
        colors = ["#3B8ED0", "#FF6F61"]

        self.ax2.barh(categories, totals, color=colors)
        self.ax2.set_title("Total Hours", fontsize=12)
        self.ax2.set_xlabel("Total Hours")
        for i, v in enumerate(totals):
           self.ax2.text(v + 0.2, i, f"{v:.1f} hrs", va="center", fontsize=9)

        self.fig2.tight_layout()
        self.canvas2.draw()

    def export_graphs(self):
        folder = os.path.join(os.getcwd(), "exports")
        os.makedirs(folder, exist_ok=True)
        path1 = os.path.join(folder, "daily_activity_breakdown.png")
        self.fig1.savefig(path1)
        path2 = os.path.join(folder, "total_hours_by_activity.png")
        self.fig2.savefig(path2)
        tk.messagebox.showinfo("Export Complete",
                               f"Saved:\n{path1}\n{path2}")
