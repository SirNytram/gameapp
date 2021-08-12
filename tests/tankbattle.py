from pygame.draw import line
from gameapp import GameApp, GameSection, GameImage, kb, GameAudio, GameText, GameFont, Rect, Point, Color, GameTimer, GameShapeRect, GameShapeCircle
from typing import List
from random import randint

class Level(GameSection):
    def on_start(self):
        self.bg = GameShapeRect(self.gameapp.rect, color=Color('black'), line_width=0)
        self.crash_boundaries = GameShapeCircle(radius=20, color=Color('green'))
        self.player = GameImage('tests\\assets\\tank_green.png', (20,20), scale=0.5).rotate(-90)
        self.player.rotation = -45
        self.enemy = GameImage('tests\\assets\\tank_purple.png', (400,200), scale=0.5).rotate(-90)
        self.crash_sound = GameAudio('tests\\assets\\crash.wav')
        self.text = GameText('', (0,0), (255,0,0), anchor_point=(0,0))
        self.coin = GameShapeCircle( (randint(0, int(self.gameapp.rect.right)), randint(0, int(self.gameapp.rect.bottom))) , 
                        radius=4, 
                        color=Color('yellow'), 
                        line_width=0)

        self.iscolliding = False
        self.auto_follow = False
        self.player_bullets:List[GameShapeCircle] = []


    def on_loop(self):
        if kb.K_UP in self.gameapp.pressed_keys:
            if not self.iscolliding:
                self.player.move_angle(5, self.player.rotation)

        if kb.K_DOWN in self.gameapp.pressed_keys:
            self.player.move_angle(-2, self.player.rotation)


        if kb.K_RIGHT in self.gameapp.pressed_keys:
            self.player.rotation -= 2

        if kb.K_LEFT in self.gameapp.pressed_keys:
            self.player.rotation += 2


        if self.player.position.distanceTo(self.enemy.position) < 40:
            if not self.iscolliding:
                self.crash_sound.play()
            self.iscolliding = True
        else:
            self.iscolliding = False 

        for bullet in self.player_bullets:
            bullet.move_angle(5, bullet.rotation)
            if bullet.position.x < 0 or bullet.position.y < 0 or bullet.position.x > self.gameapp.rect.right or bullet.position.y > self.gameapp.rect.bottom:
                self.player_bullets.remove(bullet)

        self.enemy.rotation= self.enemy.get_angle_towards(self.player.position)
        if self.auto_follow and not self.iscolliding:
            self.enemy.move_to(2, self.player.position)

    def on_render(self):
        self.bg.render()
        for bullet in self.player_bullets:
            bullet.render()

        self.player.render()
        self.enemy.render()
        self.coin.render()

        self.crash_boundaries.position = self.player.position
        self.crash_boundaries.render()
        

    def on_key(self, is_down, key, mod):
        if is_down:
            if key == kb.K_a:
                self.auto_follow = not self.auto_follow

            if key == kb.K_RCTRL:
                bullet = GameShapeCircle(center=self.player.position, radius=4,color=Color('red'), line_width=0)
                bullet.rotation = self.player.rotation
                self.player_bullets.append(bullet)

            if key == kb.K_ESCAPE:
                self.gameapp.quit()


game = GameApp(display_number=1, width= 600, height=600)
game.sections['car'] = Level(game, True)
game.start()