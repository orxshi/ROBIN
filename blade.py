# Reference 1: Mineck, Raymond E. Steady and periodic pressure measurements on a generic helicopter fuselage model in the presence of a rotor. NASA Langley Research Center, 2000.
# Reference 2: Shibliyev, Orxan, and Ibrahim Sezai. "Overset Grid Assembler and Flow Solver with Adaptive Spatial Load Balancing." Applied Sciences 11.11 (2021): 5132.

# Some of coefficients [C1,...,C8] in Reference 1 are modified since the original coefficients do not produce the expected output.
# In appendix of Reference 2, some of the coefficients are modified.
# Coefficients in coef_fuselage.py and coef_pylon.py are taken from Reference 2.

# Some numbers might seem weird such as 0.001 and not 0.
# This is needed, otherwise, code fails due to division by zero.

import sys
import numpy
import BOPTools.JoinAPI
from mesh import *
from make_component import *
from constant import *
from modify_geo import *
from NACA0012 import *
from blade_helper import *

# Make a new document in FreeCAD.
doc = App.newDocument('newdoc')

# Parameters
fuselage_end = 1.997 # fuselage tail x-coordinate.
L_inch = 78.57 # length of fuselage in inches.
L = L_inch * INCH_TO_METER / fuselage_end # normalized length of fuselage in meters.
chord_inch = 2.61 # chord length of blade in inches.
chord = chord_inch * INCH_TO_METER
aoa = 4; # angle of attack in degrees.
twist = 8; # twist angle in degrees.
blade_radius_inch = 33.88 # length from the center of hub to the end of blade without root cut out.
blade_radius = blade_radius_inch * INCH_TO_METER
root_cut_out = 0.24 * blade_radius 
blade_length = blade_radius - root_cut_out
nx = 10; # number of points on airfoil profile.
hub_center = [0.696 * L, 0, 0.322 * L]
cylinder_radius = chord * 10
cylinder_length = cylinder_radius * 2

# ----------------------------------------------------

# Make points of NACA0012 profile.
x = numpy.linspace(0.00001, chord, nx)
points = make_NACA0012_points(x, chord)

# Make 4 blades.
blade = [make_blade(points, aoa, twist, blade_length) for _ in range(4)]

# Make 4 meshes.
for i in range(4):

    # Positions of 1st and 2nd blades will be used as reference for 3rd and 4th blades.
    if i == 0 or i == 2:
        ref_blade = blade[0]
    if i == 1 or i == 3:
        ref_blade = blade[1]

    # Bring each blade to correct positions.
    pos = reposition_blade(ref_blade, blade[i], i, blade_radius, hub_center, chord)

    # Define the blades as FreeCAD object.
    blade_object = doc.addObject("Part::Feature","Blade"+str(i))
    blade_object.Shape = blade[i]

    # Make a cylinder for each blade.
    cylinder = make_cylinder(i, cylinder_radius, chord, cylinder_length, blade_length, hub_center[2], pos)

    # Cut blade from the cylinder.
    cut = cylinder.cut(blade)

    # Define the cut as FreeCAD object.
    cut_object = doc.addObject("Part::Feature","Cut" + str(i))
    cut_object.Shape = cut

    # Mesh the cut object.
    mesh(cut_object, 'blade', doc)

    # Modify geo files to our needs.
    file_name = "blade" + str(i)
    modify_geo(file_name, 'Cut', hub_center)
