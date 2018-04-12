import cube as c
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


class Renderer:
    def __init__(self):
        self.deep_x_streng = -.6
        self.deep_y_streng = -.5

    def _convert_to_2d(self, point3d):
        return c.Point2d(point3d.cords[0] + (point3d.cords[1] * self.deep_x_streng),
                         point3d.cords[2] + (point3d.cords[1] * self.deep_y_streng))

    def add_line(self):
        pass

    def add_rect(self):
        pass

    def render(self):
        pass


class RenderObj:

    type = {
        'point': 1,
        'line': 2,
        'triangle': 3,
        'rectangle': 4
    }

    def __init__(self, point_list=None, index=-1):
        self.point_list = point_list
        self.type = None
        self.index = index
