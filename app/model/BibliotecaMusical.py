from app.model.ListaReproduccion import ListaReproduccion
import json
import os
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
            for lista in self.listas:
                lista.eliminar(cancion)
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
            'canciones': [{
                'titulo': c.titulo,
                'artista': c.artista,
                'duracion': c.duracion,
                'pathArchivo': c.pathArchivo,
                'favorito': c.favorito
            } for c in self.canciones],
            'listas': [{
                'nombre': lista.nombre,
                'canciones': [{
                    'titulo': c.titulo,
                    'artista': c.artista
                } for c in lista.canciones]
            } for lista in self.listas]
        }

        with open(self.archivo_datos, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

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

                # Cargar canciones
                self.canciones = [
                    Cancion(c['titulo'], c['artista'], c['duracion'], c['pathArchivo'])
                    for c in data.get('canciones', [])
                ]
                for c, original in zip(self.canciones, data.get('canciones', [])):
                    c.favorito = original.get('favorito', False)

                # Diccionario para buscar canciones rápido
                cancion_dict = {(c.titulo, c.artista): c for c in self.canciones}

                # Cargar listas
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