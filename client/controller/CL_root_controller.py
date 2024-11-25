import socket
from tkinter import messagebox

class root_controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model
    
    def connect_to_server(self, server_ip, server_port):

        if not server_ip or not server_port:
            message = "Vui lòng nhập IP và Port!"
            self.view.show_message(message)
            return

        self.model.set_ip_address(server_ip)
        self.model.set_port(server_port)        
        
        try:
            message = self.model.connect_to_server(server_ip, server_port)  # Gọi hàm connect_to_server từ Model
            self.view.show_message(message)  # Hiển thị thông báo kết nối thành công trong View
        except ConnectionError as e:
            self.view.show_message(f"Lỗi: {str(e)}")  # Hiển thị lỗi nếu kết nối thất bại

    def get_ip_and_port(self):
        """Lấy IP và Port từ các Entry, đồng thời kiểm tra tính hợp lệ"""
        ip = self.view.entry_ip.get()
        port = self.view.entry_port.get()

        # Kiểm tra nếu IP hợp lệ
        if not self.is_valid_ip(ip):
            self.show_message("IP không hợp lệ! Vui lòng nhập IP đúng.")
            return None, None  # Trả về None nếu không hợp lệ

        # Kiểm tra nếu Port hợp lệ
        if not self.is_valid_port(port):
            self.show_message("Port không hợp lệ! Port phải là số nguyên trong khoảng 1 đến 65535.")
            return None, None  # Trả về None nếu không hợp lệ

        return ip, int(port)
            
    def is_valid_ip(self, ip):
        """Kiểm tra tính hợp lệ của địa chỉ IP"""
        try:
            socket.inet_aton(ip)  # Sử dụng socket để kiểm tra IP hợp lệ
            return True
        except socket.error:
            return False

    def is_valid_port(self, port):
        """Kiểm tra tính hợp lệ của Port (1-65535)"""
        try:
            port = int(port)
            return 1 <= port <= 65535
        except ValueError:
            return False

        
    
