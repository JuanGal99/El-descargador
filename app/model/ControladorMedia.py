import vlc

class ControladorMedia:
    def __init__(self):
        self.player = vlc.MediaPlayer()

    def play(self, path):
        self.player.set_media(vlc.Media(path))

    def pausar(self):
        self.player.pause()

    def detener(self):
        self.player.stop()