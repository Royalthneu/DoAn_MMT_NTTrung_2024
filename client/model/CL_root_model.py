import socket
from tkinter import messagebox

class root_model:
    def __init__(self, view):
        self.client_socket = None
        self.connected = False
        self.view = view
        
    def connect_to_server(self, server_ip, server_port):
        if self.connected:
            raise ConnectionError("Đã kết nối đến server!")        
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, server_port))
            self.connected = True
            return "Kết nối thành công đến server!"
        except socket.error as e:
            self.connected = False
            self.client_socket = None
            raise ConnectionError(f"Lỗi khi kết nối đến server: {e}")
    
    def send_command(self, command):
        if not self.connected or not self.client_socket:
            raise ConnectionError("Chưa kết nối đến server!")        
        try:
            self.client_socket.sendall(command.encode())  # Mã hóa lệnh và gửi
        except socket.error as e:
            raise ConnectionError(f"Lỗi khi gửi lệnh đến server: {e}")

    def receive_response(self, buffer_size=65535):
        if not self.connected or not self.client_socket:
            raise ConnectionError("Chưa kết nối đến server!")        
        try:
            response = self.client_socket.recv(buffer_size).decode()  # Nhận và giải mã phản hồi
            return response
        except socket.error as e:
            raise ConnectionError(f"Lỗi khi nhận phản hồi từ server: {e}")
    
    def show_message(self, message):
        messagebox.showinfo("Thông báo", message)
    
    def set_ip_address(self, ip):
        self.server_ip = ip

    def set_port(self, port):
        self.server_port = port