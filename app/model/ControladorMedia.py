import vlc
import pathlib
import os
import logging


logger = logging.getLogger(__name__)

class ControladorMedia:
    def __init__(self):
        self.player = vlc.MediaPlayer()

    def play(self, path):
        path = os.path.normpath(path)
        if os.path.isfile(path):
            logger.info("Reproduciendo: %s", path)
            self.player.set_media(vlc.Media(pathlib.Path(path).as_uri()))
            self.player.play()
        else:
            logger.error("Archivo no encontrado para reproducir: %s", path)

    def pausar(self):
        self.player.pause()

    def detener(self):
        self.player.stop()