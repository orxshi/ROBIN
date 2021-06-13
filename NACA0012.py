import FreeCAD

thick = 12 / 100;

def y(x, chord):
    C1 = 0.2969
    C2 = 0.1260
    C3 = 0.3516
    C4 = 0.2843
    C5 = 0.1036
    xc = x / chord
    y = thick * chord / 0.2 * (C1 * xc**(1/2) - C2 * xc**(1) - C3 * xc**(2) + C4 * xc**(3) - C5 * xc**(4))
    return y

def make_NACA0012_points(x, chord):
    points = []
    # Upper half of the profile.
    for i in range(len(x)):
        points.append(FreeCAD.Vector(x[i], y(x[i], chord), 0))
    # Lower half of the profile.
    for i in reversed(range(1, len(x)-1)):
        points.append(FreeCAD.Vector(x[i], -y(x[i], chord), 0))
    points.append(points[0]) # add the first point to close the polygon.
    return points
