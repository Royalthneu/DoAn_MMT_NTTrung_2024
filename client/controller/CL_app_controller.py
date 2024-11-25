import socket
from tkinter import messagebox
from model.CL_app_model import app_model
from view.CL_app_view import app_view

class app_controller:
    def __init__(self, window):
        self.window = window
        self.model = app_model()
        self.view = app_view(window)
    
    