import logging
import tkinter as tk
from app.view.InterfazUsuario import InterfazUsuario
from app.controller.ControladorPrincipal import ControladorPrincipal
from app.model.RutasAplicacion import obtener_directorio_datos

def main():
    directorio_datos = obtener_directorio_datos()
    logging.basicConfig(
        filename=directorio_datos / "el_descargador.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
    )
    root = tk.Tk()
    vista = InterfazUsuario(root)
    controlador = ControladorPrincipal(vista)
    vista.set_controlador(controlador)
    root.mainloop()

if __name__ == "__main__":
    main()
