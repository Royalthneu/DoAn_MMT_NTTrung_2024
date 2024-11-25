import tkinter as tk
from view.CL_root_view import root_view
from controller.CL_controller import cl_controller
from model.CL_model import cl_model

def main():
    window = tk.Tk()

    # Khởi tạo các thành phần của MVC
    view = root_view(window)
    model = cl_model (view)    
    controller = cl_controller (view, model)  
    view.controller = controller
    
    window.mainloop()
    
if __name__ == "__main__":
    main() 