import yt_dlp
import os
from model.Cancion import Cancion

class GestorDescargas:
    def __init__(self):
        self.directorio = "audio"
        os.makedirs(self.directorio, exist_ok=True)

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
            path = os.path.abspath(f"{self.directorio}/{info['title']}.mp3")
            return Cancion(info['title'], info.get('uploader', 'Desconocido'), info['duration'], path)
        