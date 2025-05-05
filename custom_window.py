from time import sleep
import customtkinter as ctk

class SelectionWindow(ctk.CTkToplevel):
    def __init__(self, title : str
                 , var : ctk.StringVar
                 , options : list[str]|tuple[str]
                 , *args, **kwargs):
        """Construct the popup window with selection options var is the customtkinter.StringVar variable 
        to pass along the result of selection, options are the list possible option string.
        This widget will set the StringVar to the text of the button clicked then destroy
        If need to add any widgets for content, set the widgets as descendent of the content_frame attribute"""
        super().__init__(*args, **kwargs)

        self.title(title)
        self.options = options
        self.value = var
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.content_frame = FormattedTextFrame(master = self, fg_color = "transparent")
        self.content_frame.grid(row = 0, column = 0, sticky = "nsew", padx=10, pady=10)
        self.option_frame = ctk.CTkFrame(master = self)
        self.option_frame.grid(row = 1, column = 0, sticky = "nsew")
        self.option_frame.columnconfigure(list(range(len(self.options))), weight=1)
        
        buttons = []
        for i in range(len(self.options)):
            btn = ctk.CTkButton(self.option_frame, text = self.options[i])
            btn.configure(command = lambda a = self.options[i]: self.click_button(a))
            btn.grid(row = 2, column = i, sticky = "nsew", padx = 5, pady = 10)
            buttons.append(btn)

    def click_button(self, text : str):
        self.value.set(text)
        print("Option selected: " + self.value.get())
        self.destroy()

    def set_content(self, msg_list, column_weights, header = None):
        """Set the content frame with formatted text"""
        self.content_frame.grid_forget()
        self.content_frame.set(msg_list, column_weights, header=header)
        self.content_frame.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 10)


class FormattedTextFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(**kwargs)
        self.labels = []

    def set(self, msg_list, column_weights, header = None):
        self.remove_content()
        if(not isinstance(msg_list, list)
           or not isinstance(column_weights, (list))
           or msg_list == None or len(msg_list) == 0):
            return
        
        self.grid_rowconfigure(list(range(len(msg_list)+1)), weight = 1)
        for j in range(len(column_weights)):
            self.grid_columnconfigure(j, weight=column_weights[j])

        if(header != None):
            label = ctk.CTkLabel(self, text = header)
            label.grid(row = 0, column = 0, columnspan = len(column_weights), padx = 5, pady = 5)
            self.labels.append(label)
        for i in range(len(msg_list)):
            if(not isinstance(msg_list[i], list)):
                continue
            for j in range(len(msg_list[i])):
                label = ctk.CTkLabel(self, text = msg_list[i][j])
                label.grid(row = i+1, column = j, sticky = "w", padx = 5, pady = 5)
                self.labels.append(label)
    
    def remove_content(self):
        for label in self.labels:
            if(label != None and label.winfo_exists()):
                label.destroy()
        self.labels = []

    
#Testing whether the popup works
# class mainpage(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.geometry("500x500")
#         f = ctk.CTkFrame(self)
#         f.pack(expand = "yes")
#         btn = ctk.CTkButton(f, text = "Enter", command = lambda a=None : self.create_window())
#         btn.pack()
#         self.v = ctk.StringVar()
#         print(self.v.get())
#         self.w = None

#     def create_window(self):
#         if(self.w == None or not self.w.winfo_exists()):
#             print("window created")
#             self.w = SelectionWindow(title = "pick one", var = self.v, options=["", "No"])
#             self.w.set_content(msg_list=[["Pick"],["Yes","No"]], column_weights=[1,1])
#         else:
#             self.w.focus()
#         self.w.grab_set()
#         self.wait_window(self.w)
#         print(self.v.get())

# app = mainpage()
# app.mainloop()