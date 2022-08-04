"""Play a midi file provided on the command line.

This depends on pygame and (probably?) FluidSynth
https://www.fluidsynth.org/

Author: Nathan Sprague
Version: 8/2022
"""

import sys
import time
import pygame

def play_file(filename):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.75)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(.1)


if __name__ == "__main__":
    play_file(sys.argv[1])
