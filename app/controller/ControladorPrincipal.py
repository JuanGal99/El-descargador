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
        except Exception as e:
            self.vista.encolar_resultado_descarga(None, f"❌ Error al descargar: {str(e)}")
            return

        self.vista.encolar_resultado_descarga(nueva, None)

    def registrar_descarga(self, nueva):
        if any(
            nueva.titulo == existente.titulo and nueva.artista == existente.artista
            for existente in self.modelo.canciones
        ):
            self.vista.finalizar_descarga(None, "⚠️ La canción ya está en la biblioteca.")
            return

        try:
            self.modelo.agregar_cancion(nueva)
            self.vista.finalizar_descarga(nueva, "✅ Canción descargada correctamente.")
        except (OSError, TypeError, ValueError) as e:
            if nueva in self.modelo.canciones:
                self.modelo.canciones.remove(nueva)
            self.vista.finalizar_descarga(None, f"❌ No se pudo guardar la canción: {str(e)}")


    def reproducir_cancion(self, cancion):
        self.media.play(cancion.pathArchivo)

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


    def marcar_favorita(self, cancion):
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
        except Exception as e:
            self.vista.mostrar_mensaje(f"❌ No se pudo eliminar la canción: {str(e)}")

    def editar_cancion(self, cancion, nuevo_titulo, nuevo_artista):
        cancion.titulo = nuevo_titulo
        cancion.artista = nuevo_artista
        self.modelo.guardar_datos()

    def crear_lista(self, nombre):
        try:
            self.modelo.crear_lista(nombre)
            self.vista.mostrar_mensaje(f"✅ Lista '{nombre}' creada.")
            return True
        except ValueError as e:
            self.vista.mostrar_mensaje(str(e))
            return False

    def obtener_nombres_listas(self):
        return [lista.nombre for lista in self.modelo.listas]

    def agregar_cancion_a_lista(self, cancion, nombre_lista):
        for lista in self.modelo.listas:
            if lista.nombre == nombre_lista:
                if cancion in lista.canciones:
                    self.vista.mostrar_mensaje("⚠️ La canción ya está en la lista.")
                    return False
                else:
                    lista.agregar_cancion(cancion)
                    self.modelo.guardar_datos()
                    self.vista.mostrar_mensaje(f"✅ Canción agregada a la lista '{nombre_lista}'.")
                    return True

        self.vista.mostrar_mensaje("❌ Lista no encontrada.")
        return False


    def obtener_canciones_de_lista(self, nombre_lista):
        for lista in self.modelo.listas:
            if lista.nombre == nombre_lista:
                return lista.canciones
        return []

    def eliminar_lista(self, nombre_lista):
        self.modelo.eliminar_lista(nombre_lista)
        self.vista.mostrar_mensaje(f"🗑 Lista '{nombre_lista}' eliminada.")

    def eliminar_cancion_de_lista(self, nombre_lista, cancion):
        self.modelo.eliminar_cancion_de_lista(nombre_lista, cancion)
        self.vista.mostrar_mensaje(f"🗑 Canción eliminada de la lista '{nombre_lista}'.")

    def ordenar_por(self, criterio):
        self.modelo.ordenar_biblioteca(criterio)
        self.vista.mostrar_todas()
