import socket
from tkinter import messagebox

class app_model:
    def __init__(self):
        self.client_socket = None
        self.connected = False
