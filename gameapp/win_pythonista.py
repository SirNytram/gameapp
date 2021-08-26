class Path():
    def __init__(self) -> None:
        self.line_width =0
    #Create a Path with an oval in the given rectangle.
    def oval(self, x, y, width, height):
        return self


    #Create a Path with a given rectangle.
    def rect(self, x, y, width, height):
        return self

    #Create a Path with a rounded rectangle.
    def rounded_rect(self, x, y, width, height, corner_radius):
        return self

    def move_to(self, x, y):
        pass

    def line_to(self, x, y):
        pass

class Scene():
    def __init__(self):
        self.size = (0,0)

    def add_child(self, object):
        pass

# class Img():
    # anchor
class SpriteNode():
    def __init__(self, texture, position=(0, 0), z_position=0.0, scale=1.0, x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None, size=None, color='white', blend_mode=0):
        # self.image = Img()
        self.anchor_point = (0,0)
        self.scale = 1.0
        self.size = (0,0)
        self.blend_mode = 0
        self.color = (0,0,0)
    def add_child(self, node):
        pass
            
    def remove_from_parent(self):
        pass
    
class LabelNode():
    def __init__(self, text, font = ('', 10), position=(0, 0), z_position=0.0, scale=1.0, x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None, size=None, color='white', blend_mode=0):
        self.anchor_point = (0,0)
        self.scale = 1.0
        self.size = (0,0)
        self.blend_mode = 0
        self.color = (0,0,0)
        self.text = ''
        self.font = ('',0)

    def add_child(self, node):
        pass
            
    def remove_from_parent(self):
        pass

class ShapeNode():
    def __init__(self, path=None, fill_color='white', stroke_color='clear', shadow=None):
        self.anchor_point = (0,0)
        self.scale = 1.0
        self.size = (0,0)
        self.blend_mode = 0
        self.color = (0,0,0)

def run(scene, orientation='DEFAULT_ORIENTATION', frame_interval=1, anti_alias=False, show_fps=False, multi_touch=True):
    pass

class Effect():
    def stop(self):
        pass
    
def play_effect(fileName)->Effect:
    return Effect()