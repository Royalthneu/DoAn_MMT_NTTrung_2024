class root_controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def show_root_view(self):
        self.view.root_view