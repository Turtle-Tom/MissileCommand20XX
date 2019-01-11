import pygame
import time

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

musicChannel = pygame.mixer.Channel(1)
effects = pygame.mixer.Channel(2)
# pygame.mixer.music.load('sounds/single_trim2.ogg')
# pygame.mixer.music.play(-1)
music = pygame.mixer.Sound("sounds/single_trim2.ogg")
ex = pygame.mixer.Sound("sounds/explosion.ogg")
musicChannel.play(music, loops=-1)
effects.play(ex, loops=3)
time.sleep(1000)
