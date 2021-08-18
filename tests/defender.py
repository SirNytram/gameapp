from gameapp import GameApp, GameSection, GameImage, kb, Color, GameShapeRect

class GameScreen(GameSection):
    def on_start(self):
        self.bg = GameShapeRect(self.gameapp.rect, Color('black'), line_width=0)
        self.canon = GameImage('tests\\assets\\canon.png', self.gameapp.rect.midbottom).rotate(-90)

    def on_loop(self):
        if kb.K_RIGHT in self.gameapp.pressed_keys:
            self.canon.rotation -= 2

        if kb.K_LEFT in self.gameapp.pressed_keys:
            self.canon.rotation += 2

        self.canon.rotation = self.canon.get_angle_towards(game.mouse_position)

    def on_render(self):
        self.bg.render()
        self.canon.render()

game = GameApp()
game.sections['main'] = GameScreen(game, True)
game.start() 