import sys
import math
import numpy

sys.path.append('/usr/lib/freecad/lib/')

import FreeCAD
import Draft
import Part
import BOPTools.JoinFeatures

doc = FreeCAD.newDocument('newdoc')

ZERO = 1e-10

def U(c, xl):

    u = c[5]

    if c[6] != 0:

        t = c[0] + c[1] * abs((xl + c[2]) / c[3]) ** c[4]
        if abs(t) <= ZERO:
            t = 0

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
            c = [2.0, 0.0, 0.0, 0.0, 0.0, 0.04, 1.0, 1.0]

        return U(c, xl);

class Pylon:

    def H(xl):

        if xl < 0.8:
            c = [1.0, -1.0, -0.8, 0.4, 3.0, 0.0, 0.145, 3.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 0.218, 2.0, 0.0, 0.145, 2.0]

        return U(c, xl);


    def W(xl):

        if xl < 0.8:
            c = [1.0, -1.0, -0.8, 0.4, 3.0, 0.0, 0.166, 3.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 0.218, 2.0, 0.0, 0.166, 2.0]

        return U(c, xl);


    def Z(xl):

        if xl < 0.4:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.0, 0.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.065, 0.06, 0.6]

        return U(c, xl);


    def N(xl):

        if xl < 0.4:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0]
        elif xl < 1.018:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0]

        return U(c, xl);


def yl(xl, phi, part):
    return r(part.H(xl), part.W(xl), part.N(xl), phi) * math.sin(phi)

def zl(xl, phi, part):
    return r(part.H(xl), part.W(xl), part.N(xl), phi) * math.cos(phi) + part.Z(xl)

def r(H, W, N, phi):
    a = abs(0.5 * H * math.sin(phi)) ** N + abs(0.5 * W * math.cos(phi)) ** N
    b = (0.25 * H * W) ** N
    return (b / a) ** (1./N)


L = 78.70 / 2 # so that length of body is 78.70

xm = numpy.linspace(0.00001, 2, 10) # 20
xp = numpy.linspace(0.40001, 1.018, 10) # 20
p = numpy.linspace(0, 2*math.pi, 10) # 30

#yy = []
#zz = []

def makepart(part, x):
    polygons = []
    for i in range(len(x)-1):
        points = []
        for j in range(len(p)-1):
            points.append(FreeCAD.Vector(x[i] * L, yl(x[i], p[j], part) * L, zl(x[i], p[j], part) * L))
            #yy.append(yl(x[i], p[j], part))
            #zz.append(zl(x[i], p[j], part))
        points.append(points[0])
        polygons.append(Part.makePolygon(points))

    loft = Part.makeLoft(polygons)
    cap1 = Part.Face(polygons[0])
    cap2 = Part.Face(polygons[-1])
    shell = Part.Shell(loft.Faces+[cap1, cap2])
    #Part.show(shell)
    return shell



fuselage = makepart(Fuselage, xm)
pylon = makepart(Pylon, xp)

#print(max(yy))
#print(max(zz))

# make compound
heli = Part.makeCompound([fuselage, pylon])

# make heli a solid
s = Part.Solid(heli)
#Part.show(heli)
s.exportStep("fuspyl.step")

# make a sphere
sphere = Part.makeSphere(L*5,FreeCAD.Vector(1,0,0))

# cut heli from sphere
cut = sphere.cut(s)
Part.show(cut)
#cut.exportStep("cut_fuspyl.step")

import ObjectsFem
mesh = ObjectsFem.makeMeshGmsh(FreeCAD.ActiveDocument, 'FEMMeshGmsh')
mesh.ElementDimension = 3
FreeCAD.ActiveDocument.ActiveObject.Part = FreeCAD.ActiveDocument.Shape

mr_fus = ObjectsFem.makeMeshRegion(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, 5.0, 'fus')
mr_outer = ObjectsFem.makeMeshRegion(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, 20.0, 'outer')

mg_fus = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_fus')
mg_outer= ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_outer')
mg_vol = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_vol')

temp = []
for i in range(2,len(App.ActiveDocument.Shape.Shape.Faces)):
    temp.append((App.ActiveDocument.Shape, 'Face' + str(i)))

mr_fus.References = temp
mg_fus.References = temp
mr_outer.References = (App.ActiveDocument.Shape, 'Face1')
mg_outer.References = (App.ActiveDocument.Shape, 'Face1')
mg_vol.References = (App.ActiveDocument.Shape, 'Solid1')

import femmesh.gmshtools as gmshtools
gmsh_mesh = gmshtools.GmshTools(mesh)
gmsh_mesh.create_mesh()

#print(str(FreeCAD.ActiveDocument.FEMMeshGmsh.FemMesh))

import modifygeo
modifygeo.modifygeo("fuspyl")
modifygeo.factor_core("fuspyl")
modifygeo.factor_interior("fuspyl")
modifygeo.factor_dirichlet("fuspyl")
modifygeo.factor_wall("fuspyl")

#doc.removeObject("Shape")
