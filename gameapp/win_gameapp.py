

import pygame
import pygame.constants as kb
from pygame.surface import Surface
from gameapp import Rect, Point, Color
from typing import List, Dict, Tuple
import time
import math

gblScale = 1.0
gblAnchorPoint = (0.5,0.5)
# gblAnchorPoint = (0.0,0.0)
class GameImage():
    def __init__(self, source = None, position = (0,0), *, anchor_point = None, rotation:float = 0.0, scale:float = 1.0, show_rect:bool=False):
        if anchor_point == None:
            anchor_point = gblAnchorPoint
        
        self._image = pygame.Surface((0,0))
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
                self._image = pygame.image.load(source).convert_alpha()
            elif type(source) == GameImage:
                self._image = source._image

            size = self._image.get_size()
            global gblScale
            newsize = (int(size[0] * gblScale), int(size[1] * gblScale))
            self._image = pygame.transform.scale(self._image, newsize)
            self.update_rect(self._image)


    def update_rect(self, img):
        size = img.get_size()
        self._rect._left = self._position._left-(size[0]*self.anchor_point[0])
        self._rect._top = self._position._top-(size[1]*self.anchor_point[1])
        self._rect._width = size[0]
        self._rect._height = size[1]

    def render(self, position = None):
        if position:
            self.position = Point(position[0], position[1])

        # img = self.image
        if self.rotation == 0.0 and self.scale == 1.0:
            img = self._image
        else:        
            img  = pygame.transform.rotozoom(self._image, self.rotation, self.scale) 
            # self._position._left *= self.scale
            # self._position._top *= self.scale
            self.update_rect(img)


        global gblScale
        scaledposition = Point(self.position.left, self.position.top)
        scaledposition.x *= gblScale        
        scaledposition.y *= gblScale

        pygame.display.get_surface().blit(img, (scaledposition.x-(img.get_size()[0]*self.anchor_point[0]), scaledposition.y-(img.get_size()[1]*self.anchor_point[1])))
        if self.show_rect:
            pygame.draw.rect(pygame.display.get_surface(), (0,255,0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), 1)

    def rotate(self, angle:float=0.0, in_place = False):
        if in_place:
            ret = self
        else:
            ret = self.copy()

        ret._image = pygame.transform.rotate(ret._image, angle)
        ret.update_rect(ret._image)

        return ret

    def resize(self, width:float, height:float, in_place:bool = False):
        if in_place:
            ret = self
        else:
            ret = self.copy()

        global gblScale
        ret._image = pygame.transform.scale(ret._image, (width * gblScale, height * gblScale))
        ret.update_rect(ret._image)
        return ret

    def flip(self, vertical:bool=False, horizontal:bool=False, in_place:bool = False):
        if in_place:
            ret = self
        else:
            ret = self.copy()
        
        ret._image = pygame.transform.flip(ret._image, vertical, horizontal)
        ret.update_rect(ret._image)
        return ret

    def rotate_scale(self, angle:float=0, scale:float=1.0, in_place:bool = False):
        if in_place:
            ret = self
        else:
            ret = self.copy()

        ret._image = pygame.transform.rotozoom(ret._image, angle, scale)
        ret.update_rect(ret._image)
        return ret

    def move_angle(self, dist:float, angle:float):
        ang = math.radians(angle)
        dx = dist * math.cos(ang)
        dy = dist * math.sin(ang)
        self.position.x += dx
        self.position.y -= dy
        self.update_rect(self._image)

    def move_to(self, dist:float, point):
        ang = self.get_angle_towards(point)
        self.move_angle(dist, ang)

    def move_around(self, angle:float, point):
        ang = math.radians(angle)
        c = math.cos(ang)
        s = math.sin(ang)

        if type(point) != Point:
            point = Point(point[0], point[1])

        px = self.position.x - point.x
        py = self.position.y - point.y

        xnew = px * c - py * s
        ynew = px * s + py * c

        self.position.x = xnew + point.x
        self.position.y = ynew + point.y

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
        if type(point) != Point:
            point = Point(point[0], point[1])

        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self._image.set_at((int(point.x), int(point.y)), pygame.Color(color.r, color.g, color.b))

    def copy(self):
        gi = GameImage(position = self.position, anchor_point=self.anchor_point, rotation=self.rotation, scale=self.scale, show_rect=self.show_rect)
        gi._image = self._image.copy()
        gi.update_rect(gi._image)
        return gi


class GameShapeRect(GameImage):
    def __init__(self, rect = (0,0,0,0), color = (0,0,0), line_width:int = 1, corner_radius:int = 0):
        '''Draw a Rectangle.

        Parameters
            rect:       list of values representing the rectangle boundaries (left, top, width, height). Can be Rect object
            color:      list of values representing the rectangle color(red, green, blue)
            line_width: width of the line. set to 0 if you want the rectangle to be filled
            corner_radius: radius of the corners. set to 0 to have a square rectangle

        Attributes
            rect:   test1
            color:  tes2
            line:   test4
        '''
        super().__init__()
        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        if type(rect) in (tuple, list):
            rect = Rect(rect[0], rect[1], rect[2], rect[3])

        self.rect = rect
        self._image = pygame.Surface((self.rect.width, self.rect.height))

        self.line_width = line_width
        self.corder_radius = corner_radius

    def render(self):
        if self.rect.size != self._image.get_size():
            self._image = pygame.Surface((self.rect.width, self.rect.height))
            self.update_rect(self._image)

        pygame.draw.rect(pygame.display.get_surface(), self.color.rgb, pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), self.line_width, self.corder_radius)
        
class GameShapeCircle(GameImage):
    def __init__(self, center = (0,0), radius = 0, color = (0,0,0), line_width:int = 1):
        super().__init__(position=center)
        self.radius = radius
        self.line_width = line_width

        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        self._image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.update_rect(self._image)


    def render(self):
        if self.rect.size != (self.radius * 2, self.radius * 2):
            self._image = pygame.Surface((self.radius * 2, self.radius * 2))
            self.update_rect(self._image)

        pygame.draw.circle(pygame.display.get_surface(), pygame.Color(self.color.r, self.color.g, self.color.b), (self.position[0], self.position[1]), self.radius, self.line_width)

class GameShapeLine(GameImage):
    def __init__(self, first_point = (0,0), last_point = (0,0), color = (0,0,0), line_width:int = 1):
        super().__init__()
        self.first_point = Point(first_point[0], first_point[1])
        self.last_point = Point(last_point[0], last_point[1])
        self.line_width = line_width

        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        self._image = pygame.Surface((self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x))
        self.update_rect(self._image)


    def render(self):
        if self.rect.size != (self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x):
            self._image = pygame.Surface((self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x))
            self.update_rect(self._image)
        pygame.draw.line(pygame.display.get_surface(), pygame.Color(self.color.r, self.color.g, self.color.b), self.first_point.point, self.last_point.point, self.line_width)

# class GameShapeTriangle(GameImage):
    # pass


class GameFont():
    def __init__(self, name = 'Verdana', size = 20, is_sys = True):
        self.name = name
        self.size = size
        self.font = None
        self.is_sys = is_sys


    def load(self):
        global gblScale
        if not self.font:
            if self.is_sys:
                self.font = pygame.font.SysFont(self.name, int(self.size * gblScale))
            else:
                self.font = pygame.font.Font(self.name, int(self.size * gblScale))

class GameText(GameImage):
    def __init__(self, text = '', position = (0,0), rotation:float = 0.0, color = (0,0,0), font = GameFont(), anchor_point = None):
        super().__init__(position=position, anchor_point=anchor_point)
        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color
        self.font = font
        self.text = text
        self.rotation = rotation

    @property
    def text(self)->str:
        return self._text

    @text.setter
    def text(self, value:str):
        self._text = value
        self.font.load()
        self._image = self.font.font.render(self._text, True, pygame.Color(self.color.r,self.color.g, self.color.b))
        self.update_rect(self._image)

    def render_text(self, text, position = None):
        self.text = str(text)
        self.render(position)

    # ChatGPT-pasted function to outline text
    def draw_text_with_outline(self, surface, text, font, text_color, outline_color, x, y, outline_width):
        text_surface = font.render(text, True, text_color)
        outline_surface = font.render(text, True, outline_color)

        # Draw the outline
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx * dx + dy * dy <= outline_width * outline_width:
                    surface.blit(outline_surface, (x + dx, y + dy))

        # Draw the main text
        surface.blit(text_surface, (x, y))

class GameAudio():
    def __init__(self, file_name = None, volume = 1):
        self.mySound:pygame.mixer.Sound = None 
        # self.played = False
        if file_name:
            self.load(file_name)
            self.set_volume(volume)
    
    def load(self, file_name):
        if self.mySound:
            self.mySound.stop()
            
        if '.' not in file_name:
            file_name += '.ogg'

        self.mySound = pygame.mixer.Sound(file_name)

    def play(self, numRepeat = 0):
        # if not self.played:
            self.mySound.play(loops = numRepeat)    
            # self.played = True

    def stop(self):
        self.mySound.stop()
        # self.played = False

    def set_volume(self, volume = 1):
        self.mySound.set_volume(volume)

    def get_busy(self):
        return pygame.mixer.get_busy()
        
class VirtualKey():
    def __init__(self, parent, label, key, colrow):
        self.parent = parent
        self.label = label
        self.key = key
        self.diameter = 20
        self.spacing = 2.5
        self.distance = (self.diameter*2) + (self.spacing * 2)

        if parent and colrow:
            xpos = self.diameter + self.spacing
            ypos  = self.parent.surface.get_height() - (self.distance * 3) + self.diameter + self.spacing
            self.position = Rect(xpos + (colrow[0]*self.distance), ypos + (colrow[1]*self.distance), 0, 0)
            self.text = GameText(self, GameFont(self, 'Calibri', 20), label, (self.position.x-10, self.position.y-10))
        
        

    def render(self):
        surf = pygame.display.get_surface()
        pygame.draw.circle(surf, (255,255,255), (self.position[0], self.position[1]), self.diameter)
        self.text.render()
        


class GameTimer():
    def __init__(self, name:str, id:int, milliseconds:float, numRepeats:int, delayMS:float=0.0):
        self.active: bool = True
        self.name:str = name
        self.id:int = id
        self.milliseconds:float = milliseconds
        self.num_repeats:int = numRepeats
        self.ms_at_start:float = 0.0
        self.num_loops_performed:int = 0
        self.delayMS:float = delayMS

    def get_next_run_MS(self):
        return self.ms_at_start + self.delayMS + ((self.num_loops_performed + 1) * self.milliseconds)

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
        

class GameApp:
    def __init__(self, *, width=640, height=480, display_number = 0, full_screen = False, scale = 1.0, has_vk = False, fps = 60):
        self.has_vk = has_vk
        self.platform = 'win'
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

        pygame.init()
        pygame.mixer.init()

        self._clock = pygame.time.Clock()
        vkspace = 0
        if has_vk:
            vk = VirtualKey(None, None, None, None)
            vkspace = vk.distance * 3

        global gblScale
        gblScale = scale
        try:
            self._surface = pygame.display.set_mode((int(self.rect.width * gblScale), int(self.rect.height * gblScale + vkspace)), display=display_number)
        except:
            self._surface = pygame.display.set_mode((int(self.rect.width * gblScale), int(self.rect.height * gblScale + vkspace)), display=0)

        if full_screen == True:
            pygame.display.toggle_fullscreen()
      
    def get_MS(self):
        return self._milliseconds_since_start

    def get_lastframe_MS(self):
        return self._milliseconds_since_last_frame 



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
        if self.has_vk:
            self.virtual_keys.append(VirtualKey(self, 'L', kb.K_LEFT, (5,1)))
            self.virtual_keys.append(VirtualKey(self, 'R', kb.K_RIGHT, (7,1)))
            self.virtual_keys.append(VirtualKey(self, 'U', kb.K_UP, (6,0)))
            self.virtual_keys.append(VirtualKey(self, 'D', kb.K_DOWN, (6,1)))
            self.virtual_keys.append(VirtualKey(self, 'R', kb.K_r, (1,2)))
            self.virtual_keys.append(VirtualKey(self, 'ESC', kb.K_ESCAPE, (1,0)))
            self.virtual_keys.append(VirtualKey(self, 'OK', kb.K_RETURN, (9,2)))

        while( self.is_running ):

            curTime = time.time() * 1000
            self._milliseconds_since_last_frame = curTime - self._milliseconds_since_start
            self._milliseconds_since_start =  curTime


            for event in pygame.event.get():
                for section in self.sections.values():
                    if section.active:
                        if section.on_event(event.type) == False:
                            break

                if event.type == pygame.QUIT:
                    self.is_running = False

                pos = pygame.mouse.get_pos()
                self.mouse_position = Point(pos[0], pos[1])
                if event.type == kb.KEYDOWN:
                    self.pressed_keys.append(event.key)
                    for section in self.sections.values():
                        if section.active:
                            if section.on_key(True, event.key, event.mod) == False:
                                break
                if event.type == kb.KEYUP:
                    self.pressed_keys.remove(event.key)
                    for section in self.sections.values():
                        if section.active:
                            if section.on_key(False, event.key, event.mod) == False:
                                break

                if event.type in (kb.MOUSEBUTTONDOWN, kb.MOUSEBUTTONUP):
                    for vk in self.virtual_keys:
                        vk: VirtualKey 
                        if self.mouse_position.x > vk.position.x - vk.diameter and self.mouse_position.x < vk.position.x + vk.diameter and \
                           self.mouse_position.y > vk.position.y - vk.diameter and self.mouse_position.y < vk.position.y + vk.diameter:
                            for section in self.sections.values():
                                if section.active:
                                    if section.on_key(event.type == kb.MOUSEBUTTONDOWN, vk.key, None) == False:
                                        break
                            
                            if event.type == kb.MOUSEBUTTONDOWN:
                                self.pressed_keys.append(vk.key)
                            else:
                                self.pressed_keys.remove(vk.key)

                global gblScale
                if event.type in (kb.MOUSEBUTTONDOWN, kb.MOUSEBUTTONUP):
                    for section in self.sections.values():
                        if section.active:
                            if section.on_mouse(event.type == kb.MOUSEBUTTONDOWN, event.button, Point(self.mouse_position[0] / gblScale, self.mouse_position[1] / gblScale)) == False:
                                break


            for timer in self.timers.values():
                if timer.active and self._milliseconds_since_start > timer.get_next_run_MS():
                    timer.num_loops_performed += 1
                    for section in self.sections.values():
                        if section.active:
                            if section.on_timer(timer) == False:
                                break
                    #check if last loop
                    #if not infinite timer
                    if timer.num_repeats >= 0 and timer.num_loops_performed > timer.num_repeats:
                        timer.active = False


                    
            for section in self.sections.values():
                if section.active:
                    if section.on_loop() == False:
                        break
                    if section.on_render() == False:
                        break

            #display virtual keys if we have any
            for vk in self.virtual_keys:
                vk.render()

            pygame.display.flip()

            for section in self.sections.values():
                if section.active:
                    if section.on_after_render() == False:
                        break

            self._clock.tick(self._fps)
 
    def stop(self):
        self.is_running = False

    def set_gbl_anchor_point(self, anchor_point):
        global gblAnchorPoint
        gblAnchorPoint = anchor_point

if __name__ == "__main__" :
    GameApp().start()
