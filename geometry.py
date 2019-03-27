"""
This module contains various functions for geometry purposes (computing
lines intersections, distances,...) that are used mainly by the game.
"""

import config
from fractions import Fraction
from random import shuffle


def dot_product(p1, p2, q):
    """Negative if q is on the right of the oriented line defined by (p1, p2),
       Positive if on the left, else zero.
    """
    return (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])


def normalize(vector):
    unit = abs(max(vector, key=abs))
    return (vector[0]/unit,
            vector[1]/unit)


def maximizing_half_plane(f, points):
    """Returns the line passing through f that defines the halfplane that
       contains a maximum number of points. Second return element indicates
       whether the halfplane is underneath the line.
    """
    counter = [[] for point in points]
    for i, p1 in enumerate(points[:-1]):
        for j, p2 in enumerate(points[i+1:]):
            od = dot_product(p1, f, p2)
            if od > 0:
                counter[i].append(p2)
            elif od < 0:
                counter[j+i+1].append(p2)
    index, count = max(enumerate(counter), key=lambda x: len(x[1]))
    return (points[index], f, count)


def contains_full(p1, p2, poly):
    if not poly_contains(poly, p1) or not poly_contains(poly, p2):
        return False
    for i in range(-1, len(poly) - 1):
        if segments_intersection(poly[i], poly[i+1], p1, p2):
            return False
    return True


def is_on(point, p, q):
    """Checks if point is on the line segment defined by p and q.
    """
    return(dot_product(p, q, point) == 0 and
           min(p[0], q[0]) <= point[0] <= max(p[0], q[0]) and
           min(p[1], q[1]) <= point[1] <= max(p[1], q[1]))


def is_strictly_on(point, p, q):
    """Checks if point is strictly on the line segment defined by p and q.
    """
    return point != p and point != q and is_on(point, p, q)


def unknot_polygon(poly):
    knotted = True
    while knotted:
        knotted = False
        for i in range(-1, len(poly) - 1):
            for j in range(i + 1, len(poly) - 1):
                if segments_intersection(poly[i], poly[i+1],
                                         poly[j], poly[j+1]):
                    shuffle(poly)
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
                    xinters = Fraction(Fraction((point[1]-p1y)*(p2x-p1x)),
                                       Fraction(p2y-p1y))+p1x
                if p1x == p2x or point[0] <= xinters:
                    inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def distance_in_poly(p1, p2, poly):
    regions = nonvisibility_regions(p1, poly)
    found = False
    for region in regions:
        if poly_contains(region[1], p2):
            found = True
            anchor, reg = region
            break
    return (eucl_dist(p1, anchor) + distance_in_poly(anchor, p2, reg) if found
            else eucl_dist(p1, p2))


def line_through(p1, p2):
    """Returns the parameters a and b of the line ax + b passing through two
       points. If it is vertical, apply a small perturbation.
    """
    if p1[0] == p2[0]:
        a = 10 * config.W_HEIGHT
    else:
        a = Fraction(Fraction(p1[1] - p2[1]), Fraction(p1[0] - p2[0]))
    b = p1[1] - p1[0] * a
    return (a, b)


def eucl_dist(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def halfline_seg_intersection(p1, q1, p2, q2):
    """Compute the intersection of the halfline defined by p1 and q1
       (extended through q1), and the line segment defined by p2, q2
    """
    l1 = line_through(p1, q1)
    l2 = line_through(p2, q2)
    inter = lines_intersection(l1, l2)
    if inter:
        p_i = eucl_dist(p1, inter)
        q_i = eucl_dist(q1, inter)
        if is_on(inter, p2, q2) and (q_i < p_i or is_on(inter, p1, q1)):
            return inter
    return None


def lines_intersection(l1, l2):
    """Computes the intersection of two lines and returns it, or None if they
       are parallel.
    """
    if l1[0] == l2[0]:
        return None
    x = Fraction(Fraction(l2[1] - l1[1]), Fraction(l1[0] - l2[0]))
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


def segments_intersection(p1, q1, p2, q2):
    sides1 = dot_product(p1, q1, p2) * dot_product(p1, q1, q2)
    sides2 = dot_product(p2, q2, p1) * dot_product(p2, q2, q1)
    # 'sides' will be negative only if points lie on opposite sides
    if sides1 < 0 and sides2 < 0:
        l1 = line_through(p1, q1)
        l2 = line_through(p2, q2)
        return lines_intersection(l1, l2)
    return None


def split_polygon(poly, p, q):
    """Splits a polygon in two by drawing an edge betwween two boundary points,
       assuming they lie on different edges.
       Return a list containing the lists of both subpolygons vertices.
       Runs in O(n) time, where n is |V_polygon|.
    """
    extending = False
    pok, qok = False, False
    subpoly = [[], []]
    for i in range(-1, len(poly) - 1):
        if not pok and is_on(p, poly[i], poly[i+1]):
            if p != poly[i+1]:
                pok = True
                if p != poly[i]:
                    subpoly[extending].append(poly[i])
                subpoly[extending].append(p)
                extending = not extending
                subpoly[extending].append(p)
        elif not qok and is_on(q, poly[i], poly[i+1]):
            if q != poly[i+1]:
                qok = True
                if q != poly[i]:
                    subpoly[extending].append(poly[i])
                subpoly[extending].append(q)
                extending = not extending
                subpoly[extending].append(q)
        else:
            subpoly[extending].append(poly[i])
    assert qok and pok, "Points were not on the polygon boundary!"
    return subpoly


def nonvisibility_regions(facility, polygon):
    regions = []
    for i in range(-1, len(polygon) - 1):
        for j in range(-1, len(polygon) - 1):
            inter = halfline_seg_intersection(facility, polygon[i],
                                              polygon[j], polygon[j+1])
            if not inter or is_on(inter, facility, polygon[i]):
                break
            elif contains_full(facility, inter, polygon):
                anchor = polygon[i]
                polygon, hidden = split_polygon(polygon, anchor, inter)
                if not poly_contains(polygon, facility):
                    polygon, hidden = hidden, polygon
                regions.append((anchor, hidden))
                regions.extend(nonvisibility_regions(facility, polygon))
                return regions
    return regions
