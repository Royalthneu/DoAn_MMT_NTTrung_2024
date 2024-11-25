from tkinter import messagebox
from model.CL_model import WidgetFactory, ScrolledTreeView

class service_view:
    def __init__(self, client_socket, top=None):
        self.top = top
        self.client_socket = client_socket
        self.top.geometry("420x300+853+120")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(0, 0)
        self.top.title("SERVICES PROCESS")
        self.top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()

    def create_widgets(self):
        # Treeview configuration
        self.tree_app_1 = ScrolledTreeView(self.top, columns="Col1")
        self.tree_app_1.place(relx=0.05, rely=0.2, relheight=0.753, relwidth=0.893)
        self.tree_app_1.heading("#0", text="Service PID", anchor="center")
        self.tree_app_1.column("#0", width=179, minwidth=20, stretch=1, anchor="w")
        self.tree_app_1.heading("Col1", text="Service Name", anchor="center")
        self.tree_app_1.column("Col1", width=179, minwidth=20, stretch=1, anchor="w")
        
        # Button configuration
        self.btn_list_service = self.widget_factory.create_button("LIST SERVICES", 0.05, 0.043, 87, 36)
        self.btn_start_service = self.widget_factory.create_button("START SERVICES", 0.3, 0.043, 87, 36)
        self.btn_stop_service = self.widget_factory.create_button("STOP SERVICES", 0.55, 0.043, 87, 36)
        self.btn_clear_list_service = self.widget_factory.create_button("CLEAR", 0.802, 0.043, 57, 36)
        