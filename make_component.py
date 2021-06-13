import FreeCAD
import Part
import math

def r(H, W, N, phi):
    # Compute radial coordinate.
    assert N != 0
    a = abs(0.5 * H * math.sin(phi)) ** N + abs(0.5 * W * math.cos(phi)) ** N
    b = (0.25 * H * W) ** N
    return (b / a) ** (1./N)

def y(x, phi, part):
    # Compute y-coordinate on the cross-section: y = r * sin(phi).
    # x: x-coordinate of cross-section.
    # phi: Angle.
    # part: The component whose coefficients will be used (fuselage or pylon).
    assert part.N(x) != 0
    return r(part.H(x), part.W(x), part.N(x), phi) * math.sin(phi)

def z(x, phi, part):
    # Compute z-coordinate on the cross-section: z = r * cos(phi) + Z.
    # x: x-coordinate of cross-section.
    # phi: Angle.
    # part: The component whose coefficients will be used (fuselage or pylon).
    assert part.N(x) != 0
    return r(part.H(x), part.W(x), part.N(x), phi) * math.cos(phi) + part.Z(x)

def make_component(component, x, pr, L):
    # Create component (fuselage or pylon).

    # List of polygons.
    polygons = []

    # Create list of polygons at each cross-section.
    # Loop through x-coordinates.
    for i in range(len(x)-1):
        points = []
        # Loop through periphery of cross-section.
        for j in range(len(pr)-1):
            # Create points along the cross-section with x-, y- and z-coordinates.
            # Note that x-, y- and z-coordinates are multiplied with L to get real (not normalized) coordinates.
            points.append(FreeCAD.Vector(x[i] * L, y(x[i], pr[j], component) * L, z(x[i], pr[j], component) * L))
        points.append(points[0]) # add the first point again in order to close the polygon.
        polygons.append(Part.makePolygon(points)) # add the polygon to the list of polygons.

    loft = Part.makeLoft(polygons, True, False) # Loft through polygons.
    return loft
