import sys
import pygame
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = {
    "packages": ["sys", "os", "pygame", "codecs", "random"],
    "includes": ["missile_command", "end_screen", "level"],
    "include_files": ["art/", "fonts/", "score_files/", "sounds/"],
    "excludes": ["Tcl", "Tkinter", "numpy"]
}

base = None
if sys.platform == "win32":
    base = 'Win32GUI'

executables = [
    Executable('start_screen.py', base=base, targetName='Missile Command 20XX')
]

setup(name='MissileCommand20XX',
      version = '1.0',
      description = 'A more modern take on the Atari game, Missile Command.',
      options = {"build_exe": buildOptions},
      executables = executables)
