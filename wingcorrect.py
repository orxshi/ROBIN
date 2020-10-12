import sys
import math
import numpy
import modifygeo
import FreeCAD
import Draft
import Part
import BOPTools.JoinFeatures
import ObjectsFem

sys.path.append('/usr/lib/freecad/lib/')
INCH_TO_M = 0.0254


doc = App.newDocument('newdoc')

def makecylinder(rad, pos, ext_dir):
    cylinder = Part.makeCylinder(rad, cyl_length, pos, ext_dir)
    return cylinder


chord = 2.61 * INCH_TO_M
thick = 12 / 100;
twist = 8;
wing_radius = 33.88 * INCH_TO_M
root_cut_out = 0.24 * wing_radius 
wing_z_start = 0
wing_z_end = wing_radius - root_cut_out

print("root_cut_out:", root_cut_out)
print("wing_z_end:", wing_z_end)

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

points = []
for i in range(len(x)):
    points.append(App.Vector(x[i], y(x[i]), wing_z_start))
for i in reversed(range(1, len(x)-1)):
    points.append(App.Vector(x[i], -y(x[i]), wing_z_start))
points.append(points[0])


def makewing(points):
    polygon = Part.makePolygon(points)
    #Part.show(polygon)

    polygon2 = Part.makePolygon(points)
    mat = polygon2.Placement.toMatrix()
    mat.rotateZ(-twist * math.pi / 180)
    mat.move(App.Vector(0,0,wing_z_end))
    polygon2.Placement = App.Placement(mat)

    #face = Part.Face(polygon)
    #wing = face.extrude(App.Vector(0,0,wing_z_end))
    wing = Part.makeLoft([polygon, polygon2], True)
    return wing


# make 4 wings
wings = [makewing(points) for _ in range(4)]

#
rot = App.Rotation(App.Vector(1,0,0), 90)
centre = App.Vector(0.5, 0, 0.05)
pos = App.Vector(0, 0, 0)

#fuslen = 78.57 * INCH_TO_M
fuslen = 78.57 * INCH_TO_M / 1.997

boxlen = 100
#fuslen = 1.99898
halffuswidthy = 0.125 * fuslen
halffuswidthz = 0.197 * fuslen
#wing_z_height = 0.13 * fuslen
wing_z_height = 0.322 * fuslen
cyl_wing_diff = wing_z_end / 5
#cyl_length = wing_z_end + cyl_wing_diff
cyl_length = chord * 10 * 2
#cyl_length = chord * 100 * 2
#pyl_x = (0.4 + 1.018) * fuslen / 4
pyl_x = 0.696 * fuslen
off_front_wing = halffuswidthy / 2
off_side_wing = halffuswidthy / 2
cyl_rad = chord * 10
#cyl_rad = chord * 100

print('cnt(0):', pyl_x)
print('cnt(1):', 0)
print('cnt(2):', wing_z_height)

cylinders = []

# reposition wings[0]
mat = wings[0].Placement.toMatrix()
mat.rotateX(math.pi/2)
mat.move(App.Vector(pyl_x-chord/2, wing_radius, wing_z_height))
wings[0].Placement = App.Placement(mat)
mattemp = wings[0].Placement.toMatrix()
mat = wings[0].Placement.toMatrix()
cylinder = makecylinder(cyl_rad, App.Vector(mat.A14+chord/2, mat.A24 + cyl_length/2 - wing_z_end/2, wing_z_height), App.Vector(0,-1,0))
cylinders.append(cylinder)

# reposition wings[1]
mat = wings[1].Placement.toMatrix()
mat.rotateZ(math.pi/2)
mat.rotateY(-math.pi/2)
mat.move(App.Vector(pyl_x - root_cut_out, -chord/2, wing_z_height))
wings[1].Placement = App.Placement(mat)
cylinder = makecylinder(cyl_rad, App.Vector(mat.A14+cyl_length/2 - wing_z_end/2, mat.A24+chord/2, wing_z_height), App.Vector(-1,0,0))
cylinders.append(cylinder)

# reposition wings[2]
wings[2] = wings[0].copy()
mat = wings[0].Placement.toMatrix()
mat.rotateY(math.pi)
mat.A24 = -(mat.A24 - wing_z_end)
mat.A14 = wings[0].Placement.toMatrix().A14 + chord
mat.A34 = wings[0].Placement.toMatrix().A34
wings[2].Placement = App.Placement(mat)
cylinder = makecylinder(cyl_rad, App.Vector(mat.A14-chord/2, mat.A24 - cyl_length/2 - wing_z_end/2, wing_z_height), App.Vector(0,1,0))
cylinders.append(cylinder)

# reposition wings[3]
wings[3] = wings[1].copy()
mat = wings[1].Placement.toMatrix()
mat.rotateX(math.pi)
mat.A24 = wings[1].Placement.toMatrix().A24 + chord
mat.A34 = wings[1].Placement.toMatrix().A34
mat.A14 = pyl_x + wing_radius
wings[3].Placement = App.Placement(mat)
cylinder = makecylinder(cyl_rad, App.Vector(mat.A14-cyl_length/2-wing_z_end/2, mat.A24-chord/2, wing_z_height), App.Vector(1,0,0))
cylinders.append(cylinder)

Part.show(wings[0])
Part.show(wings[1])
Part.show(wings[2])
Part.show(wings[3])

wings[0].exportStep("wing0.step")
wings[1].exportStep("wing1.step")
wings[2].exportStep("wing2.step")
wings[3].exportStep("wing3.step")

Part.show(cylinders[0])
Part.show(cylinders[1])
Part.show(cylinders[2])
Part.show(cylinders[3])

box = Part.makeBox(boxlen, boxlen, boxlen, App.Vector(pyl_x-boxlen/2, 0-boxlen/2, wing_z_height-boxlen/2))
#Part.show(box)


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


def meshwing(cylinder, wing, tag):
    cut = cylinder.cut(wing)
    cut_object = doc.addObject("Part::Feature","Cut")
    cut_object.Shape = cut
    if not cut_object:
        cut_object.ViewObject.Transparency = 50

    mesh = ObjectsFem.makeMeshGmsh(doc, 'FEMMeshGmsh')
    mesh.Part = cut_object

    mg_wing = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_wing')
    mg_interog = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_interog')
    mg_vol = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_vol')

    temp = []
    for i in range(4,len(cut_object.Shape.Faces)+1):
        temp.append((cut_object, 'Face' + str(i)))

    mg_wing.References = temp

    temp = []
    for i in range(1,4):
        temp.append((cut_object, 'Face' + str(i)))

    mg_interog.References = temp
    mg_vol.References = (cut_object, 'Solid1')

    import femmesh.gmshtools as gmshtools
    gmsh_mesh = gmshtools.GmshTools(mesh)
    gmsh_mesh.create_mesh()

    doc.removeObject("Cut")
    doc.removeObject("FEMMeshGmsh")
    doc.removeObject("mg_wing")
    doc.removeObject("mg_interog")
    doc.removeObject("mg_vol")
    doc.recompute()


for i in range(4):

    fn = "wing" + str(i)

    meshwing(cylinders[i], wings[i], i)
    modifygeo.modifygeo(fn, 'Cut', pyl_x, 0, wing_z_height)
    #modifygeo.factor_core(fn)
    #modifygeo.factor_interior(fn)
    #modifygeo.factor_interog(fn)
    #modifygeo.factor_farfield(fn)
    #modifygeo.factor_wall(fn)

#meshbox()
#modifygeo.modifygeo("box", 'Box', pyl_x, 0, wing_z_height)
#modifygeo.factor_core("box")
#modifygeo.factor_interior("box")
#modifygeo.factor_farfield("box")
