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


def _create_polygon(thickness, offset, space, pointyness):
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

    pointstring = ""
    for p in polygon:
        pointstring += str(p) + " "
    return '<polygon points="{}" fill="#090" />'.format(pointstring.strip())


def create(thickness=17, offset=30, space=10, pointedness=7):
    """ Create logo svg image

    :param thickness: Thickness of the line
    :param offset: Distance from begin of segment to begin arrowhead
    :param space: Whitespace inside arrowhead
    :param pointedness: Angle of the arrowhead
    :return: SVG string
    """
    logo_height = _triangle_height(100)

    result = '<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'

    # Shift whole logo downward since a equilateral triangle doesn't fit in a square box
    result += '<g transform="translate(100,100) rotate(180) translate(0, {})">'.format((100 - logo_height) / 2)

    # Create one side
    result += _create_polygon(thickness, offset, space, pointedness)

    # Create rotated second side
    result += '<g transform="translate(100,0) rotate(120) ">'
    result += _create_polygon(thickness, offset, space, pointedness)
    result += '</g>'

    # Create the final piece
    result += '<g transform="translate(50,{}) rotate(240) ">'.format(logo_height)
    result += _create_polygon(thickness, offset, space, pointedness)
    result += '</g>'

    result += "</g></svg>"
    return result


if __name__ == '__main__':
    print(create())
