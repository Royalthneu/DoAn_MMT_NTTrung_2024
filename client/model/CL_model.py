import socket
from tkinter import messagebox, ttk
import tkinter as tk

class cl_model:
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
    
    def get_socket(self):
        return self.client_socket
        
    def send_command(self, client_socket, command):
        client_socket.sendall(command.encode())  # Mã hóa lệnh và gửi

    def receive_response(self, client_socket, buffer_size=65535):
        response = client_socket.recv(buffer_size).decode()  # Nhận và giải mã phản hồi
    
    def show_message(self, message):
        messagebox.showinfo("Thông báo", message)
    
    def set_ip_address(self, ip):
        self.server_ip = ip

    def set_port(self, port):
        self.server_port = port
        
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
        
def open_wd_client_socket(root, client_socket, controller, window_class):
    # Tạo cửa sổ mới
    top = tk.Toplevel(root)
    # Khởi tạo cửa sổ từ lớp window_class
    window_class (top=top, client_socket=client_socket, controller=controller)
    # Đảm bảo rằng cửa sổ chính không thể click khi cửa sổ top đang mở
    top.grab_set()    
    # Khi cửa sổ top đóng, hủy grab_set
    top.protocol("WM_DELETE_WINDOW", lambda: (top.grab_release(), top.destroy()))