import cube as c
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

deepStreng = .4


def convert_to_2d(p):
    return c.Point2d(p.cords[0] + (p.cords[2] * deepStreng), p.cords[1] + (p.cords[2] * deepStreng))


lis3d = []
for i in range(-2, 3):
    lis3d.append([c.Point3d(-2, 2, i), c.Point3d(-2, -2, i)])
    lis3d.append([c.Point3d(-2, -2, i), c.Point3d(2, -2, -i)])

for l in lis3d:
    print(l[0].cords, l[1].cords)

lis2d = []
for l in lis3d:
    lis2d.append([convert_to_2d(l[0]), convert_to_2d(l[1])])

for l in lis2d:
    print(l[0].cords, l[1].cords)


ax = plt.gca()
for e in lis2d:
    line = mlines.Line2D([e[0].cords[0], e[1].cords[0]], [e[0].cords[1], e[1].cords[1]])
    ax.add_line(line)

# set limites x e y iguales para el plot
ax.set_xbound(-5, 5)
ax.set_ybound(-5, 5)

plt.show()