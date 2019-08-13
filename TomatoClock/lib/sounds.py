import os

_SOUND_DIR = os.path.join(
    os.path.split(os.path.dirname(__file__))[0],
    "sounds"
)

try:
    _SOUND_DIR = str(_SOUND_DIR)
except UnicodeError:
    _SOUND_DIR = str(_SOUND_DIR, 'gbk')

BREAK = os.path.join(_SOUND_DIR, "break.mp3")
ABORT = os.path.join(_SOUND_DIR, "abort.mp3")
START = os.path.join(_SOUND_DIR, "page.mp3")
TIMEOUT = os.path.join(_SOUND_DIR, "TIMEOUT.mp3")
HALF_TIME = os.path.join(_SOUND_DIR, "half_time.wav")
