import arcade
black = (0, 0, 0)

from .toch_geo import xywhToPoints, cirBox


class Quad:
    def __init__(self, center, width, height, col=black, filled=False):
        self.cenx = center[0]
        self.ceny = center[1]
        self.width = width
        self.height = height
        self.rect = arcade.rect.XYWH(center[0], center[1], width, height)
        self.col = col  # Color
        self.filled = filled  # Filled or outline
        self.tilt = 0  # Rotation angle in degrees
        self.thickness = 4  # Outline thickness
        self.yesdraw = True  # Flag to draw or not

    def draw(self):
        if self.yesdraw:
            if self.filled:
                arcade.draw_rect_filled(self.rect, self.col, self.tilt)
            else:
                arcade.draw_rect_outline(self.rect, self.col, self.thickness, self.tilt)

    def move(self, dx, dy):
        self.cenx += dx
        self.ceny += dy
        self.rect = arcade.rect.XYWH(self.cenx, self.ceny, self.width, self.height)

    def moveleft(self, dx):
        self.move(-dx, 0)

    def moveright(self, dx):
        self.move(dx, 0)

    def moveup(self, dy):
        self.move(0, dy)

    def movedown(self, dy):
        self.move(0, -dy)

    def teleport(self, xspot, yspot):
        self.rect.x = xspot
        self.rect.y = yspot

    def rotate(self, angle):
        if self.tilt + angle < 360:
            self.tilt += angle

    def rotate_set(self, angle):
        if angle < 360:
            self.tilt = angle

    def hide(self):
        self.yesdraw = False

    def show(self):
        self.yesdraw = True

    def get_points(self):
        return xywhToPoints(self.cenx, self.ceny, self.width, self.height)


class Circle:
    def __init__(self, center, width, height, col=black, filled=False):
        self.center = center
        self.x = width
        self.y  = height
        self.col = col
        self.filled = filled
        self.tilt = 0
        self.thickness = 4
        self.yesdraw = True
        self.circle = None

    def draw(self):
        if self.yesdraw:
            if self.filled:
                arcade.draw_ellipse_filled(self.center[0], self.center[1], self.x, self.y, self.col, self.tilt)
            else:
                arcade.draw_ellipse_outline(self.center[0], self.center[1], self.x, self.y, self.col, self.thickness, self.tilt)

    def move(self, dx, dy):
        self.center = (self.center[0]+dx, self.center[1]+dy)

    def moveleft(self, dx):
        self.center = (self.center[0]-dx, self.center[1])

    def moveright(self, dx):
        self.center = (self.center[0]+dx, self.center[1])

    def moveup(self, dy):
        self.center = (self.center[0], self.center[1]+dy)

    def movedown(self, dy):
        self.center = (self.center[0], self.center[1]-dy)

    def teleport(self, xspot, yspot):
        self.center = (xspot, yspot)

    def rotate(self, angle):
        if self.tilt + angle < 360:
            self.tilt += angle

    def rotate_set(self, angle):
        if angle < 360:
            self.tilt = angle

    def hide(self):
        self.yesdraw = False

    def show(self):
        self.yesdraw = True

    def get_box(self):
        return cirBox(self.center, self.x, self.y)



class Line:
    def __init__(self, start, end, col=black, thickness=4):
        self.start = start
        self.end = end
        self.col = col
        self.thickness = thickness
        self.yesdraw = True

    def draw(self):
        if self.yesdraw:
            arcade.draw_line(self.start[0], self.start[1], self.end[0], self.end[1], color=self.col, line_width=self.thickness)

    def hide(self):
        self.yesdraw = False

    def show(self):
        self.yesdraw = True

    def distort_shape(self, start, end):
        self.start = start
        self.end = end

class Trio:
    def __init__(self, poi1, poi2, poi3, col=black, filled=False):
        self.poi1 = poi1
        self.poi2 = poi2
        self.poi3 = poi3
        self.col = col
        self.filled = filled
        self.yesdraw = True
        self.thickness = 4

    def draw(self):
        if self.yesdraw:
            if self.filled:
                arcade.draw_triangle_filled(self.poi1[0], self.poi1[1], self.poi2[0], self.poi2[1], self.poi3[0], self.poi3[1], self.col)
            else:
                arcade.draw_triangle_outline(self.poi1[0], self.poi1[1], self.poi2[0], self.poi2[1], self.poi3[0], self.poi3[1], self.col, self.thickness)

    def move(self, dx, dy):
        self.poi1 = (self.poi1[0] + dx, self.poi1[1] + dy)
        self.poi2 = (self.poi2[0] + dx, self.poi2[1] + dy)
        self.poi3 = (self.poi3[0] + dx, self.poi3[1] + dy)

    def moveleft(self, dx):
        self.poi1 = (self.poi1[0] - dx, self.poi1[1])
        self.poi2 = (self.poi2[0] - dx, self.poi2[1])
        self.poi3 = (self.poi3[0] - dx, self.poi3[1])

    def moveright(self, dx):
        self.poi1 = (self.poi1[0] + dx, self.poi1[1])
        self.poi2 = (self.poi2[0] + dx, self.poi2[1])
        self.poi3 = (self.poi3[0] + dx, self.poi3[1])

    def movedown(self, dy):
        self.poi1 = (self.poi1[0], self.poi1[1] - dy)
        self.poi2 = (self.poi2[0], self.poi2[1] - dy)
        self.poi3 = (self.poi3[0], self.poi3[1] - dy)

    def moveup(self, dy):
        self.poi1 = (self.poi1[0], self.poi1[1] + dy)
        self.poi2 = (self.poi2[0], self.poi2[1] + dy)
        self.poi3 = (self.poi3[0], self.poi3[1] + dy)

    def teleport(self, new_x, new_y):
        # Calculate the center of the triangle
        center_x = (self.poi1[0] + self.poi2[0] + self.poi3[0]) / 3
        center_y = (self.poi1[1] + self.poi2[1] + self.poi3[1]) / 3
        # Find the difference to move the center
        dx = new_x - center_x
        dy = new_y - center_y
        # Move all points by the same offset
        self.poi1 = (self.poi1[0] + dx, self.poi1[1] + dy)
        self.poi2 = (self.poi2[0] + dx, self.poi2[1] + dy)
        self.poi3 = (self.poi3[0] + dx, self.poi3[1] + dy)

    def distort_shape(self, poi1, poi2, poi3):
        self.poi1 = poi1
        self.poi2 = poi2
        self.poi3 = poi3

    def hide(self):
        self.yesdraw = False

    def show(self):
        self.yesdraw = True

    def get_points(self):
        return [self.poi1, self.poi2, self.poi3]


class Poly:
    def __init__(self, points, col=black, filled=False):
        self.points = points
        self.col = col
        self.filled = filled
        self.yesdraw = True
        self.thickness = 4

    def draw(self):
        if self.yesdraw:
            if self.filled:
                arcade.draw_polygon_filled(self.points, self.col)
            else:
                arcade.draw_polygon_outline(self.points, self.col, self.thickness)

    def move(self, dx, dy):
        self.points = [(x + dx, y + dy) for x, y in self.points]

    def moveleft(self, dx):
        self.points = [(x - dx, y) for x, y in self.points]

    def moveright(self, dx):
        self.points = [(x + dx, y) for x, y in self.points]

    def moveup(self, dy):
        self.points = [(x, y + dy) for x, y in self.points]

    def movedown(self, dy):
        self.points = [(x, y - dy) for x, y in self.points]

    def teleport(self, xspot, yspot):
        # Calculate the center
        center_x = sum(x for x, y in self.points) / len(self.points)
        center_y = sum(y for x, y in self.points) / len(self.points)
        # Find the difference to move the center
        dx = xspot - center_x
        dy = yspot - center_y
        self.points = [(x + dx, y + dy) for x, y in self.points]

    def distort_shape(self, newpoints):
        self.points = newpoints

    def hide(self):
        self.yesdraw = False

    def show(self):
        self.yesdraw = True

    def get_points(self):
        return [(x, y) for x, y in self.points]

class Arc:
    def __init__(self, circle, start_angle, end_angle, col=black, filled=False):
        self.center_x = circle[0]
        self.center_y = circle[1]
        self.width = circle[2]
        self.height = circle[3]
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.color = col
        self.angle = 0  # Rotation angle, initially 0
        self.yesdraw = True
        self.filled = filled
        self.thickness = 4
        self.circle = None

    def draw(self):
        if self.yesdraw:
            if self.filled:
                arcade.draw_arc_filled(
                self.center_x, self.center_y, self.width, self.height,
                self.color, self.start_angle, self.end_angle, self.angle
            )
            else:
                arcade.draw_arc_outline(
                    self.center_x, self.center_y, self.width, self.height,
                    self.color, self.start_angle, self.end_angle, self.thickness, self.angle
                )

    def move(self, dx, dy):
        self.center_x += dx
        self.center_y += dy

    def moveleft(self, dx):
        self.center_x -= dx

    def moveright(self, dx):
        self.center_x += dx

    def moveup(self, dy):
        self.center_y += dy

    def movedown(self, dy):
        self.center_y -= dy

    def teleport(self, xspot, yspot):
        self.center_x = xspot
        self.center_y = yspot

    def rotate(self, angle):
        if angle + self.tilt < 360:
            self.angle += angle

    def rotate_set(self, angle):
        if angle < 360:
            self.angle = angle

    def hide(self):
        self.yesdraw = False

    def show(self):
        self.yesdraw = True

    def get_box(self):
        return cirBox(self.center, self.x, self.y)

class Parabola:
    def __init__(self, start, end, height, col=black, filled=False):
        self.start = start
        self.end = end
        self.height = height
        self.col = col
        self.filled = filled
        self.yesdraw = True
        self.thickness = 4

    def draw(self):
        if self.yesdraw:
            if self.filled:
                arcade.draw_parabola_filled(self.start[0], self.start[1], self.end, self.height, self.col)
            else:
                arcade.draw_parabola_outline(self.start[0], self.start[1], self.end,
                                            self.height, self.col, self.thickness)

    def hide(self):
        self.yesdraw = False

    def show(self):
        self.yesdraw = True

    def distort_shape(self, start, end):
        self.start = start
        self.end = end



__all__ = ['Arc', 'Circle', 'Line', 'Parabola', 'Poly', 'Quad', 'Trio']
