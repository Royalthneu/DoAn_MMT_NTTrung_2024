# SV_controller.py
import threading

class SV_Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.client_socket = None
        self.client_ip = None
        self.client_port = None
        self.view.btn_open.config(command=self.start_server)
        self.view.btn_close.config(command=self.stop_server)

    def start_server(self):
        if self.model.start_server():
            self.view.show_message("THÔNG BÁO", f"Server is listening on: {self.model.server_ip}:{self.model.server_port}")
            self.view.set_lbl_status("Server is opening")
            self.view.set_lbl_server_ip(self.model.server_ip)
            self.view.disable_open_button()
            self.view.enable_close_button()
            threading.Thread(target=self.listen_for_clients,daemon=True).start()
        else:
            self.view.show_message("Lỗi", "Không thể khởi động server.")
            self.view.enable_open_button()
            self.view.disable_close_button()
            return

    def listen_for_clients(self):
        try:
            while True:
                self.client_socket, self.addr = self.model.accept_client()
                if self.client_socket:
                    print(f"Client connected from {self.addr}")
                    self.client_ip, self.client_port = self.addr
                    self.model.update_config_server("sv_config.json", self.model.server_ip, self.model.server_port, self.client_ip, 6789)
                    client_thread = threading.Thread(
                        target=self.handle_client, args=(self.client_socket, self.addr), daemon=True)
                    client_thread.start()
                else:
                    break  # Nếu không có client kết nối, thoát khỏi vòng lặp
        except Exception as e:
            print(f"Error: {e}")
            self.view.enable_open_button()
            self.view.disable_close_button()
        finally:
            self.stop_server()
            self.view.enable_open_button()
            self.view.disable_close_button()


    def handle_client(self, client_socket, addr):
        """Xử lý lệnh từ Client"""
        try:
            while True:
                command = self.model.receive_response(client_socket)

                #1. List app running
                if command == "LIST_APPS_RUNNING":
                    result = self.model.list_apps_running()  # Chuyển lệnh trả về từ model
                    self.model.send_command_utf8(client_socket, result)  # Gửi kết quả lại cho client
                
                elif command.startswith("START_APP_BY_NAME"):
                    name = command.split(" ", 1)[1]
                    result = self.model.start_app_by_name(name)
                    self.model.send_command(client_socket, result)                
                
                elif command.startswith("STOP_APP_BY_PID"):
                    pid = int(command.split(" ", 1)[1])
                    result = self.model.stop_app_by_pid(pid)
                    self.model.send_command(client_socket, result)
                
                elif command == "CLEAR_LIST_APPS":
                    self.model.send_command(client_socket, command)

                #2. List services running
                elif command == "LIST_SERVICES_RUNNING":
                    result = self.model.list_running_services()
                    self.model.send_command_utf8(client_socket, result)

                elif command.startswith("START_SERVICE"):
                    service_name = command.split(" ", 1)[1]
                    result = self.model.start_service(service_name)
                    self.model.send_command(client_socket, result)

                elif command.startswith("STOP_SERVICE_BY_PID"):
                    service_pid = int(command.split(" ", 1)[1])
                    result = self.model.stop_service_by_pid(service_pid)
                    self.model.send_command(client_socket, result)
                
                elif command.startswith("STOP_SERVICE_BY_NAME"):
                    service_name = command.split(" ", 1)[1]
                    result = self.model.stop_service_by_name(service_name)
                    self.model.send_command(client_socket, result)
                    
                elif command == "CLEAR_LIST_SERVICES":
                    self.model.send_command(client_socket, command)
                
                #3. Shutdown_reset
                elif command == "SHUTDOWN_SERVER":
                    result = self.model.shutdown_server()
                    self.model.send_command(client_socket, result)

                elif command == "RESET_SERVER":
                    result = self.model.reset_server()
                    self.model.send_command(client_socket, result)

                #4. Screen_share
                elif command.startswith("START_SCREEN_SHARING"):               
                    client_ip, client_port = self.model.read_config_server("sv_config.json")
                    client_view_stream, stream_thread = self.model.start_screen_sharing(client_ip, client_port)
                    stream_thread.start()
                    self.model.send_command(client_socket, "Screen sharing started.")

                    # Chờ dừng chia sẻ màn hình
                    while True:
                        stop_command = self.model.receive_response(client_socket)
                        if stop_command == "STOP_SCREEN_SHARING":
                            result = self.model.stop_screen_sharing(client_view_stream)
                            self.model.send_command(client_socket, result)
                            break

                #5. Key Logger
                elif command == "START_KEYLOGGER":
                    listener = self.model.start_keylogger()
                    self.model.send_command(client_socket, "Keylogger started.")
                    # Listen for stop command
                    while True:
                        stop_command = self.model.receive_response(client_socket)
                        if stop_command == "STOP_KEYLOGGER":
                            result = self.model.stop_keylogger(listener)
                            self.model.send_command(client_socket, result)
                            break

                #6. Del va Copy
                if command.startswith("COPY_FILE"):
                    file_path = command.split(" ", 1)[1]
                    self.model.copy_file(client_socket, file_path)

                elif command.startswith("VALIDATE_FILE"):
                    file_path = command.split(" ", 1)[1]
                    response = self.model.validate_file(file_path)
                    self.model.send_command(client_socket, response)

                elif command.startswith("DELETE_FILE"):
                    file_path = command.split(" ", 1)[1]
                    response = self.model.delete_file(file_path)                    
                    self.model.send_command(client_socket, response)

                else:
                    self.model.send_command(client_socket, "Unknown command.")

        except Exception as e:
            self.view.show_message(title = "Ngoại lệ", message = f"Error handling client {addr}: {str(e)}")
        finally:
            client_socket.close()
            self.view.show_message(title = "Thông báo", message = f"Client disconnected: {addr}")

    def stop_server(self):
        self.model.close_server()
        self.view.set_lbl_status("Server is closed")
        self.view.set_lbl_server_ip("Bí mật")
        self.view.disable_close_button()
        self.view.enable_open_button()
