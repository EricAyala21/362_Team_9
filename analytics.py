import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
from custom_date_entry import CustomDateEntry
import datetime
import os  # For handling file paths

class AnalyticsPage(ctk.CTkFrame):
    def __init__(self, master, filename):
        # Setup database connection
        super().__init__(master)
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()

        # Store user-selected date range
        self.start_date = None
        self.end_date = None

        # Set up color scheme
        self.bg_color = "#F4F4F4"
        self.graph_color = "#3B8ED0"
        self.highlight_color = "#273366"
        self.bar_color = "#4CAF50"

        self.configure(bg_color=self.bg_color)

        # Setup both UI sections
        self.setup_left_frame()
        self.setup_graph_frame()

    def setup_left_frame(self):
        # Frame for date selection and button
        self.left_frame = ctk.CTkFrame(self, width=200)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Label for date selection
        self.date_label = ctk.CTkLabel(self.left_frame, text="Select Date Range")
        self.date_label.pack(pady=5)

        # Start and End date pickers
        self.start_picker = CustomDateEntry(self.left_frame)
        self.start_picker.pack(pady=5)

        self.end_picker = CustomDateEntry(self.left_frame)
        self.end_picker.pack(pady=5)

        # Button to generate graph
        self.generate_btn = ctk.CTkButton(
            self.left_frame,
            text="Generate Graphs",
            command=self.update_graphs,
            fg_color=self.graph_color,
            hover_color=self.highlight_color
        )
        self.generate_btn.pack(pady=10)

        # Button to export graphs as images
        self.export_btn = ctk.CTkButton(
            self.left_frame,
            text="Export Graphs",
            command=self.export_graphs,
            fg_color=self.graph_color,
            hover_color=self.highlight_color
        )
        self.export_btn.pack(pady=10)

    def setup_graph_frame(self):
        # Frame where graphs will be shown
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(expand=True, side="right", fill="both", padx=10, pady=10)

        # Setup for line chart
        self.figure1 = Figure(figsize=(5, 3), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.ax1.set_title("Driving vs Resting Time")
        self.ax1.set_xlabel("Date")
        self.ax1.set_ylabel("Hours")
        self.canvas1 = FigureCanvasTkAgg(self.figure1, self.graph_frame)
        self.canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Setup for bar chart
        self.figure2 = Figure(figsize=(5, 2.5), dpi=100)
        self.ax2 = self.figure2.add_subplot(111)
        self.ax2.set_title("Total Driving vs Resting Time")
        self.ax2.set_ylabel("Total Hours")
        self.canvas2 = FigureCanvasTkAgg(self.figure2, self.graph_frame)
        self.canvas2.get_tk_widget().pack(fill="both", expand=True)

    def update_graphs(self):
        # Clear any previous data in both charts
        self.ax1.clear()
        self.ax2.clear()

        self.ax1.set_title("Driving vs Resting Time")
        self.ax1.set_xlabel("Date")
        self.ax1.set_ylabel("Hours")

        self.ax2.set_title("Total Driving vs Resting Time")
        self.ax2.set_ylabel("Total Hours")

        # Retrieve dates from user input
        start = self.start_picker.get_date()
        end = self.end_picker.get_date()

        # Check if both dates are selected
        if not start or not end:
            self.ax1.text(0.5, 0.5, "Select valid start and end dates.", ha='center')
            self.canvas1.draw()
            return

        # Format the dates for SQL query
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")

        # Query the logs table for matching records
        query = """
        SELECT timestamp, drivetime, resttime
        FROM logs
        WHERE date(timestamp) BETWEEN ? AND ?
        ORDER BY timestamp;
        """
        try:
            rows = self.cur.execute(query, (start_str, end_str)).fetchall()
        except Exception as e:
            self.ax1.text(0.5, 0.5, "Error loading data", ha='center')
            self.canvas1.draw()
            return

        # Handle empty results
        if not rows:
            self.ax1.text(0.5, 0.5, "No data found in this range.", ha='center')
            self.canvas1.draw()
            return

        # Organize the data into separate lists
        dates = [datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").date() for row in rows]
        drive_hours = [row[1] for row in rows]
        rest_hours = [row[2] for row in rows]

        # Line chart: Day-by-day comparison
        self.ax1.plot(dates, drive_hours, label="Driving Time", color=self.graph_color, linewidth=2)
        self.ax1.plot(dates, rest_hours, label="Resting Time", color="#ff6f61", linewidth=2)
        self.ax1.legend()
        self.canvas1.draw()

        # Bar chart: Total comparison
        total_drive = sum(drive_hours)
        total_rest = sum(rest_hours)
        self.ax2.bar(["Driving", "Resting"], [total_drive, total_rest], color=[self.graph_color, "#ff6f61"])
        self.canvas2.draw()

    def export_graphs(self):
        """
        Export both graphs as image files (PNG format).
        Each graph is saved with a unique name in the current directory.
        """
        if not os.path.exists('exports'):
            os.makedirs('exports')  # Create directory if it doesn't exist

        # Export line graph
        line_graph_path = os.path.join('exports', 'driving_vs_resting_time.png')
        self.figure1.savefig(line_graph_path)
        print(f"Line graph saved as {line_graph_path}")

        # Export bar graph
        bar_graph_path = os.path.join('exports', 'total_driving_vs_resting_time.png')
        self.figure2.savefig(bar_graph_path)
        print(f"Bar graph saved as {bar_graph_path}")

        # Notify the user
        tk.messagebox.showinfo("Export Successful", "Graphs have been saved in the 'exports' folder.")

