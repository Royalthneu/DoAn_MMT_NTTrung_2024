import tkinter as tk
from view.CL_root_view import root_view
from controller.CL_root_controller import root_controller
from model.CL_root_model import root_model

def main():
    window = tk.Tk()

    # Khởi tạo các thành phần của MVC
    view = root_view(window)
    model = root_model(view)    
    controller = root_controller(view, model)  
    view.controller = controller
    
    window.mainloop()
    
if __name__ == "__main__":
    main()