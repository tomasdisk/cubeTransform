import cube as c
from pygame import draw


class Renderer:
    def __init__(self, width, height, scale=10):
        self.height = height
        self.width = width
        self.scale = scale
        self._deep_x_streng = -.8
        self._deep_y_streng = .5

    def _convert_to_2d(self, point3d):
        return c.Point2d((point3d.cords[0] + (point3d.cords[1] * self._deep_x_streng)) * self.scale + self.width / 2,
                         (-point3d.cords[2] + (point3d.cords[1] * self._deep_y_streng)) * self.scale + self.height / 2)

    def render_line(self, screen, line, color=(0, 0, 0)):
        p0 = self._convert_to_2d(line[0]).cords
        p1 = self._convert_to_2d(line[1]).cords
        draw.aaline(screen, color, [p0[0], p0[1]], [p1[0], p1[1]], True)

    def render_rect(self):
        pass

    def render_point(self, screen, point, color=(0, 0, 0)):
        center = self._convert_to_2d(point).cords
        draw.circle(screen, color, [int(center[0]), int(center[1])], 4)

    def render_shape(self):
        pass

