import pygame

SOUNDS_DIR = 'sounds/'

SOUNDS = {
    "bark": "dog-barking.mp3",
    "water": "water-splashing.mp3",
    "insect": "cricket-chirping.mp3",
    "birds": "birds-singing.mp3",
}


def play_sound(sound_type: str):
    pygame.mixer.init()
    pygame.mixer.music.load(SOUNDS_DIR + SOUNDS[sound_type])
    pygame.mixer.music.play()
