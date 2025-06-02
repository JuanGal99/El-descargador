from app.model.ListaReproduccion import ListaReproduccion
import json
import os
import unicodedata
from app.model.Cancion import Cancion

class BibliotecaMusical:
    def __init__(self):
        self.canciones = []
        self.listas = []
        self.archivo_datos = "biblioteca.json"
        self.cargar_datos()

    def agregar_cancion(self, cancion):
        if cancion in self.canciones:
            raise ValueError("La canción ya está en la biblioteca.")
        self.canciones.append(cancion)
        self.guardar_datos()

    def eliminar_cancion(self, cancion):
        if cancion in self.canciones:
            self.canciones.remove(cancion)

            # Eliminar de listas
            for lista in self.listas:
                lista.eliminar(cancion)

            # Intentar eliminar el archivo físico
            try:
                real_path = os.path.normpath(cancion.pathArchivo)
                real_path = os.path.abspath(real_path)
                if os.path.isfile(real_path):
                    os.remove(real_path)
                    print(f"🗑 Archivo eliminado: {real_path}")
                else:
                    print(f"⚠️ Archivo no encontrado: {real_path}")
            except Exception as e:
                print(f"❌ Error al eliminar archivo: {e}")

            self.guardar_datos()

    def crear_lista(self, nombre):
        if any(lista.nombre == nombre for lista in self.listas):
            raise ValueError("Ya existe una lista con ese nombre.")
        nueva = ListaReproduccion(nombre)
        self.listas.append(nueva)
        self.guardar_datos()

    def agregar_a_lista(self, nombre_lista, cancion):
        for lista in self.listas:
            if lista.nombre == nombre_lista:
                lista.agregar(cancion)
                self.guardar_datos()
                return
        raise ValueError("Lista no encontrada.")

    def obtener_listas(self):
        return self.listas

    def buscar(self, texto):
        return [c for c in self.canciones if texto.lower() in c.titulo.lower()]

    def obtener_favoritas(self):
        return [c for c in self.canciones if c.favorito]

    def guardar_datos(self):
        data = {
            'canciones': [self._serializar_cancion(c) for c in self.canciones],
            'listas': [{
                'nombre': lista.nombre,
                'canciones': [{'titulo': c.titulo, 'artista': c.artista} for c in lista.canciones]
            } for lista in self.listas]
        }

        with open(self.archivo_datos, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _serializar_cancion(self, c):
        return {
            'titulo': c.titulo,
            'artista': c.artista,
            'duracion': c.duracion,
            'pathArchivo': os.path.normpath(c.pathArchivo),
            'favorito': c.favorito
        }

    def cargar_datos(self):
        if not os.path.exists(self.archivo_datos):
            print("📁 No se encontró el archivo de datos, se creará uno nuevo.")
            return

        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return
                data = json.loads(contenido)
                if not isinstance(data, dict):
                    print("⚠️ El archivo de datos no tiene el formato esperado. Se ignorará.")
                    return

                self.canciones = [
                    Cancion(c['titulo'], c['artista'], c['duracion'], os.path.normpath(c['pathArchivo']))
                    for c in data.get('canciones', [])
                ]
                for c, original in zip(self.canciones, data.get('canciones', [])):
                    c.favorito = original.get('favorito', False)

                cancion_dict = {(c.titulo, c.artista): c for c in self.canciones}

                self.listas = []
                for lista_data in data.get('listas', []):
                    lista = ListaReproduccion(lista_data['nombre'])
                    for c in lista_data['canciones']:
                        key = (c['titulo'], c['artista'])
                        if key in cancion_dict:
                            lista.agregar(cancion_dict[key])
                    self.listas.append(lista)

        except json.JSONDecodeError:
            print("⚠️ Archivo JSON corrupto, se ignorará.")

    def eliminar_lista(self, nombre_lista):
        self.listas = [l for l in self.listas if l.nombre != nombre_lista]
        self.guardar_datos()

    def eliminar_cancion_de_lista(self, nombre_lista, cancion):
        for lista in self.listas:
            if lista.nombre == nombre_lista:
                lista.eliminar(cancion)
                self.guardar_datos()
                return

    def ordenar_biblioteca(self, criterio):
        if self.canciones and hasattr(self.canciones[0], criterio):
            self.canciones.sort(key=lambda c: getattr(c, criterio))
