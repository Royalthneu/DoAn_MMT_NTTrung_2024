from model.CL_model import WidgetFactory, ScrolledTreeView, open_wd_client_socket_from


class service_view:
    def __init__(self, top, client_socket, controller):
        self.top = top
        self.client_socket = client_socket
        self.controller = controller
        self.top.geometry("420x400+853+120")
        self.top.minsize(120, 1)
        self.top.maxsize(5564, 1901)
        self.top.resizable(0, 0)
        self.top.title("SERVICES PROCESS")
        self.top.configure(
            background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="#000000")

        # Create an instance of WidgetFactory
        self.widget_factory = WidgetFactory(self.top)
        self.create_widgets()

    def create_widgets(self):
        # Treeview configuration
        self.tree_app_1 = ScrolledTreeView(self.top, columns="Col1")
        self.tree_app_1.place(relx=0.05, rely=0.27,
                              relheight=0.703, relwidth=0.893)
        self.tree_app_1.heading("#0", text="Service PID", anchor="center")
        self.tree_app_1.column(
            "#0", width=179, minwidth=20, stretch=1, anchor="w")
        self.tree_app_1.heading("Col1", text="Service Name", anchor="center")
        self.tree_app_1.column(
            "Col1", width=179, minwidth=20, stretch=1, anchor="w")

        # Button configuration
        self.btn_list_service = self.widget_factory.create_button(
            "LIST SERVICES", 0.05, 0.043, 87, 36)
        self.btn_list_service.configure(command=self.btn_list_service_click)

        self.btn_start_service = self.widget_factory.create_button(
            "START SERVICES", 0.3, 0.043, 87, 36)
        self.btn_start_service.configure(command=self.btn_start_service_click)

        self.btn_stop_service = self.widget_factory.create_button(
            "STOP BY PID", 0.55, 0.043, 87, 36)
        self.btn_stop_service.configure(command=self.btn_stop_service_click)

        self.btn_stop_service_by_name = self.widget_factory.create_button(
            "STOP BY NAME", 0.55, 0.153, 87, 36)
        self.btn_stop_service_by_name.configure(
            command=self.btn_stop_service_by_name_click)

        self.btn_clear_list_service = self.widget_factory.create_button(
            "CLEAR", 0.802, 0.043, 57, 36)
        self.btn_clear_list_service.configure(
            command=self.btn_clear_list_service_click)

    def btn_list_service_click(self):
        self.controller.list_services(
            self.client_socket, self.update_tree_view)

    def btn_start_service_click(self):
        from view.CL_frm_nhap_Ten_view import frm_nhap_Ten_view
        open_wd_client_socket_from(self.top, self.client_socket, self.controller,
                                   frm_nhap_Ten_view, from_screen="service_view_btn_start")

    def btn_stop_service_click(self):
        from view.CL_frm_nhap_PID_view import frm_nhap_PID_view
        open_wd_client_socket_from(
            self.top, self.client_socket, self.controller, frm_nhap_PID_view, from_screen="service_view")

    def btn_stop_service_by_name_click(self):
        from view.CL_frm_nhap_Ten_view import frm_nhap_Ten_view
        open_wd_client_socket_from(self.top, self.client_socket, self.controller,
                                   frm_nhap_Ten_view, from_screen="service_view_btn_stop")

    def btn_clear_list_service_click(self):
        for item in self.tree_app_1.get_children():
            self.tree_app_1.delete(item)

    def update_tree_view(self, services_list):
        for item in self.tree_app_1.get_children():
            self.tree_app_1.delete(item)
        for pid, services_name in services_list:
            self.tree_app_1.insert("", "end", text=pid,
                                   values=(services_name,))
