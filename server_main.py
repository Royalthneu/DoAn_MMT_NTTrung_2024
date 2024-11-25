# main.py
import socket
import tkinter as tk

from server.view.server_view import SV_View
from server.model.server_model import SV_Model
from server.controller.server_controller import SV_Controller

def main():

    window = tk.Tk()
    server_ip = socket.gethostbyname(socket.gethostname())
    port = 8081
    
    view = SV_View(window)
    model = SV_Model(server_ip, port)    
    controller = SV_Controller(model, view)
    
    window.mainloop()

if __name__ == "__main__":
    main()
