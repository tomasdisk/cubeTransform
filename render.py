import cube as c
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

deep_x_streng = -.6
deep_y_streng = -.5
distance = 10


def convert_to_2d(point):
    return c.Point2d(point.cords[0] + (point.cords[1] * deep_x_streng), point.cords[2] + (point.cords[1] * deep_y_streng))


lis3d = [  # ejes
         [c.Point3d(-distance, 0, 0), c.Point3d(distance, 0, 0)],
         [c.Point3d(0, 0, -distance), c.Point3d(0, 0, distance)],
         [c.Point3d(0, -distance, 0), c.Point3d(0, distance, 0)],
         # lines de referencia segun 'distace'
         [c.Point3d(-distance, -distance, -distance), c.Point3d(-distance, distance, -distance)],
         [c.Point3d(-distance, -distance, -distance), c.Point3d(distance, -distance, -distance)],
         [c.Point3d(-distance, -distance, distance), c.Point3d(-distance, distance, distance)],
         [c.Point3d(-distance, -distance, distance), c.Point3d(distance, -distance, distance)],
         [c.Point3d(-distance, distance, distance), c.Point3d(-distance, distance, -distance)],
         [c.Point3d(-distance, -distance, distance), c.Point3d(-distance, -distance, -distance)],
         [c.Point3d(distance, -distance, distance), c.Point3d(distance, -distance, -distance)],
         [c.Point3d(-distance, distance, -distance), c.Point3d(distance, distance, -distance)],
         [c.Point3d(distance, distance, -distance), c.Point3d(distance, -distance, -distance)]]

lis2d = []
for l in lis3d:
    lis2d.append([convert_to_2d(l[0]), convert_to_2d(l[1])])

C = c.Cube(radius=2)
C.rotate('y', 2)
C.rotate('x', 2)
for l in C.edges:
    lis2d.append([convert_to_2d(l[0]), convert_to_2d(l[1])])
    lis2d.append([convert_to_2d(c.Point3d(-distance, l[0].cords[1], l[0].cords[2])),
                  convert_to_2d(c.Point3d(-distance, l[1].cords[1], l[1].cords[2]))])
    lis2d.append([convert_to_2d(c.Point3d(l[0].cords[0], -distance, l[0].cords[2])),
                  convert_to_2d(c.Point3d(l[1].cords[0], -distance, l[1].cords[2]))])
    lis2d.append([convert_to_2d(c.Point3d(l[0].cords[0], l[0].cords[1], -distance)),
                  convert_to_2d(c.Point3d(l[1].cords[0], l[1].cords[1], -distance))])

ax = plt.gca()
for e in lis2d:
    line = mlines.Line2D([e[0].cords[0], e[1].cords[0]], [e[0].cords[1], e[1].cords[1]])
    ax.add_line(line)

# p = c.Point3d(0, 0, 3)
# p = convert_to_2d(p)
# plt.scatter(p.cords[0], p.cords[1])

x = []
y = []
for v in C.vertex:
    # proyect x
    point = c.Point3d(-distance, v.cords[1], v.cords[2])
    p = convert_to_2d(point)
    x.append(p.cords[0])
    y.append(p.cords[1])
    # proyect y
    point = c.Point3d(v.cords[0], -distance, v.cords[2])
    p = convert_to_2d(point)
    x.append(p.cords[0])
    y.append(p.cords[1])
    # proyect z
    point = c.Point3d(v.cords[0], v.cords[1], -distance)
    p = convert_to_2d(point)
    x.append(p.cords[0])
    y.append(p.cords[1])


plt.scatter(x, y)

# set limites x e y iguales para el plot
limit = distance * 2
ax.set_xbound(-limit, limit)
ax.set_ybound(-limit, limit)

plt.show()
