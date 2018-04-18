import pygame as pg
import Buttons
import cube as c
from render import Renderer
from math import pi as PI

pg.init()
width = 1000
height = 600
screen = pg.display.set_mode((width, height))
done = False
game_refresh = True
ui_refresh = True
FPS = 60
# timing
clock = pg.time.Clock()

# TODO add reset to 0 button
# TODO add zoom(distance) button
# TODO add render Faces and colors

class UserInterface:
    def __init__(self):
        self.x_state = 0
        self.y_state = 0
        self.z_state = 0
        self.xUpButton = None
        self.xDownButton = None
        self.yUpButton = None
        self.yDownButton = None
        self.zUpButton = None
        self.zDownButton = None
        self._aling_x = 15
        self._aling_y = 10
        self._aling_l = 65
        self._aling_h = 40
        self.color_bg = (100, 100, 100)
        self.x_color = (50, 50, 150)
        self.y_color = (50, 150, 50)
        self.z_color = (150, 50, 50)

    def init(self):
        pg.display.set_caption("Cube Transform")
        self.xUpButton = Buttons.Button()
        self.xDownButton = Buttons.Button()
        self.yUpButton = Buttons.Button()
        self.yDownButton = Buttons.Button()
        self.zUpButton = Buttons.Button()
        self.zDownButton = Buttons.Button()
        # create buttons
        aling_y = self._aling_y
        self.xDownButton.create_button(screen, (100, 100, 100), self._aling_x,
                                       aling_y, self._aling_l, self._aling_h, 0, ">", (255, 255, 255))
        self.xUpButton.create_button(screen, (100, 100, 100), self._aling_x + 90,
                                     aling_y, self._aling_l, self._aling_h, 0, "<", (255, 255, 255))
        aling_y += 50
        self.yDownButton.create_button(screen, (100, 100, 100), self._aling_x,
                                       aling_y, self._aling_l, self._aling_h, 0, ">", (255, 255, 255))
        self.yUpButton.create_button(screen, (100, 100, 100), self._aling_x + 90,
                                     aling_y, self._aling_l, self._aling_h, 0, "<", (255, 255, 255))
        aling_y += 50
        self.zDownButton.create_button(screen, (100, 100, 100), self._aling_x,
                                       aling_y, self._aling_l, self._aling_h, 0, ">", (255, 255, 255))
        self.zUpButton.create_button(screen, (100, 100, 100), self._aling_x + 90,
                                     aling_y, self._aling_l, self._aling_h, 0, "<", (255, 255, 255))

    def _write_text(self, surface, text, text_color, length, height, x, y):
        font_size = 2 * int(length // len(text))
        myFont = pg.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText,
                     ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))
        return surface

    def update(self):
        pass

    def draw(self):
        pg.draw.rect(screen, self.color_bg, pg.Rect(0, 0, width, 60))
        aling_x = self._aling_x
        self._write_text(screen, 'X:', self.x_color, 40, 40, aling_x, 12)
        aling_x += 50
        if self.x_state > 0:
            self.xDownButton.create_button(screen, self.x_color, aling_x,
                                           self._aling_y, self._aling_l, self._aling_h, 0, "<", (255, 255, 255))
        aling_x += 90
        self._write_text(screen, "{:0>3}".format(self.x_state), self.x_color, 90, 40, aling_x - 10, 12)
        aling_x += 100
        if self.x_state < 100:
            self.xUpButton.create_button(screen, self.x_color, aling_x,
                                         self._aling_y, self._aling_l, self._aling_h, 0, ">", (255, 255, 255))
        aling_x += 90
        self._write_text(screen, 'Y:', self.y_color, 40, 40, aling_x, 12)
        aling_x += 50
        if self.y_state > 0:
            self.yDownButton.create_button(screen, self.y_color, aling_x,
                                           self._aling_y, self._aling_l, self._aling_h, 0, "<", (255, 255, 255))
        aling_x += 90
        self._write_text(screen, "{:0>3}".format(self.y_state), self.y_color, 90, 40, aling_x - 10, 12)
        aling_x += 100
        if self.y_state < 100:
            self.yUpButton.create_button(screen, self.y_color, aling_x,
                                         self._aling_y, self._aling_l, self._aling_h, 0, ">", (255, 255, 255))
        aling_x += 90
        self._write_text(screen, 'Z:', self.z_color, 40, 40, aling_x, 12)
        aling_x += 50
        if self.z_state > 0:
            self.zDownButton.create_button(screen, self.z_color, aling_x,
                                           self._aling_y, self._aling_l, self._aling_h, 0, "<", (255, 255, 255))
        aling_x += 90
        self._write_text(screen, "{:0>3}".format(self.z_state), self.z_color, 90, 40, aling_x - 10, 12)
        aling_x += 100
        if self.z_state < 100:
            self.zUpButton.create_button(screen, self.z_color, aling_x,
                                         self._aling_y, self._aling_l, self._aling_h, 0, ">", (255, 255, 255))


class App:
    def __init__(self):
        self.cube = c.Cube(radius=2)
        self.distance = 13
        self.renderer = Renderer(width, height+60, self.distance)
        self.color_bg = (150, 150, 150)
        self.x_color = (50, 50, 150)
        self.y_color = (50, 150, 50)
        self.z_color = (150, 50, 50)
        self.space = [  # ejes
            [c.Point3d(-self.distance, 0, 0), c.Point3d(self.distance, 0, 0)],
            [c.Point3d(0, 0, -self.distance), c.Point3d(0, 0, self.distance)],
            [c.Point3d(0, -self.distance, 0), c.Point3d(0, self.distance, 0)],
            # lines de referencia segun 'distace'
            [c.Point3d(-self.distance, -self.distance, -self.distance), c.Point3d(-self.distance, self.distance, -self.distance)],
            [c.Point3d(-self.distance, -self.distance, -self.distance), c.Point3d(self.distance, -self.distance, -self.distance)],
            [c.Point3d(-self.distance, -self.distance, self.distance), c.Point3d(-self.distance, self.distance, self.distance)],
            [c.Point3d(-self.distance, -self.distance, self.distance), c.Point3d(self.distance, -self.distance, self.distance)],
            [c.Point3d(-self.distance, self.distance, self.distance), c.Point3d(-self.distance, self.distance, -self.distance)],
            [c.Point3d(-self.distance, -self.distance, self.distance), c.Point3d(-self.distance, -self.distance, -self.distance)],
            [c.Point3d(self.distance, -self.distance, self.distance), c.Point3d(self.distance, -self.distance, -self.distance)],
            [c.Point3d(-self.distance, self.distance, -self.distance), c.Point3d(self.distance, self.distance, -self.distance)],
            [c.Point3d(self.distance, self.distance, -self.distance), c.Point3d(self.distance, -self.distance, -self.distance)]]
        self.x_state = 0
        self.y_state = 0
        self.z_state = 0

    def init(self):
        pass

    def update(self, x_state, y_state, z_state):
        self.cube.rotate('x', PI * 2 / 100 * (x_state - self.x_state))
        self.x_state = x_state
        self.cube.rotate('y', PI * 2 / 100 * (y_state - self.y_state))
        self.y_state = y_state
        self.cube.rotate('z', PI * 2 / 100 * (z_state - self.z_state))
        self.z_state = z_state

    def draw(self):
        pg.draw.rect(screen, self.color_bg, pg.Rect(0, 60, width, height-60))
        for line in self.space:
            self.renderer.render_line(screen, line)
        for point in self.cube.vertex:
            self.renderer.render_point(screen, point)
        for line in self.cube.edges:
            self.renderer.render_line(screen, line)
        for v in self.cube.vertex:
            # proyect x
            point = c.Point3d(-self.distance, v.cords[1], v.cords[2])
            self.renderer.render_point(screen, point, self.x_color)
            # proyect y
            point = c.Point3d(v.cords[0], -self.distance, v.cords[2])
            self.renderer.render_point(screen, point, self.y_color)
            # proyect z
            point = c.Point3d(v.cords[0], v.cords[1], -self.distance)
            self.renderer.render_point(screen, point, self.z_color)


ui = UserInterface()
ui.init()
app = App()
app.init()

while not done:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if ui.xUpButton.pressed(pg.mouse.get_pos()):
                if ui.x_state < 100:
                    ui.x_state += 1
            if ui.xDownButton.pressed(pg.mouse.get_pos()):
                if ui.x_state > 0:
                    ui.x_state -= 1
            if ui.yUpButton.pressed(pg.mouse.get_pos()):
                if ui.z_state < 100:
                    ui.y_state += 1
            if ui.yDownButton.pressed(pg.mouse.get_pos()):
                if ui.y_state > 0:
                    ui.y_state -= 1
            if ui.zUpButton.pressed(pg.mouse.get_pos()):
                if ui.z_state < 100:
                    ui.z_state += 1
            if ui.zDownButton.pressed(pg.mouse.get_pos()):
                if ui.z_state > 0:
                    ui.z_state -= 1
    ui.update()
    app.update(ui.x_state, ui.y_state, ui.z_state)
    ui.draw()
    app.draw()
    pg.display.flip()
    clock.tick(FPS)
