import json
import socket
import subprocess
from tkinter import messagebox, ttk
import tkinter as tk

import keyboard

class cl_model:
    def __init__(self, view):
        self.client_socket = None
        self.connected = False
        self.view = view
        self.keys_buffer = []
        
    def connect_to_server(self, server_ip, server_port):
        # if self.connected:
        #     raise ConnectionError("Đã kết nối đến server!")        
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, server_port))
            self.connected = True
            return "Kết nối thành công đến server!"

        except socket.error as e:
            self.connected = False
            self.client_socket = None
            raise ConnectionError(f"Lỗi khi kết nối đến server: {e}")
    
    def get_socket(self):
        return self.client_socket
        
    def send_command(self, client_socket, command):
        client_socket.sendall(command.encode())  # Mã hóa lệnh và gửi
        
    # def send_command_recieve_keylogger(self, command):
    #     try:
    #         self.client_socket.sendall(command.encode())
    #         if command in ["STOP_KEYLOGGER", "FETCH_KEYLOGGER"]:
    #             data = self.client_socket.recv(65535).decode()
    #             return data.split(" ") if data else []
    #         return []
    #     except Exception as e:
    #         print(f"Error sending command: {e}")
    #         return []

    def receive_response_list(self, client_socket, buffer_size=65535):
        self.clear_socket_buffer(client_socket) # Có xóa buffer cũ 
        return client_socket.recv(buffer_size).decode() # Nhận và giải mã phản hồi        
    
    def receive_response_utf8_list(self, client_socket, buffer_size=65535):
        self.clear_socket_buffer(client_socket)  # Có xóa buffer cũ 
        return client_socket.recv(buffer_size).decode("utf-8")  # Nhận và giải mã phản hồi
    
    def receive_response(self, client_socket, buffer_size=65535):
        return client_socket.recv(buffer_size).decode() # Nhận và giải mã phản hồi        
    
    def receive_response_utf8(self, client_socket, buffer_size=65535):
        return client_socket.recv(buffer_size).decode("utf-8")  # Nhận và giải mã phản hồi
    
    
    def clear_socket_buffer(self, client_socket):
        try:
            client_socket.setblocking(False)  # Tạm thời chuyển socket về non-blocking
            while True:
                _ = client_socket.recv(1024)  # Đọc và bỏ qua dữ liệu cũ trong buffer
        except BlockingIOError:
            pass  # Không còn dữ liệu trong buffer
        finally:
            client_socket.setblocking(True)  # Chuyển socket về blocking mode

    
    def show_message(self, message):
        messagebox.showinfo("Thông báo", message)
    
    def set_ip_address(self, ip):
        self.server_ip = ip

    def set_port(self, port):
        self.server_port = port
        
    # Chuyển đổi output của lệnh 'tasklist' thành danh sách [(pid, app_name), ...].
    def parse_app_list(self, response):
        app_list = []
        try:
            # Tách phản hồi thành các dòng
            lines = response.splitlines()
            # Loại bỏ 3 dòng đầu tiên
            lines = lines[3:]
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    app_name = parts[0]
                    pid = parts[1]
                    app_list.append((pid, app_name))
        except Exception as e:
            raise ValueError(f"Lỗi khi phân tích danh sách ứng dụng: {e}")
        
        return app_list

    def parse_service_list(self, response):
        service_list = []
        try:
            # Tách phản hồi thành các dòng
            lines = response.splitlines()
            # Loại bỏ các dòng trống hoặc không cần thiết và dòng tiêu đề
            lines = [line.strip() for line in lines if line.strip()]
            
            # Bỏ qua dòng tiêu đề (dòng đầu tiên)
            for line in lines[1:]:
                # Tách dòng theo khoảng trắng để lấy các thành phần
                parts = line.split(None, 1)  # Tách thành tối đa 2 phần
                if len(parts) == 2:
                    pid = parts[0]
                    service_name = parts[1]
                    service_list.append((pid, service_name))
        except Exception as e:
            raise ValueError(f"Lỗi khi phân tích danh sách dịch vụ: {e}")
        
        return service_list
    
    # Hàm kiểm tra sự tồn tại của file cấu hình
    def check_config_file(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r"):
                return True
        except FileNotFoundError:
            return False 
    
    # Hàm cập nhật cấu hình
    def update_config_client(self, CONFIG_FILE, server_ip=None, server_port=None, client_ip=None, client_port=None):
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
            # messagebox.showinfo("Cập nhât", f"cl_config.json updated: Server IP = {config['server_ip']}, Server Port = {config['server_port']}, Client IP = {config['client_ip']}, Client Port = {config['client_port']}")
            print("Cập nhât", f"cl_config.json updated: Server IP = {config['server_ip']}, Server Port = {config['server_port']}, Client IP = {config['client_ip']}, Client Port = {config['client_port']}") #Debugging
        else:
            messagebox.showerror("Lỗi file cấu hình IP PORT", f"cl_config.json không tồn tại.")

    # Hàm đọc cấu hình client từ file
    def read_config_client(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
            return config.get("client_ip"), config.get("client_port")
        except json.JSONDecodeError:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "cl_config.json không hợp lệ. Vui lòng kiểm tra nội dung file.")
            return None, None
        except FileNotFoundError:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "cl_config.json không tồn tại.")
            return None, None    
        
    def read_config_server(self, CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
            return config.get("server_ip"), config.get("server_port")
        except json.JSONDecodeError:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "File cấu hình không hợp lệ. Vui lòng kiểm tra nội dung file.")
            return None, None
        except FileNotFoundError:
            messagebox.showerror("Lỗi file cấu hình IP PORT", "File cấu hình không tồn tại.")
            return None, None 
    
            
#Thiet ke giao dien
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped


#Thiet ke giao dien
class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')   

class WidgetFactory:
    def __init__(self, window):
        self.window = window

    def create_label(self, text, relx, rely, width, height):
        label = tk.Label(self.window, text=text, background="#d9d9d9", foreground="#000000", anchor='w')
        label.place(relx=relx, rely=rely, width=width, height=height)
        return label

    def create_entry(self, relx, rely, relwidth, height):
        entry = tk.Entry(self.window, background="white", foreground="#000000")
        entry.place(relx=relx, rely=rely, relwidth=relwidth, height=height)
        return entry

    def create_button(self, text, relx, rely, width, height):
        button = tk.Button(self.window, text=text, background="#d9d9d9", foreground="#000000")
        button.place(relx=relx, rely=rely, width=width, height=height)
        return button

    def create_separator(self, relx, rely, relwidth=0.946):
        separator = ttk.Separator(self.window, orient="horizontal")
        separator.place(relx=relx, rely=rely, relwidth=relwidth)
        
def open_wd_client_socket_from(root, client_socket, controller, window_class, from_screen):
    # Tạo cửa sổ mới
    top = tk.Toplevel(root)
    # Khởi tạo cửa sổ từ lớp window_class
    window_class (top=top, client_socket=client_socket, controller=controller, from_screen=from_screen)
    # Đảm bảo rằng cửa sổ chính không thể click khi cửa sổ top đang mở
    # top.grab_set()    
    # Khi cửa sổ top đóng, hủy grab_set
    top.protocol("WM_DELETE_WINDOW", lambda: (top.grab_release(), top.destroy()))
    
def open_wd_client_socket(root, client_socket, controller, window_class):
    # Tạo cửa sổ mới
    top = tk.Toplevel(root)
    # Khởi tạo cửa sổ từ lớp window_class
    window_class (top=top, client_socket=client_socket, controller=controller)
    # Đảm bảo rằng cửa sổ chính không thể click khi cửa sổ top đang mở
    # top.grab_set()    
    # Khi cửa sổ top đóng, hủy grab_set
    top.protocol("WM_DELETE_WINDOW", lambda: (top.grab_release(), top.destroy()))
    
def run_powershell_command(command):
    """Hàm thực thi lệnh PowerShell và trả về kết quả hoặc lỗi"""
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            check=True, capture_output=True, text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
