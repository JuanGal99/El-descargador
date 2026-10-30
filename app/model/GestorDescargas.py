import yt_dlp
import os
from pathlib import Path
from app.model.Cancion import Cancion
import re
import unicodedata

class GestorDescargas:
    def __init__(self):
        self.directorio = Path(__file__).resolve().parents[2] / "audio"
        self.directorio.mkdir(parents=True, exist_ok=True)

    def limpiar_nombre(self, nombre):
        # Reemplazar caracteres inválidos y quitar tildes
        nombre = re.sub(r'[\\/*?:"<>|]', "_", nombre)
        nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('ascii')
        return nombre

    def descargar(self, url):
        plantilla = str(self.directorio / "%(title)s.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': plantilla,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo_original = info['title']
            titulo_limpio = self.limpiar_nombre(titulo_original)
            archivo_descargado = Path(ydl.prepare_filename(info)).with_suffix(".mp3")
            path = os.path.normpath(str(archivo_descargado.resolve()))
            return Cancion(titulo_limpio, info.get('uploader', 'Desconocido'), info['duration'], path)
