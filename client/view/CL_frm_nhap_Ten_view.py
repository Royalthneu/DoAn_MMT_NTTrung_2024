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
        self.top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()
        
    def create_widgets(self):
        # Label configuration
        self.Lb_nhap_Ten = self.widget_factory.create_label("Nhập Tên", 0.016, 0.25, 82, 25)
        # Entry configuration
        self.entry_nhap_Ten = self.widget_factory.create_entry(0.2, 0.25, 0.5, 25)
        # Button configuration with custom cursor
        self.btn_nhap_Ten = self.widget_factory.create_button("OK", 0.75, 0.25, 60, 25)
        self.btn_nhap_Ten.configure(command= self.btn_nhap_Ten_click)
    
    def btn_nhap_Ten_click(self):
        name = self.entry_nhap_Ten.get()
        if name:
            # Start a new thread to run start_app or start_service
            threading.Thread(target=self.run_in_background, args=(name,)).start()
        else:
            messagebox.showerror(title="Lỗi Tên", message="Tên không hợp lệ hoặc không tồn tại! Vui lòng nhập lại.")
    
    def run_in_background(self, name):
        # This method will run in a separate thread
        if self.from_screen == "app_view":
            self.controller.start_app(self.client_socket, name)  # Running start_app on the controller
        elif self.from_screen == "service_view":
            self.controller.start_service(self.client_socket, name)  # Running start_service on the controller
        
        # Once the background task is done, we update the UI in the main thread
        self.top.after(0, self.top.destroy())  # Schedule the UI update to run in the main thread
    