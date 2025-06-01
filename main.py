import tkinter as tk
from app.view.InterfazUsuario import InterfazUsuario
from app.controller.ControladorPrincipal import ControladorPrincipal

def main():
    root = tk.Tk()
    vista = InterfazUsuario(root)
    controlador = ControladorPrincipal(vista)
    vista.set_controlador(controlador)
    root.mainloop()

if __name__ == "__main__":
    main()
