import math


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return '{0:.1f},{1:.1f}'.format(self.x, self.y)


def _triangle_height(base):
    return (math.sqrt(3) / 2.0) * base


def _point_between(a, b, offset):
    angle = _point_angle(a, b)
    distance = _distance(a, b)
    distance *= offset
    return _move(a, angle, distance)


def _distance(a, b):
    return math.sqrt(((b.x - a.x) ** 2) + ((b.y - a.y) ** 2))


def _point_angle(a, b):
    return math.atan2(b.y - a.y, b.x - a.x) * 180 / math.pi


def _move(start, angle, distance):
    x = start.x
    y = start.y
    angle = math.radians(angle)
    x += distance * math.cos(angle)
    y += distance * math.sin(angle)
    return Point(x, y)


def _midpoint(a, b):
    return _point_between(a, b, 0.5)


def _create_polygon(points):
    pointstring = ""
    for p in points:
        pointstring += str(p) + " "
    return '<polygon points="{}" fill="#090" />'.format(pointstring.strip())


def _create_triangle_side(thickness, offset, space, pointyness):
    height = _triangle_height(100)

    angle = _point_angle(Point(0, 0), Point(50, height))

    outer_angle_point = _point_between(Point(0, 0), Point(50, height), offset / 100.0)
    inner_angle_point = _move(outer_angle_point, angle - 90, thickness)

    midpoint = _midpoint(inner_angle_point, outer_angle_point)
    tip = _move(midpoint, angle, pointyness)

    polygon = [
        inner_angle_point,
        tip,
        outer_angle_point,
        Point(0, 0),
        Point(100 - offset - (space / 2), 0),
        Point(100 - offset - (space / 2) - pointyness, thickness / 2),
        Point(100 - offset - (space / 2), thickness),
        Point(thickness * 1.75, thickness)
    ]

    return _create_polygon(polygon)


def _create_square_side(thickness, offset, space, pointyness, alength, blength):
    blength += thickness

    midpoint_a = _midpoint(Point(space, 0), Point(space, thickness))
    arraw_a = _move(midpoint_a, 0, pointyness)

    midpoint_b = _midpoint(Point(alength, blength), Point(alength - thickness, blength))
    arraw_b = _move(midpoint_b, 90, pointyness)

    points = [
        Point(space, 0),
        Point(alength, 0),
        Point(alength, blength),
        arraw_b,
        Point(alength - thickness, blength),
        Point(alength - thickness, thickness),
        Point(space, thickness),
        arraw_a
    ]

    return _create_polygon(points)


def _create_path(commands, color):
    d = ""
    for command in commands:
        d += str(command) + " "
    return '<path d="{}" fill="{}" />'.format(d.strip(), color)


def _create_phone(width, height, radius, bezel):
    result = ""
    commands = []
    # starting point
    commands.append('M 0 {}'.format(radius))
    # top left corner
    commands.append('A {radius} {radius} 0 0 1 {x} {y}'.format(radius=radius, x=radius, y=0))
    # top line
    commands.append('h {}'.format(width - radius - radius))
    # top right corner
    commands.append('a {radius} {radius} 0 0 1 {x} {y}'.format(radius=radius, x=radius, y=radius))
    # right line
    commands.append('v {}'.format(height - radius - radius))
    # bottom right corner
    commands.append('a {radius} {radius} 0 0 1 {x} {y}'.format(radius=radius, x=-radius, y=radius))
    # bottom line
    commands.append('h {}'.format(-(width - radius - radius)))
    # bottom left corner
    commands.append('a {radius} {radius} 0 0 1 {x} {y}'.format(radius=radius, x=-radius, y=-radius))
    # close shape
    commands.append('Z')

    result += _create_path(commands, '#000')

    # Draw the screen
    result += '<rect x="{}" y="{}" width="{}" height="{}" fill="{}"/>'.format(bezel, radius, width - bezel - bezel,
                                                                              height - radius - radius, '#fff')

    hole_radius = radius / 2
    hole_width = width / 3

    commands = []
    commands.append('M {} {}'.format(hole_width + hole_radius, hole_radius * 1.5))
    commands.append('a {radius} {radius} 0 1 1 {x} {y}'.format(radius=hole_radius / 2, x=0, y=-hole_radius))
    commands.append('h {}'.format(hole_width - hole_radius - hole_radius))
    commands.append('a {radius} {radius} 0 1 1 {x} {y}'.format(radius=hole_radius / 2, x=0, y=hole_radius))
    commands.append('Z')
    result += _create_path(commands, '#fff')

    commands = []
    commands.append('M {} {}'.format(hole_width + hole_radius, height - (hole_radius * 0.5)))
    commands.append('a {radius} {radius} 0 1 1 {x} {y}'.format(radius=hole_radius / 2, x=0, y=-hole_radius))
    commands.append('h {}'.format(hole_width - hole_radius - hole_radius))
    commands.append('a {radius} {radius} 0 1 1 {x} {y}'.format(radius=hole_radius / 2, x=0, y=hole_radius))
    commands.append('Z')
    result += _create_path(commands, '#fff')

    return result


def create(thickness=17, offset=30, space=10, pointedness=7, phone=True):
    """ Create logo svg image

    :param thickness: Thickness of the line
    :param offset: Distance from begin of segment to begin arrowhead
    :param space: Whitespace inside arrowhead
    :param pointedness: Angle of the arrowhead
    :return: SVG string
    """
    logo_height = _triangle_height(100)

    result = '<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'

    logo_translate = ""
    if phone:
        result += '<g transform="translate(20,0)">'
        result += _create_phone(60, 100, 10, 5)
        result += '</g>'
        logo_translate = "scale(0.5) translate(50,50)"

    # Shift whole logo downward since a equilateral triangle doesn't fit in a square box
    result += '<g transform="translate(100,100) rotate(180) translate(0, {}){}">'.format((100 - logo_height) / 2,
                                                                                         logo_translate)

    # Create one side
    result += _create_triangle_side(thickness, offset, space, pointedness)

    # Create rotated second side
    result += '<g transform="translate(100,0) rotate(120) ">'
    result += _create_triangle_side(thickness, offset, space, pointedness)
    result += '</g>'

    # Create the final piece
    result += '<g transform="translate(50,{}) rotate(240) ">'.format(logo_height)
    result += _create_triangle_side(thickness, offset, space, pointedness)
    result += '</g>'

    result += "</g></svg>"
    return result


def create_rectangular(thickness=17, width=50, offset=17, space=5, pointedness=7):
    result = '<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    result += '<g transform="translate({}, 0)">'.format((100 - width) / 2)

    result += _create_square_side(thickness, offset, space, pointedness, width, 0)

    # Create rotated second side
    result += '<g transform="translate({},{}) rotate(90) ">'.format(width, thickness)
    result += _create_square_side(thickness, offset, space, pointedness, 100 - thickness, 0)
    result += '</g>'

    # Create rotated second side
    result += '<g transform="translate({},{}) rotate(180) ">'.format(2 * thickness - 1, 100)
    result += _create_square_side(thickness, offset, space, pointedness, width, 0)
    result += '</g>'

    # Create rotated second side
    result += '<g transform="translate({},{}) rotate(270) ">'.format(-thickness, 100 - thickness)
    result += _create_square_side(thickness, offset, space, pointedness, 100 - thickness, 0)
    result += '</g>'

    result += "</g></svg>"
    return result


if __name__ == '__main__':
    print(create())
