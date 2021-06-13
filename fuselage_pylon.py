# Reference 1: Mineck, Raymond E. Steady and periodic pressure measurements on a generic helicopter fuselage model in the presence of a rotor. NASA Langley Research Center, 2000.
# Reference 2: Shibliyev, Orxan, and Ibrahim Sezai. "Overset Grid Assembler and Flow Solver with Adaptive Spatial Load Balancing." Applied Sciences 11.11 (2021): 5132.

# Some of coefficients [C1,...,C8] in Reference 1 are modified since the original coefficients do not produce the expected output.
# In appendix of Reference 2, some of the coefficients are modified.
# Coefficients in coef_fuselage.py and coef_pylon.py are taken from Reference 2.

# Some numbers might seem weird such as 0.001 and not 0.
# This is needed, otherwise, code fails due to division by zero.

import sys
import math
import numpy
import Part
import BOPTools.JoinAPI
from mesh import *
from coef_fuselage import *
from coef_pylon import *
from make_component import *
from constant import *
from modify_geo import *

# Make a new document in FreeCAD.
doc = FreeCAD.newDocument('newdoc')

# Parameters
fuselage_start = 0.001 # fuselage head x-coordinate.
fuselage_end = 1.997 # fuselage tail x-coordinate.
pylon_start = 0.40001 # pylon head x-coordinate.
pylon_end = 1.018 # pylon tail x-coordinate.
radial_start = 0.00001 # starting radial coordinate along a cross-section.
nx_fuselage = 10 # number of points along x-direction on fuselage.
nx_pylon = 10 # number of points along x-direction on pylon.
np = 10 # number of points along a cross-section.
L_inch = 78.57 # length of fuselage in inches.
L = L_inch * INCH_TO_METER / fuselage_end # normalized length of fuselage in meters.
dia = 50 # diameter of the sphere to be used for meshing.

# ----------------------------------------------------

px_fuselage = numpy.linspace(fuselage_start, fuselage_end, nx_fuselage) # a list of x-coordinates along the fuselage.
px_pylon = numpy.linspace(pylon_start, pylon_end, nx_pylon) # a list of x-coordinates along the pylon.
pr = numpy.linspace(radial_start, 2.0*math.pi, np) # a list of radial coordinates along a cross-section.

fuselage = make_component(Fuselage, px_fuselage, pr, L) # make fuselage.
pylon = make_component(Pylon, px_pylon, pr, L) # make pylon.

# Connect fuselage and pylon.
helicopter = BOPTools.JoinAPI.connect([fuselage, pylon])

# Make the connected components a solid.
solid_helicopter = Part.Solid(helicopter)

# Make a sphere to be cut with the main body.
sphere = Part.makeSphere(dia,FreeCAD.Vector(1,0,0))

# Cut helicopter from the sphere.
cut = sphere.cut(solid_helicopter)

# Define the cut as FreeCAD object.
cut_object = doc.addObject("Part::Feature","Cut")
cut_object.Shape = cut

# Mesh the cut object.
mesh(cut_object, 'main_body', doc)

# Modify geo files to our needs.
file_name = "fuselage_pylon"
modify_geo(file_name, 'Cut')

# Some useful commands:
Part.show(helicopter)
# s.exportStep("filename.step")
