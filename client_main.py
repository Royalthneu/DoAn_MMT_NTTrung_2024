import tkinter as tk
from client.view.CL_root_view import root_view
from client.controller.CL_root_controller import root_controller
from client.model.CL_root_model import root_model

if __name__ == "__main__":
    root = tk.Tk()

    # Khởi tạo các thành phần của MVC
    root_model = root_model()
    root_view = root_view(root, controller=None)
    root_controller = root_controller(root_view, root_model)  
    
    # Liên kết Controller vào View  
    root_view.controller = root_view 

    # Bắt đầu với màn hình root
    root_controller.show_root_view  

    root.mainloop()