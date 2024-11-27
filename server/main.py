# main.py
import socket
import tkinter as tk

from view.server_view import SV_View
from model.server_model import SV_Model
from controller.server_controller import SV_Controller

def main():

    window = tk.Tk()
    server_ip = socket.gethostbyname(socket.gethostname())
    server_port = 8081
    
    view = SV_View(window)
    model = SV_Model(server_ip, server_port)    
    controller = SV_Controller(model, view)
    
    window.mainloop()

if __name__ == "__main__":
    main() 
