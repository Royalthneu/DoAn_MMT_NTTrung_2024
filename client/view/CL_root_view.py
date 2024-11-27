
from tkinter import messagebox
from model.CL_model import WidgetFactory
from model.CL_model import open_wd_client_socket

from view.CL_service_view import service_view
# from view.CL_del_copy_view import del_copy_view
# from view.CL_shutdown_view import shutdown_view
# from view.CL_keylogger_view import keylogger_view

class root_view:
    def __init__(self, window):        
        self.window = window         
        self.controller = None
        self.client_socket = None
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
        self.btn_services.configure(command=self.btn_services_click)
                
        self.btn_shutdown_reset = self.widget_factory.create_button("3. Shutdown / Reset máy SERVER", 0.08, 0.561, 317, 36)
        self.btn_shutdown_reset.configure(command=self.btn_shutdown_reset_click)
        
        self.btn_view_screen = self.widget_factory.create_button("4. Xem màn hình hiện thời của máy SERVER", 0.08, 0.654, 317, 36)
        self.btn_view_screen.configure(command=self.btn_view_screen_click)
        
        self.btn_keylogger = self.widget_factory.create_button("5. Khóa / Bật phím (keylogger)", 0.08, 0.749, 317, 36)        
        self.btn_keylogger.configure(command=self.btn_keylogger_click)
        
        self.btn_file_operations = self.widget_factory.create_button("6. Xóa files ; Copy files từ SERVER", 0.08, 0.843, 317, 36)
        self.btn_file_operations.configure(command=self.btn_file_operations_click)
        
        # Separators
        self.widget_factory.create_separator(0.027, 0.113)
        self.widget_factory.create_separator(0.027, 0.34)    
    
    def show_message(self, message):
        messagebox.showinfo("Thông báo", message)
        
    def btn_connect_click(self):
        server_ip, server_port = self.controller.get_ip_and_port()
        if server_ip and server_port:
            try:
                # Thực hiện kết nối nếu IP và Port hợp lệ
                self.controller.connect_to_server(server_ip, server_port)
                self.client_socket = self.controller.get_client_socket()
            except Exception as e:
                # Xử lý lỗi khi có exception
                self.show_message(f"Lỗi khi kết nối: {str(e)}")
            
    def btn_applications_click(self):
        from view.CL_app_view import app_view
        open_wd_client_socket(self.window, self.client_socket, self.controller, app_view)
        
    def btn_services_click(self):
        from view.CL_service_view import service_view
        open_wd_client_socket(self.window, self.client_socket, self.controller, service_view)
        
    def btn_shutdown_reset_click(self):
        from view.CL_shutdown_view import shutdown_view
        open_wd_client_socket(self.window, self.client_socket, self.controller, shutdown_view)
        
    def btn_view_screen_click(self):
        self.controller.share_screen_server(self.client_socket)
        
    def btn_keylogger_click(self):
        from view.CL_keylogger_view import keylogger_view
        open_wd_client_socket(self.window, self.client_socket, self.controller, keylogger_view)
        
    def btn_file_operations_click(self):
        from view.CL_del_copy_view import del_copy_view
        open_wd_client_socket(self.window, self.client_socket, self.controller, del_copy_view)  



    # def update_tree_view(self, app_list):
    #     self.tree_app.delete(*self.tree_app.get_children())  # Xóa dữ liệu cũ trong TreeView
    #     if not app_list:  # Nếu danh sách ứng dụng rỗng
    #         self.show_message("Thông báo", "Không có ứng dụng nào đang chạy.")
    #         return
    #     for pid, app_name in app_list:
    #         self.tree_app.insert("", "end", text=pid, values=(app_name,))

        
        
        