from app.model.ListaReproduccion import ListaReproduccion
import json
import os
from pathlib import Path
from app.model.Cancion import Cancion

class BibliotecaMusical:
    def __init__(self):
        self.canciones = []
        self.listas = []
        self.directorio_base = Path(__file__).resolve().parents[2]
        self.directorio_audio = self.directorio_base / "audio"
        self.archivo_datos = self.directorio_base / "biblioteca.json"
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

            # Only remove files managed by this application.
            try:
                real_path = Path(cancion.pathArchivo).resolve()
                real_path.relative_to(self.directorio_audio.resolve())
                if real_path.is_file():
                    real_path.unlink()
                    print(f"🗑 Archivo eliminado: {real_path}")
                else:
                    print(f"⚠️ Archivo no encontrado: {real_path}")
            except (OSError, ValueError) as e:
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
        texto = texto.casefold()
        return [
            c for c in self.canciones
            if texto in c.titulo.casefold() or texto in c.artista.casefold()
        ]

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
        path = Path(c.pathArchivo).resolve()
        try:
            path_guardado = path.relative_to(self.directorio_base).as_posix()
        except ValueError:
            path_guardado = str(path)

        return {
            'titulo': c.titulo,
            'artista': c.artista,
            'duracion': c.duracion,
            'pathArchivo': path_guardado,
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

                canciones_data = data.get('canciones', [])
                if not isinstance(canciones_data, list):
                    raise ValueError("'canciones' debe ser una lista.")

                self.canciones = []
                for original in canciones_data:
                    path = Path(original['pathArchivo'])
                    if not path.is_absolute():
                        path = self.directorio_base / path
                    if not path.is_file():
                        ruta_local = self.directorio_audio / Path(original['pathArchivo']).name
                        if ruta_local.is_file():
                            path = ruta_local

                    cancion = Cancion(
                        original['titulo'],
                        original['artista'],
                        original['duracion'],
                        os.path.normpath(str(path))
                    )
                    cancion.favorito = original.get('favorito', False)
                    self.canciones.append(cancion)

                cancion_dict = {(c.titulo, c.artista): c for c in self.canciones}

                self.listas = []
                for lista_data in data.get('listas', []):
                    lista = ListaReproduccion(lista_data['nombre'])
                    for c in lista_data['canciones']:
                        key = (c['titulo'], c['artista'])
                        if key in cancion_dict:
                            lista.agregar(cancion_dict[key])
                    self.listas.append(lista)

        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as e:
            print(f"⚠️ No se pudieron cargar los datos de la biblioteca: {e}")

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
