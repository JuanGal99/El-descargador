class BibliotecaMusical:
    def __init__(self):
        self.canciones = []

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)

    def buscar(self, texto):
        return [c for c in self.canciones if texto.lower() in c.titulo.lower()]