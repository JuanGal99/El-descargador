import yt_dlp
import os
from app.model.Cancion import Cancion
import re
import unicodedata

class GestorDescargas:
    def __init__(self):
        self.directorio = "audio"
        os.makedirs(self.directorio, exist_ok=True)

    def limpiar_nombre(self, nombre):
        nombre = re.sub(r'[\\/*?:"<>|]', "_", nombre)
        nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('ascii')
        return nombre

    def descargar(self, url):
        plantilla = os.path.join(self.directorio, "%(title)s.%(ext)s")
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
            titulo_original= info['title']
            titulo_limpio = self.limpiar_nombre(titulo_original)
            archivo_mp3 = f"{titulo_limpio}.mp3"
            path = os.path.abspath(os.path.join(self.directorio, archivo_mp3))
            return Cancion(titulo_limpio, info.get('uploader', 'Desconocido'), info['duration'], path)
        