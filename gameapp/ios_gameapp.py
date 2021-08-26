# type: ignore
import os, time
from gameapp.rect import Rect, Point, Color
import gameapp.kb as kb
import platform
import math
from typing import List, Dict, Tuple

if os.name == 'nt':
    from gameapp.win_pythonista import run, Scene, SpriteNode, LabelNode, ShapeNode, Path
    import gameapp.win_pythonista as sound
else:
     from scene import run, Scene, SpriteNode, LabelNode, ShapeNode
     from ui import Path
     import sound
    
gblScale = 1
renderImages = []
gblAnchorPoint = (0.,0.)



class GameImage():
    def __init__(self, source = None, position = (0,0), *, anchor_point = None, rotation:float = 0.0, scale:float = 1.0, show_rect:bool=False):
    # def __init__(self, parent, fileName = None, *, position = (0,0), anchor_point = (0,0), rotation = 0.0, scale = 1.0):
        if anchor_point == None:
            anchor_point = gblAnchorPoint

        if source:
           source = source.replace('\\', '/')
        self._image = SpriteNode(None)
        self.anchor_point = Point(anchor_point[0],anchor_point[1])
        self.rotation = rotation
        self.scale = scale
        self._position = Point(position[0], position[1])
        self._position._changed = True
        self._rect = Rect(0, 0, 1, 1)
        self.show_rect = show_rect
        
        self.load(source)


    ###################### 
    @property
    def rect(self)->Rect:
        if self._position._changed:
            self._rect._left = self._position._left - (self._rect._width * self.anchor_point.left)
            self._rect._top = self._position._top - (self._rect._height * self.anchor_point.top)
            self._position._changed = False

        return self._rect

    @rect.setter
    def rect(self, value:Rect):
        self._rect = Rect(value._left, value._top, value._width, value._height)
        self._position._left = self._rect._left + (self._rect._width * self.anchor_point.left)
        self._position._top = self._rect._top + (self._rect._height * self.anchor_point.top)
        self._position._changed = False

    @property
    def position(self)->Point:
        if self._rect._changed:
            self._position._left = self._rect._left + (self._rect._width * self.anchor_point.left)
            self._position._top = self._rect._top + (self._rect._height * self.anchor_point.top)
            self._rect._changed = False

        return self._position

    @position.setter
    def position(self, value):
        if type(value) != Point:
            value = Point(value[0], value[1])
            
        self._position = Point(value._left, value._top)
        self._rect._left = self._position._left - (self._rect._width * self.anchor_point[0])
        self._rect._top = self._position._top - (self._rect._height * self.anchor_point[1])
        self._rect._changed = False


    ###################### 


    def load(self, source):
        if source:
            if type(source) == str:
                self._image = self._image = SpriteNode(source)
            elif type(source) == GameImage:
                self._image = source._image

        
            # global gblScale
            # global renderImages  
        self._image.anchor_point = self.anchor_point
        self.update_rect(self._image)        

    def update_rect(self, img):
        size = img.size
        self._rect._left = self._position._left-(size[0]*self.anchor_point[0])
        self._rect._top = self._position._top-(size[1]*self.anchor_point[1])
        self._rect._width = size[0]
        self._rect._height = size[1]            

    def render(self, position = None):
        global gblScale
        self._image.scale = self.scale * gblScale
       # print('render')

        if position:
            self.position = Point(position[0], position[1])

        # if position:
        #     if type(position) == Point:
        #         self.position = Point(position.x, position.y)
        #     else:
        #         self.position.moveTo(position[0], position[1])

        #screen_height = screen_size[1] 
        global gblScene
        screen_height = gblScene.size[1] 
        self._image.position = (self.position.x * gblScale, screen_height - (self.position.y * gblScale)  - (self._image.size[1] * self._image.scale))
        self._image.rotation = self.rotation

        #TODO
        # if self.show_rect:
        #     pygame.draw.rect(pygame.display.get_surface(), (0,255,0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), 1)


        global renderImages
      #  print(f'renderIm {renderImages}')
        renderImages.append(self)
       
    def rotate(self, angle:float=0.0, in_place = False):
        #TODO Action.rotate_by
        pass

    def resize(self, width:float, height:float, in_place:bool = False):
        #TODO Action.scale_by
        pass

    def flip(self, vertical:bool=False, horizontal:bool=False, in_place:bool = False):
        #TODO
        pass

    def rotate_scale(self, angle:float=0, scale:float=1.0, in_place:bool = False):
    # def rotoZoom(self, angle=0, scale=0):
        pass
        # self.image = pygame.transform.rotozoom(self.image, angle, scale)

    def move_angle(self, dist:float, angle:float):
    # def moveAngle(self, dist, angle):
        ang = math.radians(angle)
        dx = dist * math.cos(ang)
        dy = dist * math.sin(ang)

        self.position.x += dx
        self.position.y -= dy

    def move_to(self, dist:float, point):
    # def moveTo(self, dist, position):
        ang = self.get_angle_towards(point)
        self.move_angle(dist, ang)

    def move_around(self, angle:float, point):
        pass


    def get_angle_towards(self, point)->float:
        dx = (point[0] - self.position.x)
        dy = -(point[1] - self.position.y)
        ang = 0
        if dx != 0:
            ang = math.degrees(math.atan(dy/dx))

        if dx < 0:
            ang += 180

        return ang

    def set_pixel(self, point, color):
        pass

    def copy(self):
        pass

class GameShapeRect(GameImage):
    def __init__(self, rect = (0,0,0,0), color = (0,0,0), line_width:int = 1, corner_radius:int = 0):
        super().__init__()
        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        if type(rect) in (tuple, list):
            rect = Rect(rect[0], rect[1], rect[2], rect[3])

        self.rect = rect

        self.line_width = line_width
        self.corder_radius = corner_radius
        #   pygame.Surface((self.rect.width, self.rect.height))
        if self.corder_radius ==  0:
            path = Path().rect(0,0, self.rect.width, self.rect.height)
        else:
            path = Path().rounded_rect(0,0, self.rect.width, self.rect.height, self.corder_radius)
        path.line_width = self.line_width
        self._image =  ShapeNode(path)


    def render(self):
        if self.rect.size != self._image.get_size():
            path = Path().rect(0,0, self.rect.width, self.rect.height)
            path.line_width = self.line_width
            self._image =  ShapeNode(path)
            # self._image = pygame.Surface((self.rect.width, self.rect.height))
            self.update_rect(self._image)

        # pygame.draw.rect(pygame.display.get_surface(), self.color.rgb, pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), self.line_width, self.corder_radius)
        global renderImages
        renderImages.append(self)


class GameShapeCircle(GameImage):
    def __init__(self, center = (0,0), radius = 0, color = (0,0,0), line_width:int = 1):
        super().__init__(position=center)
        self.radius = radius
        self.line_width = line_width

        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        # self._image = pygame.Surface((self.radius * 2, self.radius * 2))
        path = Path().oval(0,0, self.radius * 2, self.radius * 2)
        path.line_width = self.line_width
        self._image =  ShapeNode(path)
        self.update_rect(self._image)


    def render(self):
        if self.rect.size != (self.radius * 2, self.radius * 2):
            path = Path().oval(0,0, self.radius * 2, self.radius * 2)
            path.line_width = self.line_width
            self._image =  ShapeNode(path)
            self.update_rect(self._image)

        # pygame.draw.circle(pygame.display.get_surface(), pygame.Color(self.color.r, self.color.g, self.color.b), (self.position[0], self.position[1]), self.radius, self.line_width)
        self._image.position = (self.position.x, gblScene.size[1] - self.position.y)
        

        global renderImages
        renderImages.append(self)



class GameShapeLine(GameImage):
    def __init__(self, first_point = (0,0), last_point = (0,0), color = (0,0,0), line_width:int = 1):
        super().__init__()
        self.first_point = Point(first_point[0], first_point[1])
        self.last_point = Point(last_point[0], last_point[1])
        self.line_width = line_width

        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        # self._image = pygame.Surface((self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x))
        path = Path()
        path.move_to(self.first_point.x, self.first_point.y)
        path.line_to(self.last_point.x, self.last_point.y)
        path.line_width = self.line_width
        self._image =  ShapeNode(path)
        self.update_rect(self._image)


    def render(self):
        if self.rect.size != (self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x):
            # self._image = pygame.Surface((self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x))
            path = Path()
            path.move_to(self.first_point.x, self.first_point.y)
            path.line_to(self.last_point.x, self.last_point.y)
            path.line_width = self.line_width
            self._image =  ShapeNode(path)
            self.update_rect(self._image)
        # pygame.draw.line(pygame.display.get_surface(), pygame.Color(self.color.r, self.color.g, self.color.b), self.first_point.point, self.last_point.point, self.line_width)
        self._image.position = self.first_point.point

        global renderImages
        renderImages.append(self)
    

class GameFont():
    def __init__(self, name = 'Helvetica', size = 20, isSys = True):
        self.name = name
        self.size = size
        self.font = None
        self.isSys = isSys


class GameText(GameImage):
    def __init__(self, text = '', position = (0,0), color = (0,0,0), font = GameFont(), anchor_point = None):
        super().__init__(position=position, anchor_point=anchor_point)
    # def __init__(self, parent, font, text = '', position = (0,0), RGB = (0,0,0)):
        self.font = font
        self.text = text

        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        if not self._image:
            self._image = LabelNode(self.text, font = (self.font.name, self.font.size*gblScale), position=(0,0))
            #self.image.color =  RGB
            self._image.color = (self.color.r/255, self.color.g/255, self.color.b/255)
            self._image.anchor_point = self.anchor_point

    @property
    def text(self)->str:
        return self._text

    @text.setter
    def text(self, value:str):
        self._text = value
        # self.font.load()

        self._image = LabelNode(self.text, font = (self.font.name, self.font.size*gblScale), position=(0,0))
        #self.image.color =  RGB
        self._image.color = (self.color.r/255, self.color.g/255, self.color.b/255)

        # self._image = self.font.font.render(self._text, True, pygame.Color(self.color.r,self.color.g, self.color.b))
        self.update_rect(self._image)

    def render_text(self, text, position = None):
        self.text = str(text)
        self.render(position)

    def render(self, position = None):
        if position:
            # if type(position) == Rect:
            #     self.position = position.copy()
            # else:
                self.position = Point(position[0], position[1])

        global gblScene
        self._image.position = (self.position.x * gblScale, gblScene.size[1] - (self.position.y * gblScale)  - (self._image.size[1]))
        self._image.text = str(self.text)
        #self.image.color = 'black'
        global renderImages
        renderImages.append(self)


class VirtualKey():
    def __init__(self, parent, label, key, colrow):
        self.parent = parent
        self.label = label
        self.key = key
        self.diameter = 50
        self.spacing = 5
        self.distance = (self.diameter) + (self.spacing)     
        self.colrow = colrow  

        global gblScale


        xpos = self.diameter + self.spacing
        global gblScene
        ypos  = gblScene.size[1] - (self.distance * 3) + self.spacing
        
        self.position = Rect(xpos + (colrow[0]*self.distance), ypos + (colrow[1]*self.distance), 0, 0)

        self.circle =  ShapeNode(Path().oval(0,0, self.diameter, self.diameter))
        self.circle.position = (self.position.x, gblScene.size[1] - self.position.y)
        

        self.text = GameText(self, GameFont(self, size=10), label)
        
        self.text._image.anchor_point = (0.5,0)

  

    def setPos(self):
        global  gblScale

        xpos = self.diameter + self.spacing
        global gblScene
        ypos  = gblScene.size[1] - (self.distance * 3) + self.spacing
        
        self.position = Point(xpos + (self.colrow[0]*self.distance), ypos + (self.colrow[1]*self.distance))

        self.circle =  ShapeNode(Path().oval(0,0, self.diameter, self.diameter))
        self.circle.position = (self.position.x, gblScene.size[1] - self.position.y)
        
            
        self.text.position.x = self.position.x/gblScale
        self.text.position.y = (self.position.y-self.spacing)/gblScale       

        
class MyScene(Scene):
    def __init__(self, gameapp):
        super().__init__()
        self.gameapp:GameApp = gameapp

    def setup(self):
        self.isShift = False

    def update(self):
        for timer in self.gameapp.timers.values():
            if timer.active and self.gameapp._milliseconds_since_start > timer.getNextRunMS():
                timer.numLoopsPerformed += 1
                self.gameapp.on_timer(timer.name)
                #check if last loop
                #if not infinite timer
                if timer.numRepeats >= 0 and timer.numLoopsPerformed > timer.numRepeats:
                    timer.active = False



        curTime = time.time() * 1000
        self.gameapp._milliseconds_since_last_frame = curTime - self.gameapp._milliseconds_since_start
        self.gameapp._milliseconds_since_start =  curTime
        global renderImages
      #  print(f'render im sc {renderImages}')

        for image in renderImages:
            image.image.remove_from_parent()
        for vk in self.gameapp.virtualKeys:
            vk.text.image.remove_from_parent()   
            vk.circle.remove_from_parent()     
            
            

        renderImages.clear()
        self.gameapp.on_render()
        for image in renderImages:
            self.add_child(image._image)
            
        for vk in self.gameapp.virtualKeys:
            vk.setPos()
            vk.text.render()
            self.add_child(vk.circle)
            self.add_child(vk.text.image)
            
        self.gameapp.on_after_render()
        self.gameapp.on_loop()

    def process_touch(self, touch, isDown):
        #print(f'touch  {touch.location} {isDown}')
        
        pos = touch.location
        for vk in self.gameapp.virtualKeys:
            vk: VirtualKey 
            if (pos[0] > vk.circle.position.x - vk.diameter/2) and (pos[0] < vk.circle.position.x + vk.diameter/2) and \
               (pos[1] > vk.circle.position.y - vk.diameter/2) and (pos[1] < vk.circle.position.y + vk.diameter/2):
                self.gameapp.on_key(isDown, vk.key, None)

       
    def touch_began(self, touch):
        self.process_touch(touch, True)

    def touch_ended(self, touch):
        self.process_touch(touch, False)
        
    def did_change_size(self):
        global gblScale
        gblScale = min(self.size[0] / self.gameapp.width, self.size[1] / self.gameapp.height)        


gblScene = MyScene(None)


class GameAudio():
    def __init__(self, fileName = None, volume = 1):
        self.effect = None
        self.fileName = None
        self.played = False
        
    def play(self, loop = 0):
    
        print(f'playing {self.fileName}')
        self.effect = sound.play_effect(self.fileName)
       
    def load(self, fileName):
        print(f'loading {fileName}')
        if self.effect:
            self.effect.stop()
        if fileName:

            fileName = str(f'{fileName}.caf').replace('\\', '/')
            self.fileName = fileName
        

    def unload(self):
        if self.effect:
           self.effect.stop()
    def pause(self):
        pass
    def unpause(self):
        pass
    def stop(self):
        if self.effect:
           self.effect.stop()

    def set_volume(self, volume = 1):
        self.effect.volume = volume


class GameTimer():
    def __init__(self, parent, name:str, id:int, milliseconds:float, numRepeats:int, delayMS:float=0.0):
        self.active: bool = True
        self.parent = parent
        self.name:str = name
        self.id:int = id
        self.milliseconds:float = milliseconds
        self.numRepeats:int = numRepeats
        self.msAtStart:float = 0.0
        self.numLoopsPerformed:int = 0
        self.delayMS:float = delayMS

    def getNextRunMS(self):
        return self.msAtStart + self.delayMS + ((self.numLoopsPerformed + 1) * self.milliseconds)

class GameSection:
    def __init__(self, gameapp, active:bool = False):
        self.gameapp:GameApp = gameapp
        self.active = active

    def on_start(self):
        pass

    def on_event(self, event_id):
        pass
    
    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_after_render(self):
        pass

    def on_key(self, is_down, key, mod):
        pass

    def on_mouse(self, is_down, key, position = Point()):
        pass

    def on_timer(self, timer: GameTimer):
        pass
        

class GameApp():
    def __init__(self, *, width=640, height=480, display_number = 0, full_screen = False, scale = 1.0, has_vk = False, fps = 60):
    # def __init__(self, width=640, height=480, displayNumber=0):
        self.has_vk = has_vk
        self.platform = 'ios'
        self.is_running = True
        self._surface = None
        self.rect = Rect(0,0, width, height)
        self._fps = fps
        self.pressed_keys = []
        self._cur_userevent_id = kb.USEREVENT 

        self._milliseconds_since_start =  time.time() * 1000
        self._milliseconds_since_last_frame = 0.0

        self.sections: Dict[str, GameSection] = {}
        self.virtual_keys: List[VirtualKey] = []
        self.timers: Dict[str, GameTimer] = {}
        self.mouse_position = Point()

        self.scene = MyScene(self)
        self.scene.gameapp = self
        global gblScale
        self.rect = Rect(0,0, width, height)

        # if os.name == 'nt':
        #     gblScale = 4.0

        # if platform.machine()[:6] == 'iPhone':
        gblScale = min(self.scene.size[0] / 240, self.scene.size[1] / 135)        
        
        self.isRunning = True
        self.curUserEventId = kb.USEREVENT 

 
    def get_MS(self):
        return self._milliseconds_since_start

    def get_lastframe_MS(self):
        return self._milliseconds_since_last_frame         

    # def on_start(self):
    #     pass
    
    # def on_event(self, eventId):
    #     pass
        
    # def on_loop(self):
    #     if self.currentSectionName:
    #         self.sections[self.currentSectionName].on_loop()
    # def on_render(self):
    #     if self.currentSectionName:
    #         self.sections[self.currentSectionName].on_render()

    # def on_after_render(self):
    #     if self.currentSectionName:
    #         self.sections[self.currentSectionName].on_after_render()

    # def on_key(self, isDown, key, mod):
    #     if self.currentSectionName:
    #         self.sections[self.currentSectionName].on_key(isDown, key, mod)
    # def on_mouse(self, isDown, key, xcoord, ycoord):
    #     if self.currentSectionName:    
    #         self.sections[self.currentSectionName].on_mouse(isDown, key, xcoord, ycoord)

    # def on_timer(self, name):
    #     if self.currentSectionName:    
    #         self.sections[self.currentSectionName].on_timer(name)

    def add_timer(self, name, milliseconds:float, num_repeats:int=-1, delay_MS:float=0.0):
        if name not in self.timers.keys():
            self._cur_userevent_id += 1
            timer = GameTimer(name, self._cur_userevent_id, milliseconds, num_repeats, delay_MS)
            timer.ms_at_start = self.get_MS()
            self.timers[name]  = timer
        else:
            timer = self.timers[name]
            timer.ms_at_start = self.get_MS()
            timer.milliseconds = milliseconds
            timer.num_repeats = num_repeats
            timer.num_loops_performed = 0
            timer.active = True

    def stop_timer(self, name):
        if name in self.timers.keys():
            self.timers[name].active = False

    def add_section(self, name: str, section: GameSection):
        section.on_start()
        self.sections[name] = section

    def start(self):
        
        global gblScene
        gblScene = self.scene
        
        self.virtual_keys.append(VirtualKey(self, 'L', kb.K_LEFT, (2,1)))
        self.virtual_keys.append(VirtualKey(self, 'R', kb.K_RIGHT, (4,1)))
        self.virtual_keys.append(VirtualKey(self, 'U', kb.K_UP, (3,0)))
        self.virtual_keys.append(VirtualKey(self, 'D', kb.K_DOWN, (3,1)))
        self.virtual_keys.append(VirtualKey(self, 'R', kb.K_r, (0,2)))
        self.virtual_keys.append(VirtualKey(self, 'ESC', kb.K_ESCAPE, (0,0)))
        self.virtual_keys.append(VirtualKey(self, 'OK', kb.K_RETURN, (6,2)))    
        
        run(self.scene)
        
    def quit(self):
        self.scene.view.close()

 
if __name__ == "__main__" :
    print('start')
    app = GameApp()
    
   # app.image.render()
    GameApp().start()
