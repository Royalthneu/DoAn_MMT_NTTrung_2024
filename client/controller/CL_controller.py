import os
import socket
import threading
from tkinter import filedialog, messagebox
import keyboard
from vidstream import StreamingServer

class cl_controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.server_ip = None
        self.server_port = None
        self.client_ip = None
        self.client_port = 6789
        self.is_logging = False
    
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
            self.server_ip = server_ip
            self.server_port = server_port     
            self.client_ip = self.model.client_socket.getsockname()[0]
            self.model.update_config_client("cl_config.json", self.server_ip, self.server_port, self.client_ip, 6789)     
            
        except ConnectionError as e:
            self.view.show_message(f"Lỗi: {str(e)}")  # Hiển thị lỗi nếu kết nối thất bại
            
    def get_client_socket(self):
        """Lấy client_socket từ model"""
        return self.model.get_socket()

    def get_ip_and_port(self):
        """Lấy IP và Port từ các Entry, đồng thời kiểm tra tính hợp lệ"""
        ip = self.view.entry_ip.get()
        port = self.view.entry_port.get()

        # Kiểm tra nếu IP hợp lệ
        if not self.is_valid_ip(ip):
            self.view.show_message("IP không hợp lệ! Vui lòng nhập IP đúng.")
            return None, None  # Trả về None nếu không hợp lệ

        # Kiểm tra nếu Port hợp lệ
        if not self.is_valid_port(port):
            self.view.show_message("Port không hợp lệ! Port phải là số nguyên trong khoảng 1 đến 65535.")
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
    
    
    #----------1. APP PROCESS ---------------------------
    def list_apps(self, client_socket, update_callback):
        thread = threading.Thread(
            target=self._list_apps_thread, 
            args=(client_socket, update_callback), 
            daemon=True)
        thread.start()

    def _list_apps_thread(self, client_socket, update_callback):
        try:
            self.model.send_command(client_socket, "LIST_APPS_RUNNING")
            response = self.model.receive_response_utf8(client_socket)
            app_list = self.model.parse_app_list(response)
            update_callback(app_list)
        except Exception as e:
            print(f"Lỗi trong thread list_apps: {e}")
            # Gọi callback với danh sách rỗng khi có lỗi
            update_callback([])
        
    def start_app(self, client_socket, app_name):
        self.model.send_command(client_socket, f"START_APP_BY_NAME {app_name}")
        response = self.model.receive_response(client_socket)
        return response

    def stop_app(self, client_socket, app_pid):
        self.model.send_command(client_socket, f"STOP_APP_BY_PID {app_pid}")
        response = self.model.receive_response(client_socket)
        return response   
    
    #----------2. SERVICE PROCESS ---------------------------
    def list_services(self, client_socket, update_callback):
        thread = threading.Thread(
            target=self._list_services_thread, 
            args=(client_socket, update_callback), 
            daemon=True)
        thread.start()

    def _list_services_thread(self, client_socket, update_callback):
        try:
            self.model.send_command(client_socket, "LIST_SERVICES_RUNNING")
            response = self.model.receive_response_utf8(client_socket)
            services_list = self.model.parse_service_list(response)
            update_callback(services_list)
        except Exception as e:
            print(f"Lỗi trong thread services_list: {e}")
            # Gọi callback với danh sách rỗng khi có lỗi
            update_callback([])
        
    def start_service(self, client_socket, service_name):
        self.model.send_command(client_socket, f"START_SERVICE {service_name}")
        response = self.model.receive_response(client_socket)
        return response

    def stop_service_by_pid(self, client_socket, service_pid):
        self.model.send_command(client_socket, f"STOP_SERVICE_BY_PID {service_pid}")
        response = self.model.receive_response(client_socket)
        return response  
    
    def stop_service_by_name(self, client_socket, service_name):
        self.model.send_command(client_socket, f"STOP_SERVICE_BY_NAME {service_name}")
        response = self.model.receive_response(client_socket)
        return response       
    
    #----------3. SHUTDOWN & RESET -------------------------
    def server_action(self, client_socket, action):
        # Tạo thông điệp xác nhận dựa trên hành động
        if action == "SHUTDOWN_SERVER":
            action_text = "tắt máy Server"
        elif action == "RESET_SERVER":
            action_text = "reset máy Server"
        else:
            action_text = "thực hiện hành động không xác định"
        
        # Hộp thoại xác nhận
        confirmation = messagebox.askyesno("Xác nhận", f"Bạn có muốn {action_text} không?")
        if confirmation:
            # Gửi lệnh đến server qua socket
            self.model.send_command(client_socket, action)
            
            # Nhận phản hồi từ server và hiển thị
            response = self.model.receive_response(client_socket)
            messagebox.showinfo("Phản hồi", response)
        else:
            messagebox.showinfo("Thông báo", f"Không {action_text.capitalize()}.")
    
    #----------4. SHARE_SCREEN -------------------------
    def share_screen_server(self, client_socket):
        client_ip, client_port = self.model.read_config_client("cl_config.json")
        if not client_ip or not client_port:
            messagebox.showinfo(title="Thông tin", message="Không thể đọc cấu hình.")
            return
        
        self.model.send_command(client_socket, "START_SCREEN_SHARING")
        server = StreamingServer(client_ip, client_port)
        server.start_server()  
        messagebox.showinfo(title="Thông tin", message="Bắt đầu chia sẻ màn hình")
        
        # Theo dõi phím ESC để dừng chia sẻ màn hình
        keyboard.wait('esc')  # Chờ đến khi phím ESC được nhấn

        # Khi dừng chia sẻ màn hình
        server.stop_server()
        self.view.show_message("Đã dừng chia sẻ màn hình.")     

    #----------5. KEYLOGGER -------------------------------
    def start_keylogger(self, client_socket):
        if not self.is_logging:
            self.is_logging = True
            self.model.send_command("START_KEYLOGGER")
            # self.view.show_message("Keylogger started!")

    def stop_keylogger(self):
        if self.is_logging:
            self.is_logging = False
            keys = self.model.send_command("STOP_KEYLOGGER")
            self.model.add_to_keys_buffer(keys)  # Lưu các phím vào bộ nhớ tạm
            # self.view.update_entry(" ".join(keys))
            # self.view.show_message("Keylogger stopped and keys fetched.")

    def print_keylogger(self):
        keys = self.model.send_command("FETCH_KEYLOGGER")
        self.model.add_to_keys_buffer(keys)  # Thêm phím vào bộ nhớ tạm
        existing_text = self.view.get_entry_text()
        self.view.update_entry(existing_text + " " + " ".join(keys))
        # self.view.show_message("Keys appended to the entry.")

    def clear_entry(self):
        self.view.update_entry("")
        self.model.clear_keys_buffer()
        # self.view.show_message("Entry cleared.")
        
    #----------6. DEL & COPY FILE --------------------------
    def get_files_from_server(self, client_socket, file_path, destination_path): 
        # Tạo tên file dựa trên đường dẫn từ server
        filename = os.path.basename(file_path)
        destination_path = os.path.join(destination_path, filename)            
        # Gửi yêu cầu copy file đến server với đường dẫn file đầy đủ
        self.model.send_command(client_socket, f"COPY_FILE {file_path}")
        # Nhận kích thước file
        file_size = int.from_bytes(client_socket.recv(4), byteorder='big')   
        
        if file_size == 0:
            # Nếu file co kich thuoc = 0 byte thi tạo một file rong
            with open(destination_path, 'wb') as f:
                pass # Tạo file rỗng
            # messagebox.showwarning(title="Dung luong file copy = 0", message=f"Tu dong tao file trong Folder {destination_path}.")
        else:
            # Nếu file có kích thước, sao chép dữ liệu xuống client
            with open(destination_path, 'wb') as f:
                data_received = 0
                while data_received < file_size:
                    packet = client_socket.recv(4096)
                    if not packet:
                        break
                    f.write(packet)
                    data_received += len(packet)
            # messagebox.showinfo(title="Kết quả", message=f"Da copy file {filename} tu server den Folder {destination_path} cua Client.") 

    def validate_file_on_server(self, client_socket, file_path):      
        self.model.send_command(client_socket, f"VALIDATE_FILE {file_path}")
        response = self.model.receive_response(client_socket)
        if "SUCCESS" in response:
            return True
        else:
            return False

    def delete_file_on_server(self, client_socket, file_path):       
        self.model.send_command(client_socket, f"DELETE_FILE {file_path}")
        response = self.model.receive_response(client_socket)
        if "SUCCESS" in response:
            return True
        else:
            return False