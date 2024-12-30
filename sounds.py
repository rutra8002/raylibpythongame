import raylib
import pyray

soundes = {}

def load_sounds():
    raylib.InitAudioDevice()
    soundes["music"] =  pyray.load_music_stream("sounds/testmusic.wav")
    soundes["music"].looping = True