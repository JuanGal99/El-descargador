class ListaReproduccion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []

    def agregar(self, cancion):
        if cancion in self.canciones:
            raise ValueError("La cancion ya esta en la lista")
        self.canciones.append(cancion)

    agregar_cancion = agregar


    def eliminar(self, cancion):
        if cancion in self.canciones:
            self.canciones.remove(cancion)
            return True
        return False

    def ordenar(self, criterio):
        if self.canciones and hasattr(self.canciones[0], criterio):
            self.canciones.sort(key= lambda c: getattr(c, criterio))
            
    def marcarFavorita(self, cancion):
        if cancion in self.canciones:
            cancion.favorito = True