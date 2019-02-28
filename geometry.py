"""
This module contains various functions for geometry purposes (computing
lines intersections, distances,...) that are used mainly by the game.
"""


def or_det(p1, p2, q):
    return (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])


def unknot_polygon(poly):
    knotted = True
    while knotted:
        knotted = False
        for i in range(-1, len(poly - 1)):
            for j in range(i + 1, len(poly) - 1):
                if segments_intersection(poly[i], poly[i+1],
                                         poly[j], poly[j+1]):
                    poly[i+1], poly[j+1] = poly[j+1], poly[i+1]
                    knotted = True
    return poly


def poly_contains(polygon, point):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n+1):
        p2x, p2y = polygon[i % n]
        if min(p1y, p2y) < point[1] <= max(p1y, p2y):
            if point[0] <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (point[1]-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                if p1x == p2x or point[0] <= xinters:
                    inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def distance_in_poly(p1, p2, poly):
    # TODO: refactor this
    if all(p1[i] == p2[i] for i in range(len(p1))):
        return 0
    for i in range(-1, len(poly) - 1):
        q1, q2 = poly[i], poly[i+1]
        if segments_intersection(p1, p2, q1, q2):
            return distance_in_poly(p1, q2, poly) \
                   + distance_in_poly(p1, q2, poly)
    return eucl_dist(p1, p2)


def sort_points(points):
    mini = 0
    for i in range(1, len(points)):
        if points[i][1] < points[mini][1] \
          or points[i][1] == points[mini][1] \
          and points[i][0] < points[mini][0]:
            mini = i
    points[0], points[mini] = points[mini], points[0]

    # TODO: not use a ducking bubble sort
    for i in range(1, len(points)):
        moved = False
        for j in range(1, len(points) - i):
            side = or_det(points[0], points[j], points[j+1])
            if side > 0 or side == 0 \
              and rect_contains(points[0], points[j], points[j+1]):
                points[j], points[j+1] = points[j+1], points[j]
                moved = True
        if not moved:
            break
    return points


def rect_contains(top_left, bottom_right, point):
    return top_left[0] <= point[0] <= bottom_right[0] and \
        top_left[1] >= point[1] >= bottom_right[1]


def middle(p1, p2):
    return((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)


def line_through(p1, p2):
    """Returns the parameters a and b of the line ax + b passing through two
       points, or None if it is vertical.
    """
    if p1[0] == p2[0]:
        return None
    a = abs(p1[1] - p2[2]) / abs(p1[0] - p2[0])
    b = p1[1] - p1[0] * a
    return (a, b)


def eucl_dist(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def perpendicular(line, point):
    a = - 1 / line[0]
    b = point[1] - a * point[0]
    return (a, b)


def med(p1, p2):
    return perpendicular(line_through(p1, p2), middle(p1, p2))


def lines_intersection(l1, l2):
    """Computes the intersection of two lines and returns it, or None if they
       are parallel.
    """
    if l1[0] == l2[0]:
        return None
    x = (l2[1] - l1[1]) / (l1[0] - l2[0])
    y = x * l1[0] + l1[1]
    return (x, y)


def line_seg_intersection(l, p, q):
    l2 = line_through(p, q)
    inter = lines_intersection(l, l2)
    if min(p[0], q[0]) < inter[0] < max(p[0], q[0]) \
       and min(p[1], q[1]) < inter[1] < max(p[1], q[1]):
        return inter
    else:
        return None


def halfline_seg_intersection(p, q):
    pass


def segments_intersection(p1, q1, p2, q2):
    sides1 = or_det(p1, q1, p2) * or_det(p1, q1, q2)
    sides2 = or_det(p2, q2, p1) * or_det(p2, q2, q1)
    if sides1 < 0 and sides2 < 0:
        l1 = line_through(p1, q1)
        l2 = line_through(p2, q2)
        return lines_intersection(l1, l2)
    return None


def visibility_region(facility, polygon):
    V = []
    for point in polygon:
        vertex = point
        for i in range(-1, len(polygon) - 1):
            inter = segments_intersection(facility, vertex,
                                          polygon[i], polygon[i+1])
            if inter is not None:
                r = eucl_dist(facility, vertex)
                s = eucl_dist(facility, inter)
                if r > s:
                    vertex = inter
        V.append(vertex)
    return sort_points(V)
