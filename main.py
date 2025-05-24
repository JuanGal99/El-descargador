from app.view.InterfazUsuario import VistaApp
from app.controller.ControladorPrincipal import Controlador

def main():
    vista = VistaApp(None)  # Inicialmente sin controlador
    controlador = Controlador(vista)
    vista.controlador = controlador  # Vincular controlador con la vista
    vista.mainloop()

if __name__ == "__main__":
    main()
