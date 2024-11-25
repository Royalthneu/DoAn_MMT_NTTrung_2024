from tkinter import messagebox
from model.CL_model import open_wd_client_socket, WidgetFactory, ScrolledTreeView

class app_view:
    def __init__(self, top, client_socket, controller):
        self.top = top        
        self.client_socket = client_socket
        self.controller = controller
        self.top.geometry("399x300+427+120")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(0, 0)
        self.top.title("APPLICATIONS PROCESS")
        self.top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")
        
        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()

    def create_widgets(self):
        # Treeview configuration
        self.tree_app = ScrolledTreeView(self.top, columns="Col1")
        self.tree_app.place(relx=0.05, rely=0.2, relheight=0.753, relwidth=0.892)
        self.tree_app.heading("#0", text="PID", anchor="center")
        self.tree_app.heading("Col1", text="Application Name", anchor="center")
        self.tree_app.column("#0", width=169, minwidth=20, stretch=1, anchor="w")
        self.tree_app.column("Col1", width=170, minwidth=20, stretch=1, anchor="w")

        # Button configuration
        self.btn_list_app = self.widget_factory.create_button("LIST APPS", 0.05, 0.043, 77, 36)
        
        
        self.btn_start_app = self.widget_factory.create_button("START APP", 0.301, 0.043, 77, 36)
        self.btn_start_app.configure(command= self.btn_start_app_click)
        
        self.btn_stop_app = self.widget_factory.create_button("STOP APP", 0.551, 0.043, 77, 36)
        self.btn_stop_app.configure(command= self.btn_stop_app_click)
        
        self.btn_clear_list_app = self.widget_factory.create_button("CLEAR", 0.802, 0.043, 57, 36)
    
    def btn_start_app_click(self):
        from view.CL_frm_nhap_Ten_view import frm_nhap_Ten_view
        open_wd_client_socket(self.top, self.client_socket, self.controller, frm_nhap_Ten_view)   
    
    def btn_stop_app_click(self):
        from view.CL_frm_nhap_PID_view import frm_nhap_PID_view
        open_wd_client_socket(self.top, self.client_socket, self.controller, frm_nhap_PID_view)  
