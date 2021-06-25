import pygame
# from typing import List
from gameapp import *

#from pygame import key

import json


class TopArrow():
    def __init__(self, direction, xposition):
        super().__init__() 
        self.direction = direction  #'left', right, up, down
        # self.isPressed = False
        self.xposition = xposition
        self.defaultImage = GameImage(self.direction + "_default.png", (self.xposition, 10))
        self.pressedImage = GameImage(self.direction + "_pressed.png", (self.xposition, 10))
        self.isPressed = False


    def render(self):
        if self.isPressed:
            self.pressedImage.render()
        else:
            self.defaultImage.render()
            
class NoteDerived(GameImage):
    def __init__(self):
        super().__init__("left_default.png", (75, 300))

    def move(self):
        self.position = (self.position[0], self.position[1] - 1)


class Note():
    def __init__(self):
        self.yposition = 300
        self.speed = 0.5
        self.arrow1image = GameImage("left_default.png")

    def render(self):
        self.arrow1image.render((20, self.yposition))
        
    def move(self):
        self.yposition -= (self.speed * 1)


class Song():
    def __init__(self):
        self.noteList = []

    def loadFile(self, fileName):
        # self.noteList.append(Note())
        pass
    

class FunkinApp(GameApp):
    # variable creation
    def __init__(self):
        super().__init__() 
        self.fps = 60
        self.toparrowLeft = None
        self.toparrowRight = None

        self.movingnote = None

        self.width = 800
        self.height = 600
        self.testfont =  None
        self.myText = None
        self.tickText = None
        self.numSecsText = None
        self.msText = None
        self.numSecs = 0
        self.numSecsTimerId = None
        self.newCarTimerId = None
        self.tick = 0
        self.ms = 0
        self.movingnote2 = None

    # game load
    def on_start(self):

        self.movingnote = Note()
        self.movingnote2 = NoteDerived()
        
        self.toparrowLeft = TopArrow('left', 10)
        self.toparrowRight = TopArrow('left', 100)

        self.testfont =  GameFont("Verdana", 20)
        self.myText = GameText(self.testfont)
        self.tickText = GameText(self.testfont)
        self.numSecsText = GameText(self.testfont)
        self.msText = GameText(self.testfont, '', (200,400) )


        f = open('tutorialfile.json') 
        songfile = json.load(f)
        print(songfile['song']['song'])
        for section in songfile['notes']:
            print(section['mustHitSection'])
            # print(section['mustHitSection'])
            for notes in section['sectionNotes']:
                print(notes)

        self.numSecsTimerId = self.addTimer(1000, True)
        self.newCarTimerId = self.addTimer(2000)


    # game logic
    def on_loop(self):
        if self.keysPressed[K_ESCAPE]:
            self.running = False

        if self.keysPressed[K_r]:
            self.movingnote.yposition = 300
            
        # if self.keysPressed[K_f]:
        #     pygame.display.toggle_fullscreen()

        self.movingnote.move()
        self.movingnote2.move()

        self.tick += 1

    # game display
    def on_render(self):
        #display background
        self.surface.fill((255, 255, 255))
        
        # display arrows
        self.toparrowLeft.render()
        self.toparrowRight.render()
        
        self.movingnote.render()
        self.movingnote2.render()

        #diplay some text
        self.myText.text = 'fps:' + str(self.clock.get_fps())
        self.myText.render((500,500))

        # self.numSecsText.text = str(self.numSecs)
        # self.numSecsText.render((400,500))
        self.numSecsText.renderText(str(self.numSecs), (400,500))

        self.tickText.renderText('tick:' + str(self.tick), (200,450))
        self.ms += self.clock.get_time()
        self.msText.renderText('ms:' + str(self.clock.get_time()))
        

    def on_event(self, eventId):
        if eventId == self.numSecsTimerId:
            self.numSecs += 1
            self.movingnote.arrow1image.rotate(45)
        

    def on_key(self, isDown, key, mod):
        
        if key == K_f and isDown:
            pygame.display.toggle_fullscreen()


        if key == K_LEFT:
            if isDown:
                self.toparrowLeft.isPressed = True
            else:
                self.toparrowLeft.isPressed = False

        if key == K_RIGHT:
            if isDown:
                self.toparrowRight.isPressed = True
            else:
                self.toparrowRight.isPressed = False
           


if __name__ == "__main__" :
    FunkinApp().start()
