from app.model.ControladorMedia import ControladorMedia
from app.model.GestorDescargas import GestorDescargas
from app.model.BibliotecaMusical import BibliotecaMusical

class ControladorPrincipal:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = BibliotecaMusical()
        self.media = ControladorMedia()
        self.descargador = GestorDescargas()

    def descargar_cancion(self, url):
        try:
            nueva = self.descargador.descargar(url)
        
            for existente in self.modelo.canciones:
                if (nueva.titulo == existente.titulo and
                    nueva.artista == existente.artista):
                    self.vista.mostrar_mensaje("⚠️ La canción ya está en la biblioteca.")
                    return
        
            self.modelo.agregar_cancion(nueva)
            self.vista.mostrar_todas()
            self.vista.mostrar_mensaje("✅ Canción descargada correctamente.")
        except Exception as e:
            self.vista.mostrar_mensaje(f"❌ Error al descargar: {str(e)}")


    def reproducir_cancion(self, index):
        try:
            cancion = self.modelo.canciones[index]
            self.media.play(cancion.pathArchivo)
        except IndexError:
            self.vista.mostrar_mensaje("❌ Índice inválido.")

    def pausar(self):
        self.media.pausar()

    def detener(self):
        self.media.detener()

    def filtrar_por_texto(self, texto):
        return self.modelo.buscar(texto)

    def obtener_favoritas(self):
        return self.modelo.obtener_favoritas()
    
    def obtener_todas(self):
        return self.modelo.canciones


    def marcar_favorita(self, index):
        cancion = self.modelo.canciones[index]
        cancion.favorito = not cancion.favorito
        self.modelo.guardar_datos()

    def eliminar_cancion(self, index):
        try:
            cancion = self.modelo.canciones[index]
            self.modelo.eliminar_cancion(cancion)
        except IndexError:
            self.vista.mostrar_mensaje("❌ No se pudo eliminar.")

    def eliminar_cancion_objeto(self, cancion):
        try:
            self.modelo.eliminar_cancion(cancion)
            self.modelo.guardar_datos()
        except Exception as e:
            self.vista.mostrar_mensaje(f"❌ No se pudo eliminar la canción: {str(e)}")


    def editar_cancion(self, index, nuevo_titulo, nuevo_artista):
        cancion = self.modelo.canciones[index]
        cancion.titulo = nuevo_titulo
        cancion.artista = nuevo_artista
        self.modelo.guardar_datos()

    def crear_lista(self, nombre):
        try:
            self.modelo.crear_lista(nombre)
            self.vista.mostrar_mensaje(f"✅ Lista '{nombre}' creada.")
        except ValueError as e:
            self.vista.mostrar_mensaje(str(e))

    def obtener_nombres_listas(self):
        return [lista.nombre for lista in self.modelo.listas]

    def agregar_cancion_a_lista(self, index_cancion, nombre_lista):
        try:
            cancion = self.modelo.canciones[index_cancion]
        except IndexError:
            self.vista.mostrar_mensaje("❌ Índice de canción inválido.")
            return

        for lista in self.modelo.listas:
            if lista.nombre == nombre_lista:
                if cancion in lista.canciones:
                    self.vista.mostrar_mensaje("⚠️ La canción ya está en la lista.")
                else:
                    lista.agregar_cancion(cancion)
                    self.modelo.guardar_datos()
                    self.vista.mostrar_mensaje(f"✅ Canción agregada a la lista '{nombre_lista}'.")
                return

        self.vista.mostrar_mensaje("❌ Lista no encontrada.")


    def obtener_canciones_de_lista(self, nombre_lista):
        for lista in self.modelo.listas:
            if lista.nombre == nombre_lista:
                return lista.canciones
        return []
