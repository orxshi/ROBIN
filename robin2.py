import sys
import math
import numpy

sys.path.append('/usr/lib/freecad/lib/')

import FreeCAD
import Draft
import Part
#import BOPTools.JoinFeatures
import BOPTools.JoinAPI

INCH_TO_M = 0.0254
ZERO = 1e-10

doc = FreeCAD.newDocument('newdoc')


def U(c, xl):

    u = c[5]

    if c[6] != 0:

        if c[1] != 0:
            t = c[0] + c[1] * abs((xl + c[2]) / c[3]) ** c[4]
            #assert c[3] != 0
            #if ((xl + c[2]) / c[3]) < 0:
                #print("xl:", xl)
                #print("c[2]:", c[2])
                #print("c[3]:", c[3])
            #assert ((xl + c[2]) / c[3]) > 0
            #t = c[0] + c[1] * ((xl + c[2]) / c[3]) ** c[4]
        else:
            t = c[0]

        if abs(t) <= ZERO:
            t = 0

        assert c[7] > 0
        u += c[6] * t ** (1./c[7])

    return u;

class Fuselage:

    def H(xl):

        if xl < 0.4:
            c = [1.0, -1.0, -0.4, 0.4, 1.8, 0.0, 0.25, 1.8]
        elif xl < 0.8:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0]
        elif xl < 1.9:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.05, 0.2, 0.6]
        elif xl < 2.0:
            c = [1.0, -1.0, -1.9, 0.1, 2.0, 0.0, 0.05, 2.0]
        else:
            print("error H")

        return U(c, xl);


    def W(xl):

        if xl < 0.4:
            c = [1.0, -1.0, -0.4, 0.4, 2.0, 0.0, 0.25, 2.0]
        elif xl < 0.8:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0]
        elif xl < 1.9:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.05, 0.2, 0.6]
        elif xl < 2.0:
            c = [1.0, -1.0, -1.9, 0.1, 2.0, 0.0, 0.05, 2.0]
        else:
            print("error W")

        return U(c, xl);


    def Z(xl):

        if xl < 0.4:
            c = [1.0, -1.0, -0.4, 0.4, 1.8, -0.08, 0.08, 1.8]
        elif xl < 0.8:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif xl < 1.9:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.04, -0.04, 0.6]
        elif xl < 2.0:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.04, 0.0, 0.0]

        return U(c, xl);


    def N(xl):

        if xl < 0.4:
            c = [2.0, 3.0, 0.0, 0.4, 1.0, 0.0, 1.0, 1.0]
        elif xl < 0.8:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0]
        elif xl < 1.9:
            c = [5.0, -3.0, -0.8, 1.1, 1.0, 0.0, 1.0, 1.0]
        elif xl < 2.0:
            #c = [2.0, 0.0, 0.0, 0.0, 0.0, 0.04, 1.0, 1.0]
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0, 1.0]
            #c = [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        else:
            print("error N")

        return U(c, xl);

class Pylon:

    def H(xl):

        if xl < 0.8:
            c = [1.0, -1.0, -0.8, 0.4, 3.0, 0.0, 0.145, 3.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 0.218, 2.0, 0.0, 0.145, 2.0]
        else:
            print("error Hpylon")

        return U(c, xl);


    def W(xl):

        if xl < 0.8:
            c = [1.0, -1.0, -0.8, 0.4, 3.0, 0.0, 0.166, 3.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 0.218, 2.0, 0.0, 0.166, 2.0]
        else:
            print("error Wpylon")

        return U(c, xl);


    def Z(xl):

        if xl < 0.4:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.0, 0.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.065, 0.06, 0.6]
        else:
            print("error Zpylon")

        return U(c, xl);


    def N(xl):

        if xl < 0.4:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0]
        elif xl < 1.018:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0]
        else:
            print("error Npylon")

        return U(c, xl);


def yl(xl, phi, part):
    if part.N(xl) == 0:
        print("phi:", phi)
        print("xl:", xl)
    return r(part.H(xl), part.W(xl), part.N(xl), phi) * math.sin(phi)

def zl(xl, phi, part):
    if part.N(xl) == 0:
        print("phi:", phi)
        print("xl:", xl)
    return r(part.H(xl), part.W(xl), part.N(xl), phi) * math.cos(phi) + part.Z(xl)

def r(H, W, N, phi):
    if  N == 0:
        print("N:", N)
    assert N != 0
    a = abs(0.5 * H * math.sin(phi)) ** N + abs(0.5 * W * math.cos(phi)) ** N
    b = (0.25 * H * W) ** N
    return (b / a) ** (1./N)


#L = 78.57 / 2 # so that length of body is 78.70
#L = 78.70 * INCH_TO_M / 2
#L = 78.70 * INCH_TO_M
L = 78.57 * INCH_TO_M / 1.997
dia = 50

#print("L:", L)

xm = numpy.linspace(0.00001, 1.997, 999)
xp = numpy.linspace(0.40001, 1.018, 999)
p = numpy.linspace(0.00001, 2.0*math.pi, 5)


def makepart(part, x):
    polygons = []
    for i in range(len(x)-1):
        points = []
        for j in range(len(p)-1):
            points.append(FreeCAD.Vector(x[i] * L, yl(x[i], p[j], part) * L, zl(x[i], p[j], part) * L))
        points.append(points[0])
        polygons.append(Part.makePolygon(points))

    loft = Part.makeLoft(polygons, True, False)
    cap1 = Part.Face(polygons[0])
    cap2 = Part.Face(polygons[-1])
    #shell = Part.Shell(loft.Faces+[cap1, cap2])
    #Part.show(shell)
    #return shell
    return loft


fuselage = makepart(Fuselage, xm)
pylon = makepart(Pylon, xp)

# make compound
heli = BOPTools.JoinAPI.connect([fuselage, pylon])
#heli = BOPTools.JoinAPI.connect([pylon, fuselage])
#heli = BOPTools.JoinAPI.embed([fuselage, pylon])
#heli = Part.makeCompound([fuselage, pylon])
Part.show(heli)

# make heli a solid
s = Part.Solid(heli)
s.exportStep("fuspyl.step")

# make a sphere
sphere = Part.makeSphere(dia,FreeCAD.Vector(1,0,0))

# cut heli from sphere
cut = sphere.cut(s)
cut_object = doc.addObject("Part::Feature","Cut")
cut_object.Shape = cut

def meshwing():
    import ObjectsFem
    mesh = ObjectsFem.makeMeshGmsh(doc, 'FEMMeshGmsh')
    mesh.ElementDimension = 3
    #mesh.CharacteristicLengthMax = 0.01
    mesh.Part = cut_object;

    mg_fus = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_fus')
    mg_farfield = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_farfield')
    mg_vol = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_vol')

    temp = []
    for i in range(2,len(cut_object.Shape.Faces)+1):
        temp.append((cut_object, 'Face' + str(i)))

    mg_fus.References = temp
    mg_farfield.References = (cut_object, 'Face1')
    mg_vol.References = (cut_object, 'Solid1')

    import femmesh.gmshtools as gmshtools
    gmsh_mesh = gmshtools.GmshTools(mesh)
    gmsh_mesh.create_mesh()

    doc.removeObject("Cut")
    doc.removeObject("FEMMeshGmsh")
    doc.removeObject("mg_fus")
    doc.removeObject("mg_farfield")
    doc.removeObject("mg_vol")
    doc.recompute()


import modifygeo
fn = "fuspyl"
meshwing()
modifygeo.modifygeo(fn, 'Cut', 0, 0, 0)
