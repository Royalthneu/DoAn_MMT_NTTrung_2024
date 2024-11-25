
import tkinter as tk
from tkinter import messagebox
from view.widget_factory import WidgetFactory
from view.CL_app_view import app_view
from view.CL_service_view import service_view
from view.CL_del_copy_view import del_copy_view
from view.CL_shutdown_view import shutdown_view
from view.CL_keylogger_view import keylogger_view


class root_view:
    def __init__(self, window):        
        self.window = window 
        self.controller = None
        self.window.title("RUN CLIENT")
        self.window.geometry("375x529+100+100")
        self.window.resizable(0, 0)
        self.window.configure(background="#d9d9d9")
        
        self.widget_factory = WidgetFactory(window)
        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.label_title = self.widget_factory.create_label("ĐỒ ÁN ĐIỀU KHIỂN MÁY TÍNH TỪ XA", 0.08, 0.019, 248, 26)
        self.label_ip = self.widget_factory.create_label("Nhập IP của server", 0.08, 0.149, 111, 26)
        self.label_port = self.widget_factory.create_label("Nhập Port của Server", 0.08, 0.206, 121, 26)
        self.label_info = self.widget_factory.create_label("Sinh viên: Nguyễn Thế Trung - MSSV: 23880092", 0.08, 0.057, 255, 26)

        # Entry fields
        self.entry_ip = self.widget_factory.create_entry(0.4, 0.149, 0.491, 20)
        self.entry_port = self.widget_factory.create_entry(0.4, 0.206, 0.491, 20)

        # Buttons
        self.btn_connect = self.widget_factory.create_button("Kết nối Server", 0.32, 0.261, 107, 26)
        self.btn_connect.configure(command=self.btn_connect_click)
        
        self.btn_applications = self.widget_factory.create_button("1. List / Start / Stop các Applications", 0.08, 0.378, 317, 36)
        self.btn_applications.configure(command=self.btn_applications_click)
        
        self.btn_services = self.widget_factory.create_button("2. List / Start / Stop các Services", 0.08, 0.469, 317, 36)
                
        self.btn_shutdown_reset = self.widget_factory.create_button("3. Shutdown / Reset máy SERVER", 0.08, 0.561, 317, 36)
        self.btn_view_screen = self.widget_factory.create_button("4. Xem màn hình hiện thời của máy SERVER", 0.08, 0.654, 317, 36)
        self.btn_keylogger = self.widget_factory.create_button("5. Khóa / Bật phím (keylogger)", 0.08, 0.749, 317, 36)
        self.btn_file_operations = self.widget_factory.create_button("6. Xóa files ; Copy files từ SERVER", 0.08, 0.843, 317, 36)

        # Separators
        self.widget_factory.create_separator(0.027, 0.113)
        self.widget_factory.create_separator(0.027, 0.34)
        
    def show_message(self, message):
        messagebox.showinfo("Thông báo", message)
        
    def btn_connect_click(self):
        server_ip, server_port = self.controller.get_ip_and_port()
        if server_ip and server_port:
            # Thực hiện kết nối nếu IP và Port hợp lệ
            self.controller.connect_to_server(server_ip, server_port)
            
    def btn_applications_click(self):
        self.open_window(app_view)
        
    def btn_services_click(self):
        self.open_window(app_view)
        
    def btn_shutdown_reset_click(self):
        self.open_window(app_view)
        
    def btn_view_screen_click(self):
        self.open_window(app_view)
        
    def btn_keylogger_click(self):
        self.open_window(app_view)
        
    def btn_file_operations_click(self):
        self.open_window(app_view)    

    def open_window(self, window_class):
    # Tạo cửa sổ mới
        top = tk.Toplevel()
        # Khởi tạo cửa sổ từ lớp window_class
        window_instance = window_class(top=top)
        # Đảm bảo rằng cửa sổ chính không thể click khi cửa sổ top đang mở
        top.grab_set()
        
        
        #1. Gắn các sự kiện cho nút CL_app_process
        # if isinstance(window_instance, CL_app_process):
        #     window_instance.btn_list_app.configure(command=lambda: self.list_apps_running(client_socket))
        #     window_instance.btn_start_app.configure(command=lambda: self.open_window(client_socket, CL_form_nhap_Name))            
        #     window_instance.btn_stop_app.configure(command=lambda: self.open_window(client_socket, CL_form_nhap_PID))            
        #     window_instance.btn_clear_list_app.configure(command=self.clear_list_apps)
            
        # elif isinstance(window_instance, CL_form_nhap_Name): 
        #         # Sự kiện khi nhấn nút btn_nhap_Name
        #         window_instance.btn_nhap_Name.configure(command=lambda: self.start_app(client_socket, window_instance))
                
        # elif isinstance(window_instance, CL_form_nhap_PID): 
        #         # Sự kiện khi nhấn nút btn_nhap_ID
        #         window_instance.btn_nhap_PID.configure(command=lambda: self.stop_app(client_socket, window_instance))    
        
        #2. Gắn các sự kiện cho nút CL_services_process  


        #3. Gắn các sự kiện cho nút CL_shutdown_reset 
        
        
        #4. Gắn các sự kiện cho nút CL_view_screen 
        
        
        #5. Gắn các sự kiện cho nút CL_keylogger 
        
        
        #6. Gắn các sự kiện cho nút CL_del_copy          
        
        # Khi cửa sổ top đóng, hủy grab_set
        top.protocol("WM_DELETE_WINDOW", lambda: (top.grab_release(), top.destroy()))
        
        
        