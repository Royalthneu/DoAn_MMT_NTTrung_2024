import threading
from tkinter import messagebox
from model.CL_model import WidgetFactory


class frm_nhap_Ten_view:
    def __init__(self, top, client_socket, controller, from_screen):
        self.top = top
        self.client_socket = client_socket
        self.from_screen = from_screen
        self.controller = controller
        self.view = None
        self.top.geometry("350x60+20+200")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(1, 1)
        self.top.title("Nhập")
        self.top.configure(
            background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()

    def create_widgets(self):
        # Label configuration
        self.Lb_nhap_Ten = self.widget_factory.create_label(
            "Nhập Tên", 0.016, 0.25, 82, 25)
        # Entry configuration
        self.entry_nhap_Ten = self.widget_factory.create_entry(
            0.2, 0.25, 0.5, 25)
        # Button configuration with custom cursor
        self.btn_nhap_Ten = self.widget_factory.create_button(
            "OK", 0.75, 0.25, 60, 25)
        self.btn_nhap_Ten.configure(command=self.btn_nhap_Ten_click)

    def btn_nhap_Ten_click(self):
        name = self.entry_nhap_Ten.get()
        if name:
            if self.from_screen == "app_view":
                threading.Thread(target=self.controller.start_app, args=(
                    self.client_socket, name)).start()
            elif self.from_screen == "service_view_btn_start":
                threading.Thread(target=self.controller.start_service, args=(
                    self.client_socket, name)).start()
            elif self.from_screen == "service_view_btn_stop":
                threading.Thread(target=self.controller.stop_service_by_name, args=(
                    self.client_socket, name)).start()
            self.top.destroy()
        else:
            messagebox.showerror(
                title="Lỗi PID", message="PID không hợp lệ hoặc không tồn tại! Vui lòng nhập lại.")
