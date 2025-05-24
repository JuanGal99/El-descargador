from . import ListaReproduccion

class BibliotecaMusical:
    def __init__(self):
        self.canciones = []
        self.listas = []

    def agregar_cancion(self, cancion):
        if cancion in self.canciones:
            raise ValueError("La cancion ya esta en la biblioteca")
        self.canciones.append(cancion)

    def crear_lista(self, nombre):
        lista = ListaReproduccion(nombre)
        self.listas.append(lista)
        return lista

    def buscar(self, texto):
        return [c for c in self.canciones if texto.lower() in c.titulo.lower()]
    
    def obtener_favoritas(self):
        return[c for c in self.canciones if c.favorito]