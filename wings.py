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

chord = 2.61
thick = 12 * chord / 100;

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
wing_z_end = 33.88
points = []
for i in range(len(x)):
    points.append(FreeCAD.Vector(x[i], y(x[i]), wing_z_start))
for i in reversed(range(len(x)-1)):
    points.append(FreeCAD.Vector(x[i], -y(x[i]), wing_z_start))


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

fuslen = 78.70
halffuswidthy = 0.125 * fuslen
halffuswidthz = 0.197 * fuslen
wing_z_height = 0.13 * fuslen
cyl_wing_diff = wing_z_end / 5
cyl_length = wing_z_end + cyl_wing_diff
pyl_x = (0.4 + 1.018) * fuslen / 4
off_front_wing = halffuswidthy / 2
off_side_wing = halffuswidthy / 2
cyl_rad = chord * 3

cylinders = []

# reposition wings[0]
mat = wings[0].Placement.toMatrix()
mat.rotateX(math.pi/2)
mat.move(FreeCAD.Vector(pyl_x-chord/2, wing_z_end+off_side_wing, wing_z_height))
wings[0].Placement = FreeCAD.Placement(mat)

#Part.show(wings[0])
cylinder = makecylinder(cyl_rad, FreeCAD.Vector(mat.A14+chord/2, mat.A24+cyl_wing_diff/2, wing_z_height), FreeCAD.Vector(0,-1,0))
cylinders.append(cylinder)
#Part.show(cylinder)

# reposition wings[1]
mat = wings[1].Placement.toMatrix()
mat.rotateZ(math.pi/2)
mat.rotateY(-math.pi/2)
mat.move(FreeCAD.Vector(pyl_x-off_front_wing,-chord/2,wing_z_height))
wings[1].Placement = FreeCAD.Placement(mat)

#Part.show(wings[1])
cylinder = makecylinder(cyl_rad, FreeCAD.Vector(mat.A14+cyl_wing_diff/2, mat.A24+chord/2, wing_z_height), FreeCAD.Vector(-1,0,0))
cylinders.append(cylinder)
#Part.show(cylinder)

# reposition wings[2]
wings[2] = wings[0].copy()
mat = wings[0].Placement.toMatrix()
mat.rotateY(math.pi)
mat.A24 = -(mat.A24 - wing_z_end)
mat.A14 = wings[0].Placement.toMatrix().A14 + chord
mat.A34 = wings[0].Placement.toMatrix().A34
wings[2].Placement = FreeCAD.Placement(mat)

#Part.show(wings[2])
cylinder = makecylinder(cyl_rad, FreeCAD.Vector(mat.A14-chord/2, mat.A24-cyl_wing_diff/2-wing_z_end, wing_z_height), FreeCAD.Vector(0,1,0))
cylinders.append(cylinder)
#Part.show(cylinder)

# reposition wings[3]
wings[3] = wings[1].copy()
mat = wings[1].Placement.toMatrix()
mat.rotateX(math.pi)
mat.A24 = wings[1].Placement.toMatrix().A24 + chord
mat.A34 = wings[1].Placement.toMatrix().A34
mat.A14 = pyl_x + wing_z_end + off_front_wing
wings[3].Placement = FreeCAD.Placement(mat)

#Part.show(wings[3])
cylinder = makecylinder(cyl_rad, FreeCAD.Vector(mat.A14-cyl_wing_diff/2-wing_z_end, mat.A24-chord/2, wing_z_height), FreeCAD.Vector(1,0,0))
cylinders.append(cylinder)
#Part.show(cylinder)

#
wings[0].exportStep("wing0.step")
wings[1].exportStep("wing1.step")
wings[2].exportStep("wing2.step")
wings[3].exportStep("wing3.step")


def makerest(cylinder, wing, tag):
    cut = cylinder.cut(wing)
    Part.show(cut)
    cut.exportStep("cut_wing" + str(tag) + ".step")

    import ObjectsFem
    mesh = ObjectsFem.makeMeshGmsh(FreeCAD.ActiveDocument, 'FEMMeshGmsh')
    mesh.ElementDimension = 3
    FreeCAD.ActiveDocument.ActiveObject.Part = FreeCAD.ActiveDocument.Shape

    mr_wing = ObjectsFem.makeMeshRegion(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, 1.0, 'mr_wing')
    mr_outer = ObjectsFem.makeMeshRegion(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, 5.0, 'mr_outer')

    mg_wing = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_wing')
    mg_outer= ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_outer')
    mg_vol = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, FreeCAD.ActiveDocument.FEMMeshGmsh, False, 'mg_vol')

    temp = []
    for i in range(4,len(App.ActiveDocument.Shape.Shape.Faces)):
        temp.append((App.ActiveDocument.Shape, 'Face' + str(i)))

    mr_wing.References = temp
    mg_wing.References = temp

    temp = []
    for i in range(1,4):
        temp.append((App.ActiveDocument.Shape, 'Face' + str(i)))

    mr_outer.References = temp
    mg_outer.References = temp
    mg_vol.References = (App.ActiveDocument.Shape, 'Solid1')

    import femmesh.gmshtools as gmshtools
    gmsh_mesh = gmshtools.GmshTools(mesh)
    gmsh_mesh.create_mesh()

    print(str(FreeCAD.ActiveDocument.FEMMeshGmsh.FemMesh))

    doc.removeObject("Shape")
    doc.removeObject("FEMMeshGmsh")
    doc.removeObject("mr_wing")
    doc.removeObject("mr_outer")
    doc.removeObject("mg_wing")
    doc.removeObject("mg_outer")
    doc.removeObject("mg_vol")
    doc.recompute()



import modifygeo

makerest(cylinders[0], wings[0], 0)
modifygeo.modifygeo("wing0")
modifygeo.factor_core("wing0")
modifygeo.factor_interior("wing0")
modifygeo.factor_dirichlet("wing0")
modifygeo.factor_wall("wing0")

makerest(cylinders[1], wings[1], 1)
modifygeo.modifygeo("wing1")
modifygeo.factor_core("wing1")
modifygeo.factor_interior("wing1")
modifygeo.factor_dirichlet("wing1")
modifygeo.factor_wall("wing1")

makerest(cylinders[2], wings[2], 2)
modifygeo.modifygeo("wing2")
modifygeo.factor_core("wing2")
modifygeo.factor_interior("wing2")
modifygeo.factor_dirichlet("wing2")
modifygeo.factor_wall("wing2")

makerest(cylinders[3], wings[3], 3)
modifygeo.modifygeo("wing3")
modifygeo.factor_core("wing3")
modifygeo.factor_interior("wing3")
modifygeo.factor_dirichlet("wing3")
modifygeo.factor_wall("wing3")
