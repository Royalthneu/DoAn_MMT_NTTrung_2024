from model.CL_model import WidgetFactory
from tkinter import filedialog, ttk, messagebox
import tkinter as tk

class del_copy_view:
    def __init__(self, top, client_socket, controller):
        self.top = top        
        self.client_socket = client_socket
        self.controller = controller
        self.top.geometry("637x207+1315+693")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(1, 1)
        self.top.title("DELETE-COPY")
        self.top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()

    def create_widgets(self):
        # Separator
        self.TSeparator3 = ttk.Separator(self.top)
        self.TSeparator3.place(relx=0.0, rely=0.391, relwidth=1.008)

        # Label configuration
        self.Label4 = self.widget_factory.create_label("PATH FILE", 0.016, 0.193, 66, 16)
        # self.Label4_1 = self.widget_factory.create_label("SOURCE FILE", 0.016, 0.483, 76, 16)
        self.Label4_1_1 = self.widget_factory.create_label("DESTINATION", 0.016, 0.725, 82, 16)
        self.Label4_1_1_1 = self.widget_factory.create_label("FOLDER", 0.031, 0.821, 53, 16)

        # Entry configuration
        self.entry_path_file_server = self.widget_factory.create_entry(0.126, 0.145, 0.697, 40) 
        # self.entry_copy = self.widget_factory.create_entry(0.157, 0.435, 0.666, 40)
        self.entry_paste = self.widget_factory.create_entry(0.157, 0.725, 0.666, 40)

        # Button configuration with custom cursor        
        self.btn_check_path_on_server = self.widget_factory.create_button("CHECK PATH", 0.848, 0.145, 87, 36)
        self.btn_check_path_on_server.configure(command= self.btn_check_path_on_server_click)     
        
        self.btn_del_file_on_server = self.widget_factory.create_button("DELETE", 0.848, 0.435, 87, 36)
        self.btn_del_file_on_server.configure(command= self.btn_del_file_click)   
        
        self.btn_paste_destination_on_client = self.widget_factory.create_button("PASTE", 0.848, 0.725, 87, 36)
        self.btn_paste_destination_on_client.configure(command= self.btn_paste_destination_click)  

    def btn_check_path_on_server_click(self):
        self.handle_file_operation("check")

    def btn_paste_destination_click(self):
       self.handle_file_operation("paste")

    def btn_del_file_click(self):
       self.handle_file_operation("delete")

    def handle_file_operation(self, operation_type):
        """Thực hiện các thao tác file (kiểm tra, sao chép, xóa) dựa trên operation_type."""
        path_file_on_server = self.entry_path_file_server.get()

        # Kiểm tra xem có đường dẫn file không
        if not path_file_on_server:
            messagebox.showwarning(title="Lỗi nhập", message="Bạn chưa nhập đường dẫn file trên server")
            return

        # Kiểm tra file trên server
        check = self.controller.validate_file_on_server(self.client_socket, path_file_on_server)
        if check == False:
            messagebox.showerror(title="Lỗi đường dẫn", message="Không tồn tại đường dẫn")
            return
        else:
            # Xử lý theo loại thao tác
            if operation_type == 'check':
                messagebox.showinfo(title="Thành công", message="File hợp lệ và có thể sao chép hoặc xóa.")
            elif operation_type == 'paste':
                # Mở hộp thoại chọn thư mục đích
                destination_path = filedialog.askdirectory(title="Chọn thư mục sẽ paste")
                self.update_entry_paste(destination_path)
                self.controller.get_files_from_server(self.client_socket, path_file_on_server, self.entry_paste.get())
                messagebox.showinfo("Thông báo", "Đã copy & paste file thành công")
            elif operation_type == 'delete':
                self.controller.delete_file_on_server(self.client_socket, path_file_on_server)
                messagebox.showinfo("Thông báo", "File đã được xóa thành công")
                    
    def update_entry_path_file(self, text):
        self.entry_path_file_server.delete(0, tk.END)
        self.entry_path_file_server.insert(0, text)

    def update_entry_paste(self, text):
        self.entry_paste.delete(0, tk.END)
        self.entry_paste.insert(0, text)