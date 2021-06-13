import math
import FreeCAD
import Part

def reposition_blade(ref_blade, blade, index, blade_radius, hub_center, chord):
    if index == 0:
        mat = ref_blade.Placement.toMatrix()
        mat.rotateX(math.pi/2)
        mat.move(FreeCAD.Vector(hub_center[0]-chord/2, blade_radius, hub_center[2]))
        blade.Placement = FreeCAD.Placement(mat)
        mat = blade.Placement.toMatrix()
    elif index == 1:
        mat = ref_blade.Placement.toMatrix()
        mat.rotateY(math.pi/2)
        mat.rotateX(math.pi/2)
        mat.move(FreeCAD.Vector(0, -chord/2, hub_center[2]))
        blade.Placement = FreeCAD.Placement(mat)
        mat = blade.Placement.toMatrix()
        mat.A14 = hub_center[0] - blade_radius
        blade.Placement = FreeCAD.Placement(mat)
    elif index == 2:
        mat = ref_blade.Placement.toMatrix()
        mat.rotateX(math.pi)
        mat.rotateY(math.pi)
        mat.A24 = 0 - blade_radius
        mat.A14 = ref_blade.Placement.toMatrix().A14 + chord
        mat.A34 = ref_blade.Placement.toMatrix().A34
        blade.Placement = FreeCAD.Placement(mat)
    elif index == 3:
        mat = ref_blade.Placement.toMatrix()
        mat.rotateY(math.pi)
        mat.rotateX(math.pi)
        mat.A24 = ref_blade.Placement.toMatrix().A24 + chord
        mat.A34 = ref_blade.Placement.toMatrix().A34
        mat.A14 = hub_center[0] + blade_radius
        blade.Placement = FreeCAD.Placement(mat)

    return mat

def makecylinder(rad, pos, ext_dir, cyl_length):
    cylinder = Part.makeCylinder(rad, cyl_length, pos, ext_dir)
    return cylinder


def make_cylinder(index, cyl_rad, chord, cyl_length, blade_length, hub_center_z, mat):
    if index == 0:
        cylinder = makecylinder(cyl_rad, FreeCAD.Vector(mat.A14+chord/2, mat.A24 + cyl_length/2 - blade_length/2, hub_center_z), FreeCAD.Vector(0,-1,0), cyl_length)
    elif index == 1:
        cylinder = makecylinder(cyl_rad, FreeCAD.Vector(mat.A14 + cyl_length/2 + blade_length/2, mat.A24+chord/2, hub_center_z), FreeCAD.Vector(-1,0,0), cyl_length)
    elif index == 2:
        cylinder = makecylinder(cyl_rad, FreeCAD.Vector(mat.A14-chord/2, mat.A24 - blade_length/2, hub_center_z), FreeCAD.Vector(0,1,0), cyl_length)
    elif index == 3:
        cylinder = makecylinder(cyl_rad, FreeCAD.Vector(mat.A14-cyl_length/2-blade_length/2, mat.A24-chord/2, hub_center_z), FreeCAD.Vector(1,0,0), cyl_length)

    return cylinder


def make_blade(points, aoa, twist, blade_length):
    # Create a face of blade.
    polygon = Part.makePolygon(points)
    mat = polygon.Placement.toMatrix()
    mat.rotateZ(-(aoa) * math.pi / 180)
    polygon.Placement = FreeCAD.Placement(mat)

    # Create another face of blade with twist.
    polygon2 = Part.makePolygon(points)
    mat = polygon2.Placement.toMatrix()
    mat.rotateZ(-(twist+aoa) * math.pi / 180)
    mat.move(FreeCAD.Vector(0,0,blade_length))
    polygon2.Placement = FreeCAD.Placement(mat)

    loft = Part.makeLoft([polygon, polygon2], True)
    return loft


def make_hub_shaft(points, aoa, twist):
    # The four connecting shafts of the hub are of the same profile (NACA 0012) as the blades.

    # Create a face of hub shaft.
    polygon = Part.makePolygon(points)
    mat = polygon.Placement.toMatrix()
    mat.rotateZ(-(twist+aoa) * math.pi / 180)
    polygon.Placement = App.Placement(mat)

    # Create another face of hub shaft.
    polygon2 = Part.makePolygon(points)
    mat = polygon2.Placement.toMatrix()
    mat.rotateZ(-(twist+aoa) * math.pi / 180)
    mat.move(App.Vector(0,0,shaft_len))
    polygon2.Placement = App.Placement(mat)

    loft = Part.makeLoft([polygon, polygon2], True)
    return loft
