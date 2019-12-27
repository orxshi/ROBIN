import sys
import math
import numpy

sys.path.append('/usr/lib/freecad/lib/')

import FreeCAD
import Draft
import Part
import BOPTools.JoinFeatures

doc = FreeCAD.newDocument('newdoc')

def makecylinder(rad, pos, ext_dir):
    cylinder = Part.makeCylinder(rad, cyl_length, pos, ext_dir)
    return cylinder

chord = 1
thick = 12 * chord / 100;
scale = 0.2

def y(x):
    C1 = 0.2969
    C2 = 0.1260
    C3 = 0.3516
    C4 = 0.2843
    C5 = 0.1036
    xc = x / chord
    y = thick * chord / 0.2 * (C1 * xc**(1/2) - C2 * xc**(1) - C3 * xc**(2) + C4 * xc**(3) - C5 * xc**(4))
    return y

nx = 10;
x = numpy.linspace(0, chord, nx)

wing_z_start = 0
wing_z_end = 1.5
points = []
for i in range(len(x)):
    points.append(FreeCAD.Vector(scale*x[i], scale*y(x[i]), wing_z_start))
for i in reversed(range(len(x)-1)):
    points.append(FreeCAD.Vector(scale*x[i], -scale*y(x[i]), wing_z_start))


def makewing(points):
    polygon = Part.makePolygon(points)
    face = Part.Face(polygon)
    #Part.show(face)
    wing = face.extrude(FreeCAD.Vector(0,0,wing_z_end))
    return wing


# make 4 wings
wings = [makewing(points) for _ in range(4)]

#
rot = FreeCAD.Rotation(FreeCAD.Vector(1,0,0), 90)
centre = FreeCAD.Vector(0.5, 0, 0.05)
pos = FreeCAD.Vector(0, 0, 0)

wing_z_height = 0.3
cyl_wing_diff = 1
cyl_length = wing_z_end + cyl_wing_diff
pyl_x = 0.7
off_front_wing = 0.2

# reposition wings[0]
mat = wings[0].Placement.toMatrix()
mat.rotateX(math.pi/2)
mat.move(FreeCAD.Vector(pyl_x-scale*chord/2,wing_z_end+0.2,wing_z_height))
wings[0].Placement = FreeCAD.Placement(mat)

Part.show(wings[0])
cylinder = makecylinder(pyl_x-scale*chord/2, FreeCAD.Vector(mat.A14+scale*chord/2, mat.A24+cyl_wing_diff/2, wing_z_height), FreeCAD.Vector(0,-1,0))
Part.show(cylinder)

# reposition wings[1]
mat = wings[1].Placement.toMatrix()
mat.rotateZ(math.pi/2)
mat.rotateY(-math.pi/2)
mat.move(FreeCAD.Vector(pyl_x-off_front_wing,-0.1,wing_z_height))
wings[1].Placement = FreeCAD.Placement(mat)

Part.show(wings[1])
cylinder = makecylinder(pyl_x-off_front_wing, FreeCAD.Vector(mat.A14+cyl_wing_diff/2, mat.A24+scale*chord/2, wing_z_height), FreeCAD.Vector(-1,0,0))
Part.show(cylinder)

# reposition wings[2]
wings[2] = wings[0].copy()
mat = wings[0].Placement.toMatrix()
mat.rotateY(math.pi)
mat.A24 = -(mat.A24 - wing_z_end)
mat.A14 = wings[0].Placement.toMatrix().A14 + scale * chord
mat.A34 = wings[0].Placement.toMatrix().A34
wings[2].Placement = FreeCAD.Placement(mat)

Part.show(wings[2])
cylinder = makecylinder(pyl_x, FreeCAD.Vector(mat.A14+scale*chord/2, mat.A24-cyl_wing_diff/2, wing_z_height), FreeCAD.Vector(0,1,0))
Part.show(cylinder)

# reposition wings[3]
wings[3] = wings[1].copy()
mat = wings[1].Placement.toMatrix()
mat.rotateX(math.pi)
mat.A24 = wings[1].Placement.toMatrix().A24 + scale * chord
mat.A34 = wings[1].Placement.toMatrix().A34
mat.A14 = pyl_x + wing_z_end + off_front_wing
wings[3].Placement = FreeCAD.Placement(mat)

#
wings[0].exportStep("wing0.step")
wings[1].exportStep("wing1.step")
wings[2].exportStep("wing2.step")
wings[3].exportStep("wing3.step")






def makerest(wing, tag):
    cut = cylinder.cut(wing)
    Part.show(cut)

    import ObjectsFem
    mesh = ObjectsFem.makeMeshGmsh(FreeCAD.ActiveDocument, 'FEMMeshGmsh')
    mesh.ElementDimension = 3
    FreeCAD.ActiveDocument.ActiveObject.Part = FreeCAD.ActiveDocument.Shape002

    mr_wing = ObjectsFem.makeMeshRegion(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, 0.05, 'mr_wing')
    mr_outer = ObjectsFem.makeMeshRegion(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, 0.5, 'mr_outer')

    mg_wing = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_wing')
    mg_outer= ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_outer')
    mg_vol = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_vol')

    temp = []
    for i in range(4,len(App.ActiveDocument.Shape002.Shape.Faces)-2):
        temp.append((App.ActiveDocument.Shape002, 'Face' + str(i)))

    mr_wing.References = temp
    mg_wing.References = temp

    temp = []
    for i in range(1,4):
        temp.append((App.ActiveDocument.Shape002, 'Face' + str(i)))

    mr_outer.References = temp
    mg_outer.References = temp

    mg_vol.References = (App.ActiveDocument.Shape002, 'Solid1')

    import femmesh.gmshtools as gmshtools
    gmsh_mesh = gmshtools.GmshTools(mesh)
    gmsh_mesh.create_mesh()

    print(str(FreeCAD.ActiveDocument.FEMMeshGmsh.FemMesh))

