import vlc
import pathlib
import os

class ControladorMedia:
    def __init__(self):
        self.player = vlc.MediaPlayer()

    def play(self, path):
        path = os.path.normpath(path)
        if os.path.isfile(path):
            print(f"🎵 Reproduciendo: {path}")
            self.player.set_media(vlc.Media(pathlib.Path(path).as_uri()))
            self.player.play()
        else:
            print(f"❌ Archivo no encontrado para reproducir: {path}")

    def pausar(self):
        self.player.pause()

    def detener(self):
        self.player.stop()