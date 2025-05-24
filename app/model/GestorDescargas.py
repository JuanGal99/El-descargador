import yt_dlp
import os
from app.model.Cancion import Cancion
import re

class GestorDescargas:
    def __init__(self):
        self.directorio = "audio"
        os.makedirs(self.directorio, exist_ok=True)

    def limpiar_nombre(self, nombre):
        nombre_limpio = re.sub(r'[\\/*?:"<>|]', "_", nombre)
        return nombre_limpio

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
        