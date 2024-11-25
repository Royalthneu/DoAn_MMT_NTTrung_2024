from tkinter import messagebox
from client.view.CL_widget_factory import WidgetFactory

class root_view:
    def __init__(self, window, controller):        
        self.window = window 
        self.controller = controller
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
        self.btn_applications = self.widget_factory.create_button("1. List / Start / Stop các Applications", 0.08, 0.378, 317, 36)
        self.btn_services = self.widget_factory.create_button("2. List / Start / Stop các Services", 0.08, 0.469, 317, 36)
        self.btn_shutdown_reset = self.widget_factory.create_button("3. Shutdown / Reset máy SERVER", 0.08, 0.561, 317, 36)
        self.btn_view_screen = self.widget_factory.create_button("4. Xem màn hình hiện thời của máy SERVER", 0.08, 0.654, 317, 36)
        self.btn_keylogger = self.widget_factory.create_button("5. Khóa / Bật phím (keylogger)", 0.08, 0.749, 317, 36)
        self.btn_file_operations = self.widget_factory.create_button("6. Xóa files ; Copy files từ SERVER", 0.08, 0.843, 317, 36)

        # Separators
        self.widget_factory.create_separator(0.027, 0.113)
        self.widget_factory.create_separator(0.027, 0.34)
    
    def get_server_ip_from_user(self):
        """Lấy địa chỉ IP của server từ người dùng."""
        return input("Dien dia chi IP cua Server: ")

    def get_server_port_from_user(self):
        """Lấy port của server từ người dùng."""
        return int(input("Dien so port: "))

    def show_invalid_ip_message(self):
        """Hiển thị thông báo lỗi khi IP không hợp lệ."""
        messagebox.showerror("Lỗi", "IP không hợp lệ. Vui lòng nhập lại.")

    def show_invalid_port_message(self):
        """Hiển thị thông báo lỗi khi port không hợp lệ."""
        messagebox.showerror("Lỗi", "Port không hợp lệ. Vui lòng nhập lại.")

    def show_connection_success(self, server_ip, server_port):
        """Hiển thị thông báo kết nối thành công."""
        messagebox.showinfo("Kết nối", f"Ket noi server co dia chi {server_ip}:{server_port} thanh cong")

    def show_connection_failure(self, error_message):
        """Hiển thị thông báo kết nối thất bại."""
        messagebox.showerror("Kết nối thất bại", f"Ket noi khong thanh cong: {error_message}. Vui long kiem tra server co dang chay khong va IP, port co dung khong.")
        
    def show_error(self, message):
        messagebox.showerror("Error", message)
    
