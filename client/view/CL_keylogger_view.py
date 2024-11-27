from model.CL_model import WidgetFactory

class keylogger_view:
    def __init__(self, top, client_socket, controller):
        self.top = top        
        self.client_socket = client_socket
        self.controller = controller
        self.top.geometry("637x489+1307+122")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(0,  0)
        self.top.title("KEYLOGGER")
        self.top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()

    def create_widgets(self):
        # Button configuration using WidgetFactory
        self.btn_clear = self.widget_factory.create_button("CLEAR", 0.738, 0.041, 97, 36)
        self.btn_print_keylogger = self.widget_factory.create_button("IN KEYLOGGER", 0.488, 0.043, 127, 36)
        self.btn_stop_keylogger = self.widget_factory.create_button("TAT KEYLOGGER", 0.27, 0.043, 107, 36)
        self.btn_start_keylogger = self.widget_factory.create_button("BAT KEYLOGGER", 0.05, 0.043, 107, 36)