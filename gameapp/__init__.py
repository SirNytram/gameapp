import os

# load pythonsta libraries
if os.name == 'posix': 
    import gameapp.kb
    from gameapp.rect import Rect, Point, Color
    from gameapp.ios_gameapp import GameApp, GameSection, GameImage, GameText, GameFont, GameAudio, GameTimer,  GameShapeRect, GameShapeCircle, GameShapeLine

#load pygame libraries
elif os.name == 'nt':
    import pygame
    import pygame.constants as kb
    from gameapp.rect import Rect, Point, Color
    from gameapp.win_gameapp import GameApp, GameSection, GameImage, GameText, GameFont, GameAudio, GameTimer, GameShapeRect, GameShapeCircle, GameShapeLine
