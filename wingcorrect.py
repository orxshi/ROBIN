import sys
import math
import numpy
import modifygeo

sys.path.append('/usr/lib/freecad/lib/')

import FreeCAD
import Draft
import Part
import BOPTools.JoinFeatures
import ObjectsFem

doc = App.newDocument('newdoc')

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
    points.append(App.Vector(x[i], y(x[i]), wing_z_start))
for i in reversed(range(1, len(x)-1)):
    points.append(App.Vector(x[i], -y(x[i]), wing_z_start))
points.append(points[0])


def makewing(points):
    polygon = Part.makePolygon(points)
    #Part.show(polygon)
    face = Part.Face(polygon)
    #Part.show(face)
    wing = face.extrude(App.Vector(0,0,wing_z_end))
    return wing


# make 4 wings
wings = [makewing(points) for _ in range(4)]
#Part.show(wings[0])

#
rot = App.Rotation(App.Vector(1,0,0), 90)
centre = App.Vector(0.5, 0, 0.05)
pos = App.Vector(0, 0, 0)

boxlen = 500
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
mat.move(App.Vector(pyl_x-chord/2, wing_z_end+off_side_wing, wing_z_height))
wings[0].Placement = App.Placement(mat)
mattemp = wings[0].Placement.toMatrix()
#print('cnt(0):', pyl_x)
#print('cnt(1):', 0)
#print('cnt(2):', wing_z_height)
cylinder = makecylinder(cyl_rad, App.Vector(mat.A14+chord/2, mat.A24+cyl_wing_diff/2, wing_z_height), App.Vector(0,-1,0))
Part.show(cylinder)
cylinders.append(cylinder)

# reposition wings[1]
mat = wings[1].Placement.toMatrix()
mat.rotateZ(math.pi/2)
mat.rotateY(-math.pi/2)
mat.move(App.Vector(pyl_x-off_front_wing,-chord/2,wing_z_height))
wings[1].Placement = App.Placement(mat)
cylinder = makecylinder(cyl_rad, App.Vector(mat.A14+cyl_wing_diff/2, mat.A24+chord/2, wing_z_height), App.Vector(-1,0,0))
Part.show(cylinder)
cylinders.append(cylinder)

# reposition wings[2]
wings[2] = wings[0].copy()
mat = wings[0].Placement.toMatrix()
mat.rotateY(math.pi)
mat.A24 = -(mat.A24 - wing_z_end)
mat.A14 = wings[0].Placement.toMatrix().A14 + chord
mat.A34 = wings[0].Placement.toMatrix().A34
wings[2].Placement = App.Placement(mat)
cylinder = makecylinder(cyl_rad, App.Vector(mat.A14-chord/2, mat.A24-cyl_wing_diff/2-wing_z_end, wing_z_height), App.Vector(0,1,0))
Part.show(cylinder)
cylinders.append(cylinder)

# reposition wings[3]
wings[3] = wings[1].copy()
mat = wings[1].Placement.toMatrix()
mat.rotateX(math.pi)
mat.A24 = wings[1].Placement.toMatrix().A24 + chord
mat.A34 = wings[1].Placement.toMatrix().A34
mat.A14 = pyl_x + wing_z_end + off_front_wing
wings[3].Placement = App.Placement(mat)
cylinder = makecylinder(cyl_rad, App.Vector(mat.A14-cyl_wing_diff/2-wing_z_end, mat.A24-chord/2, wing_z_height), App.Vector(1,0,0))
Part.show(cylinder)
cylinders.append(cylinder)

box = Part.makeBox(boxlen, boxlen, boxlen, App.Vector(pyl_x-boxlen/2, 0-boxlen/2, wing_z_height-boxlen/2))
Part.show(box)


def meshbox():
    obj = doc.addObject("Part::Feature","Box")
    obj.Shape = box

    mesh = ObjectsFem.makeMeshGmsh(doc, 'FEMMeshGmsh')
    mesh.Part = obj

    mg_outer = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_outer')
    mg_vol = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_vol')

    temp = []
    for i in range(1,7):
        temp.append((obj, 'Face' + str(i)))

    mg_outer.References = temp
    mg_vol.References = (obj, 'Solid1')

    import femmesh.gmshtools as gmshtools
    gmsh_mesh = gmshtools.GmshTools(mesh)
    gmsh_mesh.create_mesh()

    doc.removeObject("Box")
    doc.removeObject("FEMMeshGmsh")
    doc.removeObject("mg_outer")
    doc.removeObject("mg_vol")
    doc.recompute()


def makerest(cylinder, wing, tag):
    cut = cylinder.cut(wing)
    cut_object = doc.addObject("Part::Feature","Cut")
    cut_object.Shape = cut
    if not cut_object:
        cut_object.ViewObject.Transparency = 50

    mesh = ObjectsFem.makeMeshGmsh(doc, 'FEMMeshGmsh')
    mesh.Part = cut_object

    mg_wing = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_wing')
    mg_outer = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_outer')
    mg_vol = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_vol')

    temp = []
    for i in range(4,len(cut_object.Shape.Faces)+1):
        temp.append((cut_object, 'Face' + str(i)))

    mg_wing.References = temp

    temp = []
    for i in range(1,4):
        temp.append((cut_object, 'Face' + str(i)))

    mg_outer.References = temp
    mg_vol.References = (cut_object, 'Solid1')

    import femmesh.gmshtools as gmshtools
    gmsh_mesh = gmshtools.GmshTools(mesh)
    gmsh_mesh.create_mesh()

    doc.removeObject("Cut")
    doc.removeObject("FEMMeshGmsh")
    doc.removeObject("mg_wing")
    doc.removeObject("mg_outer")
    doc.removeObject("mg_vol")
    doc.recompute()



for i in range(4):

    fn = "wing" + str(i)

    makerest(cylinders[i], wings[i], i)
    modifygeo.modifygeo(fn, 'Cut', pyl_x, 0, wing_z_height)
    modifygeo.factor_core(fn)
    modifygeo.factor_interior(fn)
    modifygeo.factor_interog(fn)
    modifygeo.factor_wall(fn)

meshbox()
modifygeo.modifygeo("box", 'Box', pyl_x, 0, wing_z_height)
modifygeo.factor_core("box")
modifygeo.factor_interior("box")
modifygeo.factor_farfield("box")
