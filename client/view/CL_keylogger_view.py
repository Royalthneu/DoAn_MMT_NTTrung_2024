import time
from tkinter import messagebox
import tkinter as tk
from model.CL_model import WidgetFactory


class keylogger_view:
    def __init__(self, top, client_socket, controller):
        self.top = top
        self.client_socket = client_socket
        self.controller = controller
        self.top.geometry("637x489+1307+122")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(0,  0)
        self.top.title("KEYLOGGER")
        self.top.configure(
            background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        self.text_bat_keylogger = tk.Text(
            self.top, wrap="word")  # Tự động xuống dòng theo từ
        self.text_bat_keylogger.place(
            relx=0.05, rely=0.15, relwidth=0.89, height=400)

        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()

    def create_widgets(self):
        # Button configuration using WidgetFactory
        self.btn_start_keylogger = self.widget_factory.create_button(
            "BAT KEYLOGGER", 0.05, 0.043, 107, 36)
        self.btn_start_keylogger.configure(
            command=self.btn_start_keylogger_click)

        self.btn_stop_keylogger = self.widget_factory.create_button(
            "TAT KEYLOGGER", 0.27, 0.043, 107, 36)
        self.btn_stop_keylogger.configure(
            command=self.btn_stop_keylogger_click)

        self.btn_print_keylogger = self.widget_factory.create_button(
            "IN KEYLOGGER", 0.488, 0.043, 127, 36)
        self.btn_print_keylogger.configure(
            command=self.btn_print_keylogger_click)

        self.btn_clear = self.widget_factory.create_button(
            "CLEAR", 0.738, 0.041, 127, 36)
        self.btn_clear.configure(command=self.btn_clear_click)

    def btn_start_keylogger_click(self):
        self.controller.start_keylogger(self.client_socket)
        self.show_message("Bắt đầu bắt phím Keylogger!")

    def btn_stop_keylogger_click(self):
        self.btn_print_keylogger_click()  # Xuất phím đã nhập ra textbox trước khi stop
        time.sleep(0.1)
        self.controller.stop_keylogger(self.client_socket)
        self.show_message("Đã in phím bắt và đã dừng keylogger.")

    def btn_print_keylogger_click(self):
        self.text_bat_keylogger.delete("1.0", "end")
        keys_from_server = self.controller.print_keylogger(self.client_socket)
        self.update_text_widget(keys_from_server)

    def btn_clear_click(self):
        self.clear_text_widget()
        self.show_message("Xóa nội dung phím bắt.")

    def update_text_widget(self, text):
        # Kiểm tra và xóa chuỗi "Unknown Command" nếu có
        if "Unknown command." in text:
            text = text.replace("Unknown command.", "")
        self.text_bat_keylogger.insert("end", text)

    def clear_text_widget(self):
        self.controller.clear_buffer_keylogger(self.client_socket)
        # Xóa từ dòng đầu tiên đến cuối cùng
        self.text_bat_keylogger.delete("1.0", "end")

    def show_message(self, message):
        messagebox.showinfo("Info", message)
