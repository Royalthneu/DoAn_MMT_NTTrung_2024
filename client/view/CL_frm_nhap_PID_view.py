from model.CL_model import WidgetFactory

class frm_nhap_PID_view:
    def __init__(self, top, client_socket, controller):
        self.top = top
        self.client_socket = client_socket
        self.controller = controller
        self.view = None        
        self.top.geometry("350x60+20+200")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(1, 1)
        self.top.title("Nhập")
        self.top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()
        
    def create_widgets(self):
        # Label configuration
        self.Lb_nhap_PID = self.widget_factory.create_label("Nhập PID", 0.016, 0.25, 82, 25)
        # Entry configuration
        self.entry_nhap_PID = self.widget_factory.create_entry(0.2, 0.25, 0.5, 25)
        # Button configuration with custom cursor
        self.btn_nhap_PID = self.widget_factory.create_button("OK", 0.75, 0.25, 60, 25)
        self.btn_nhap_PID.configure(command= self.btn_nhap_PID_click)
    
    def btn_nhap_PID_click(self):
        pid = self.entry_nhap_PID.get() 
        if pid.isdigit():
            self.controller.stop_app(self.client_socket, pid)
            self.top.destroy()
        else:
            message = "PID không hợp lệ! Vui lòng nhập lại."
            self.view.show_message(message)

        