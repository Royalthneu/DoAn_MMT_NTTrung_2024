import json
import os
import socket
import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from vidstream import ScreenShareClient

import keyboard

class SV_Model:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None
        self.running = False

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(3)
            print(f"Server is listening on: {self.server_ip}:{self.server_port}")
            return True
        except Exception as e:
            print(f"Error while starting server: {e}")
            return False

    def accept_client(self):
        try:
            self.client_socket, addr = self.server_socket.accept()
            return self.client_socket, addr
        except Exception as e:
            print(f"Error while accepting client: {e}")
            return None, None

    def close_server(self):
        if self.server_socket:
            self.server_socket.close()  # Đóng socket của server
            print("Server stopped.")
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
        """Nhận phản hồi từ server/client"""
        return socket.recv(buffer_size).decode()
    
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
    
    def stop_service(self, service_pid):
        self.command = f"taskkill /PID {service_pid} /F"
        return self.run_powershell_command(self.command)


    #---------------3. SV_Shutdown: --------------------------  
    def shutdown_server():
        try:
            SV_Model.run_powershell_command("Stop-Computer -Force")
            return "Server is shutting down..."
        except Exception as e:
            return f"Khong the shutdown server: {e}"
    
    def reset_server():
        try:
            SV_Model.run_powershell_command("Restart-Computer -Force")
            return "Server is reset..."
        except Exception as e:
            return f"Khong the reset server: {e}"

    #4. SV_ScreenShare:    
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
            print(f"Configuration updated: Server IP = {config['server_ip']}, Server Port = {config['server_port']}, Client IP = {config['client_ip']}, Client Port = {config['client_port']}")
        else:
            print("Configuration file does not exist.")

    # Hàm đọc cấu hình server từ file
    def read_config_server(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
            return config.get("server_ip"), config.get("server_port")
        except json.JSONDecodeError:
            print("File cấu hình không hợp lệ. Vui lòng kiểm tra nội dung file.")
            return None, None
        except FileNotFoundError:
            print("File cấu hình không tồn tại.")
            return None, None
        
    def read_config_client(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
            return config.get("client_ip"), config.get("client_port")
        except json.JSONDecodeError:
            print("File cấu hình không hợp lệ. Vui lòng kiểm tra nội dung file.")
            return None, None
        except FileNotFoundError:
            print("File cấu hình không tồn tại.")
            return None, None

    #5. SV_Keylogger:    
    def start_keylogger():
        keys_pressed = ""
        MAX_LINE_LENGTH = 50
        stop_keylogger = False
        listener = None

        def on_press(key):
            nonlocal keys_pressed, stop_keylogger
            if stop_keylogger:
                return False

            if hasattr(key, 'char') and key.char is not None:
                key_str = key.char
            else:
                key_str = f' {str(key)} '

            if key == keyboard.Key.enter:
                keys_pressed = ""
            else:
                keys_pressed += key_str

            return key_str

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        return listener

    
    def stop_keylogger(listener):
        listener.stop()
        return "KEYLOGGER_STOPPED"
    #6. SV_Del_Copy:
    
    def delete_file(client_socket, file_path):
    # Xóa file tại đường dẫn được chỉ định trên server.
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return f"Xoa file thanh cong."
            except Exception as e:
                return f"Loi: xoa file: {e}"
        else:
            return f"File khong ton tai tren may Server."  
        
    
    def copy_file(client_socket, file_path):
        #Sao chép file tại đường dẫn được chỉ định trên server và gửi tới client.
        if os.path.exists(file_path):        
            # Lấy kích thước file
            file_size = os.path.getsize(file_path)
            
            # Gửi kích thước file đến client
            client_socket.sendall(file_size.to_bytes(4, byteorder='big'))
            
            # Gửi file tới client
            with open(file_path, 'rb') as f:
                while (chunk := f.read(65535)):
                    client_socket.sendall(chunk)
        else:
            # Nếu file không tồn tại, gửi kích thước 0 để báo lỗi
            client_socket.sendall((0).to_bytes(4, byteorder='big'))
            


    