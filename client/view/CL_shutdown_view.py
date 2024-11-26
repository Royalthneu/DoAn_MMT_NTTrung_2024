from model.CL_model import WidgetFactory

class shutdown_view:
    def __init__(self, top, client_socket, controller):
        self.top = top        
        self.client_socket = client_socket
        self.controller = controller
        self.top.geometry("374x110+13+884")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(0, 0)
        self.top.title("SHUTDOWN RESET SERVER")
        self.top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()

    def create_widgets(self):
        self.btn_cl_shutdown_sv = self.widget_factory.create_button("SHUT DOWN SERVER", 0.246, 0.091, 167, 36)
        self.btn_cl_shutdown_sv.configure(command=self.btn_cl_shutdown_sv_click)
        
        self.btn_cl_reset_sv = self.widget_factory.create_button("RESET SERVER", 0.246, 0.545, 167, 36)
        self.btn_cl_reset_sv.configure(command=self.btn_cl_reset_sv_click)
        
    def btn_cl_shutdown_sv_click(self):
        self.controller.server_action(self.client_socket, "SHUTDOWN_SERVER")
        
    def btn_cl_reset_sv_click(self):
        self.controller.server_action(self.client_socket, "RESET_SERVER")