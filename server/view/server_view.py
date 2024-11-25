# SV_view.py

import tkinter as tk
from tkinter import messagebox

btn_open = None
btn_close = None

class SV_View:
    def __init__(self, window):        
        self.window = window        
        self.window.geometry("389x83+24+119")
        self.window.minsize(120, 1)
        self.window.maxsize(5564, 1901)
        self.window.resizable(0, 0)
        self.window.title("RUN SERVER")
        self.window.configure(bg="#d9d9d9")
        
        def create_label(window, text, relx, rely, width, height=20, bg="#d9d9d9", fg="#000000", font="-family {Segoe UI} -size 9", anchor="w"):
            label = tk.Label(window, text=text, bg=bg, fg=fg, font=font, anchor=anchor)
            label.place(relx=relx, rely=rely, width=width, height=height)
            return label
        
        self.lbl_server_ip = create_label(self.window, "Server IP:", relx=0.041, rely=0.289, width=93)
        self.lbl_server_port = create_label(self.window, "Port: 8081", relx=0.054, rely=0.602, width=80)
        self.lbl_status = create_label(self.window, "Server is closing", relx=0.300, rely=0.58, width=300)
        self.lbl_ip = create_label(self.window, "Bí mật", relx=0.22, rely=0.28, width=119)

        def create_button_config(text, command, state, x, y, width, height):
            button = tk.Button(text=text, command=command, state=state)
            button.place(x=x, y=y, width=width, height=height)
            return button

        self.btn_open = create_button_config("Open Server",None,"normal",x=250,y=15,width=97,height=26)        
        self.btn_close = create_button_config("Close Server",None,"disabled",x=250,y=50,width=97,height=26)

    def set_lbl_server_ip(self, ip):        
        self.lbl_ip.config(text=ip)

    def set_lbl_status(self, status):
        self.lbl_status.config(text=status)

    def disable_open_button(self):
        self.btn_open.config(state="disabled")

    def enable_open_button(self):
        self.btn_open.config(state="normal")

    def disable_close_button(self):
        self.btn_close.config(state="disabled")

    def enable_close_button(self):
        self.btn_close.config(state="normal")

    def show_message(self, title, message):        
        messagebox.showinfo(title=title, message=message)
        

