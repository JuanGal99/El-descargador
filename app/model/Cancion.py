class Cancion: 
    def __init__(self, titulo, artista, duracion, pathArchivo):
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion
        self.pathArchivo = pathArchivo
        self.favorito = False

    def __str__(self):
        return f"{self.titulo} - {self.artista}"