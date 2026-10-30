import yt_dlp
import os
import logging
from pathlib import Path
from app.model.Cancion import Cancion
from app.model.RutasAplicacion import obtener_directorio_datos
import re
import unicodedata


logger = logging.getLogger(__name__)


class GestorDescargas:
    def __init__(self):
        self.directorio = obtener_directorio_datos() / "audio"
        self.directorio.mkdir(parents=True, exist_ok=True)

    def limpiar_nombre(self, nombre):
        # Reemplazar caracteres inválidos y quitar tildes
        nombre = re.sub(r'[\\/*?:"<>|]', "_", nombre)
        nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('ascii')
        return nombre

    def descargar(self, url, navegador=None):
        logger.info(
            "Iniciando descarga de un solo video (sesión del navegador: %s).",
            navegador or "desactivada"
        )
        plantilla = str(self.directorio / "%(title)s.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': plantilla,
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        if navegador:
            ydl_opts['cookiesfrombrowser'] = (navegador, None, None, None)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info or info.get('_type') == 'playlist':
                raise ValueError("El enlace no produjo un video individual descargable.")

            titulo_original = info['title']
            titulo_limpio = self.limpiar_nombre(titulo_original)
            archivo_descargado = Path(ydl.prepare_filename(info)).with_suffix(".mp3")
            archivo_descargado = archivo_descargado.resolve()
            if not archivo_descargado.is_file():
                raise FileNotFoundError(
                    f"yt-dlp terminó sin generar el archivo MP3 esperado: {archivo_descargado}"
                )

            path = os.path.normpath(str(archivo_descargado))
            logger.info("La descarga y conversión a MP3 finalizaron correctamente.")
            return Cancion(
                titulo_limpio,
                info.get('uploader', 'Desconocido'),
                info.get('duration'),
                path
            )
