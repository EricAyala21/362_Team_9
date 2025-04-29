import customtkinter as ctk
from custom_date_entry import CustomDateEntry
import datetime as dt

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry ("300x300")
app.columnconfigure(1, weight = 3)
input_box = CustomDateEntry(app)
input_box.grid(row = 0, column = 0)
btn1 = ctk.CTkButton(app, text = "get", command=lambda a = None : print(input_box.get_date()))
btn1.grid(row = 1, column = 1, sticky = "ewns")
btn2 = ctk.CTkButton(app, text = "clear", command=input_box.clear)
btn2.grid(row = 1, column = 0)
btn3 = ctk.CTkButton(app, text = "set", command=lambda a = dt.date(2025,6,15): input_box.set_date(a))
btn3.grid(row = 2, column = 0)
app.mainloop()