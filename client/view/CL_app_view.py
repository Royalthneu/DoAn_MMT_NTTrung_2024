import tkinter as tk
from tkinter import ttk, messagebox



class WidgetFactory:
    def __init__(self, window):
        self.window = window

    def create_label(self, text, relx, rely, width, height):
        label = tk.Label(self.window, text=text, background="#d9d9d9", foreground="#000000", anchor='w')
        label.place(relx=relx, rely=rely, width=width, height=height)
        return label

    def create_entry(self, relx, rely, relwidth, height):
        entry = tk.Entry(self.window, background="white", foreground="#000000")
        entry.place(relx=relx, rely=rely, relwidth=relwidth, height=height)
        return entry

    def create_button(self, text, relx, rely, width, height):
        button = tk.Button(self.window, text=text, background="#d9d9d9", foreground="#000000")
        button.place(relx=relx, rely=rely, width=width, height=height)
        return button

    def create_separator(self, relx, rely, relwidth=0.946):
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.place(relx=relx, rely=rely, relwidth=relwidth)