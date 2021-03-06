from math import sin, cos, sqrt
# inported below within methods
# import matplotlib.pyplot as plt
# import matplotlib.lines as mlines


class Point2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cords = (x, y)


class Point3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.cords = (x, y, z)

    def rotate(self, axis, angle, rot_center):
        # dejo fijo el eje sobre el que se rota
        if axis == 'x':  # hay que fijar x y el plano de rotacion es (y, z)
            rot_cord_u = 1
            rot_cord_v = 2
            axis_cord = 0
        elif axis == 'y':  # hay que fijar y y el plano de rotacion es (x, z)
            rot_cord_u = 0
            rot_cord_v = 2
            axis_cord = 1
        elif axis == 'z':  # hay que fijar z y el plano de rotacion es (x, y)
            rot_cord_u = 0
            rot_cord_v = 1
            axis_cord = 2
        else:
            return 0

        # guardo valores (u, v) para rotar en el plano y dejo fijo el eje j
        u = self.cords[rot_cord_u]
        v = self.cords[rot_cord_v]
        j = self.cords[axis_cord]

        # guardo el centro de rotacion (u, v) en el plano y dejo fijo el eje j
        rot_center_u = rot_center.cords[rot_cord_u]
        rot_center_v = rot_center.cords[rot_cord_v]

        s = sin(angle)
        c = cos(angle)

        # trasladar el punto al origen
        u -= rot_center_u
        v -= rot_center_v

        # rotar el punto respecto del origen
        u_new = u * c - v * s
        v_new = u * s + v * c

        # trasladar a la pocicion original
        u = u_new + rot_center_u
        v = v_new + rot_center_v

        # aplico los cambios
        if rot_cord_u == 0:
            self.x = u
        elif rot_cord_u == 1:
            self.y = u
        elif rot_cord_u == 2:
            self.z = u
        if rot_cord_v == 0:
            self.x = v
        elif rot_cord_v == 1:
            self.y = v
        elif rot_cord_v == 2:
            self.z = v
        if axis_cord == 0:
            self.x = j
        elif axis_cord == 1:
            self.y = j
        elif axis_cord == 2:
            self.z = j

        self.cords = (self.x, self.y, self.z)


class Face:
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.vertex = [p1, p2, p3, p4]
        self.edges = [(p1, p2),
                      (p2, p3),
                      (p3, p4),
                      (p4, p1)]

    def rotate(self, axis, angle):
        rot_center = Point3d(0, 0, 0)
        self.p1.rotate(axis, angle, rot_center)
        self.p2.rotate(axis, angle, rot_center)
        self.p3.rotate(axis, angle, rot_center)
        self.p4.rotate(axis, angle, rot_center)

    def mid_point(self):
        x = (self.p1.x + self.p2.x + self.p3.x + self.p4.x) / 4
        y = (self.p1.y + self.p2.y + self.p3.y + self.p4.y) / 4
        z = (self.p1.z + self.p2.z + self.p3.z + self.p4.z) / 4
        return Point3d(x, y, z)

    def dist_center_to_mid(self, point):
        p_mid = self.mid_point()
        return sqrt((point.cords[0]-p_mid.cords[0])**2+(point.cords[1]-p_mid.cords[1])**2+(point.cords[1]-p_mid.cords[1])**2)


class Cube:
    def __init__(self, radius=.5, location=Point3d(0, 0, 0), rotation=None):
        self.radius = radius
        self.location = location
        self.rotation = rotation
        self.vertex = [
            Point3d(self.radius + self.location.x, self.radius + self.location.y, self.radius + self.location.z),
            Point3d(self.radius + self.location.x, -self.radius + self.location.y, self.radius + self.location.z),
            Point3d(self.radius + self.location.x, -self.radius + self.location.y, -self.radius + self.location.z),
            Point3d(self.radius + self.location.x, self.radius + self.location.y, -self.radius + self.location.z),
            Point3d(-self.radius + self.location.x, self.radius + self.location.y, self.radius + self.location.z),
            Point3d(-self.radius + self.location.x, -self.radius + self.location.y, self.radius + self.location.z),
            Point3d(-self.radius + self.location.x, -self.radius + self.location.y, -self.radius + self.location.z),
            Point3d(-self.radius + self.location.x, self.radius + self.location.y, -self.radius + self.location.z)]
        self.f1 = Face(self.vertex[0], self.vertex[1], self.vertex[2], self.vertex[3])  # fijo x
        self.f2 = Face(self.vertex[4], self.vertex[5], self.vertex[6], self.vertex[7])  # fijo -x
        self.f3 = Face(self.vertex[0], self.vertex[4], self.vertex[7], self.vertex[3])  # fijo y
        self.f4 = Face(self.vertex[1], self.vertex[5], self.vertex[6], self.vertex[2])  # fijo -y
        self.f5 = Face(self.vertex[0], self.vertex[4], self.vertex[5], self.vertex[1])  # fijo z
        self.f6 = Face(self.vertex[3], self.vertex[7], self.vertex[6], self.vertex[2])  # fijo -z
        self.faces = [self.f1, self.f2, self.f3, self.f4, self.f5, self.f6]
        # los edges son la union de cada punto de la cara f1 y f2 con el punto que le sigue de la misma cara
        # y las uniones entre puntos iguales entre caras
        self.edges = [(self.f1.p1, self.f1.p2),
                      (self.f1.p2, self.f1.p3),
                      (self.f1.p3, self.f1.p4),
                      (self.f1.p4, self.f1.p1),
                      (self.f2.p1, self.f2.p2),
                      (self.f2.p2, self.f2.p3),
                      (self.f2.p3, self.f2.p4),
                      (self.f2.p4, self.f2.p1),
                      (self.f1.p1, self.f2.p1),
                      (self.f1.p2, self.f2.p2),
                      (self.f1.p3, self.f2.p3),
                      (self.f1.p4, self.f2.p4)]

    def rotate(self, axis, angle):
        rot_center = self.location
        for v in self.vertex:
            v.rotate(axis, angle, rot_center)

    def proyect_vertex(self, axis):
        if axis == 'x':  # el resultado es un punto proyectado (y, z)
            rot_cord_u = 1
            rot_cord_v = 2
        elif axis == 'y':  # el resultado es un punto proyectado (x, z)
            rot_cord_u = 0
            rot_cord_v = 2
        elif axis == 'z':  # el resultado es un punto proyectado (x, y)
            rot_cord_u = 0
            rot_cord_v = 1
        else:
            return 0

        # devuelvo un lista de Point2d proyectados en el plano axis
        lis = []
        for v in self.vertex:
            lis.append(Point2d(v.cords[rot_cord_u], v.cords[rot_cord_v]))
        return lis

    def proyect_edges(self, axis):
        if axis == 'x':  # el resultado es un punto proyectado (y, z)
            rot_cord_u = 1
            rot_cord_v = 2
        elif axis == 'y':  # el resultado es un punto proyectado (x, z)
            rot_cord_u = 0
            rot_cord_v = 2
        elif axis == 'z':  # el resultado es un punto proyectado (x, y)
            rot_cord_u = 0
            rot_cord_v = 1
        else:
            return 0

        # devuelvo un lista de pares de Point2d proyectados en el plano axis
        lis = []
        for e in self.edges:
            lis.append((Point2d(e[0].cords[rot_cord_u], e[0].cords[rot_cord_v]),
                        Point2d(e[1].cords[rot_cord_u], e[1].cords[rot_cord_v])))
        return lis

    def proyect_perimeter(self, axis):
        # lis = self.proyectVertex(axis)
        # TODO quedarme con los Point2d en la lista que pertencen al perimetro
        pass

    def shadow_area(self, axis):
        # lis = self.proyectPerimeter(axis)
        pass

    def plot_points_proyection(self, axis):
        import matplotlib.pyplot as plt
        x = []
        y = []
        for p in self.proyect_vertex(axis):
            x.append(p.cords[0])
            y.append(p.cords[1])

        plt.scatter(x, y)

        # set limites x e y iguales para el plot
        ax = plt.gca()
        xmin, xmax = ax.get_xbound()
        ymin, ymax = ax.get_ybound()
        ax.set_xbound(min(xmin, ymin), max(xmax, ymax))
        ax.set_ybound(ax.get_ybound())

        plt.show()

    def plot_cube_proyection(self, axis):
        import matplotlib.pyplot as plt
        import matplotlib.lines as mlines
        ax = plt.gca()
        for e in self.proyect_edges(axis):
            line = mlines.Line2D([e[0].cords[0], e[1].cords[0]], [e[0].cords[1], e[1].cords[1]])
            ax.add_line(line)
        for v in self.proyect_vertex(axis):
            plt.scatter(v.cords[0], v.cords[1], c='b')

        # set limites x e y iguales para el plot
        xmin, xmax = ax.get_xbound()
        ymin, ymax = ax.get_ybound()
        ax.set_xbound(min(xmin, ymin), max(xmax, ymax))
        ax.set_ybound(ax.get_ybound())

        plt.show()


if __name__ == "__main__":
    C = Cube()
    print("Se lo proyecta el cubo sobre el eje Z.")
    C.plot_cube_proyection('z')
    print("Se rota el cubo 2 radianes en el eje Y, luego se lo proyecta sobre Z.")
    C.rotate('y', 2)
    C.plot_cube_proyection('z')
    print("Se vuelver a rotar el cubo 2 radianes en el eje X, luego se lo vuelve proyectar sobre Z.")
    C.rotate('x', 2)
    C.plot_cube_proyection('z')
