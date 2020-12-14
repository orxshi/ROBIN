import shutil
import os

def modifygeo(name, shapename, cx, cy, cz):
    shutil.copyfile('/tmp/shape2mesh.geo', '/home/orhan/ROBIN/' + name + '.geoo')
    #shutil.copyfile('/tmp/Cut_Geometry.brep', '/home/orhan/ROBIN/' + name + '.brep')
    brep = '/tmp/' + shapename + '_Geometry.brep'
    shutil.copyfile(brep, '/home/orhan/ROBIN/' + name + '.brep')

    with open(name + '.geoo', 'r') as inFile, open(name + '.geo', 'w') as outFile:
        for line in inFile:
            if line.strip():
                outFile.write(line)

    os.remove(name + '.geoo')

    with open(name + '.geo', 'r') as file :
        filedata = file.readlines()

    filedata = [line for line in filedata if not 'SaveAll' in line]
    filedata = [line for line in filedata if not 'Save' in line]
    filedata = [line for line in filedata if not 'Mesh  3' in line]
    filedata = [line for line in filedata if not 'Coherence' in line]
    filedata = [line for line in filedata if not 'Mesh.CharacteristicLengthMin' in line]
    filedata = [line for line in filedata if not 'Mesh.CharacteristicLengthMax' in line]
    filedata = [line for line in filedata if not 'Mesh.Optimize' in line]
    filedata = [line for line in filedata if not 'Mesh.OptimizeNetgen' in line]
    filedata = [line for line in filedata if not 'Mesh.High' in line]
    filedata = [line for line in filedata if not 'Geometry.Tolerance' in line]
    filedata = [line for line in filedata if not '//' in line]

    for i, line in enumerate(filedata):
        #if 'Mesh.CharacteristicLengthMin =' in line:
            #filedata[i] = 'Mesh.CharacteristicLengthMin = 0.005;\n'
        if 'Mesh.Format' in line:
            filedata[i] = 'Mesh.Format = 1;\n'
        if 'Mesh.Algorithm =' in line:
            filedata[i] = 'Mesh.Algorithm = 1;\n'
        if 'Mesh.Algorithm3D =' in line:
            filedata[i] = 'Mesh.Algorithm3D = 10;\n'
        if 'ElementOrder' in line:
            filedata[i] = 'Mesh.ElementOrder = 1;\n'
        if 'Save' in line:
            filedata[i] =  "Save \"" + name + ".msh\";"
        if 'Merge' in line:
            filedata[i] =  "Merge \"" + name + ".brep\";\n\n"
        if 'mg_fus' in line:
            if shapename == 'Cut':
                import re
                regex = r"\{(.*?)\}"
                matches = re.findall(regex, line, re.MULTILINE | re.DOTALL)
            filedata[i] = filedata[i].replace("\"mg_fus\"", "1")
        if 'mg_wing' in line:
            if shapename == 'Cut':
                import re
                regex = r"\{(.*?)\}"
                matches = re.findall(regex, line, re.MULTILINE | re.DOTALL)
            filedata[i] = filedata[i].replace("\"mg_wing\"", "1")
        #if 'mg_outer' in line:
            #filedata[i] = filedata[i].replace("\"mg_outer\"", "2")
        if 'mg_farfield' in line:
            filedata[i] = filedata[i].replace("\"mg_farfield\"", "9")
        if 'mg_interog' in line:
            filedata[i] = filedata[i].replace("\"mg_interog\"", "11")
        if 'mg_vol' in line:
            filedata[i] = filedata[i].replace("\"mg_vol\"", "4")
            filedata[i] = filedata[i] + '\n'

    filedata.append('Mesh.MshFileVersion = 2.2;\n')
    filedata.append('Mesh.MeshSizeExtendFromBoundary = 0;\n')
    filedata.append('Mesh.RandomFactor = 1e-6;\n\n')

    filedata.append('lc = 0.0025;\n')
    filedata.append('Field[1] = Distance;\n')
    if shapename == 'Cut':
        filedata.append('Field[1].SurfacesList = {' + matches[0] + '};\n')
        filedata.append('Field[1].NumPointsPerCurve = 200;\n')
    elif shapename == 'Box':
        filedata.append('Point(111)={' + str(cx) + ', ' + str(cy) + ', ' + str(cz) + '};\n')
        filedata.append('Field[1].NodesList = {111};\n')
    filedata.append('Field[2] = MathEval;\n')
    filedata.append('Field[2].F = Sprintf("F1/5 + %g", lc);\n')
    filedata.append('Background Field = 2;\n')

    # Write the file out again
    with open(name + '.geo', 'w') as file:
        for line in filedata:
            file.write(line)


def factor_core(name):
    shutil.copyfile(name + '.geo', name + '_core.geo')

    with open(name + '_core.geo', 'r') as file :
      filedata = file.readlines()

    filedata = [line for line in filedata if not 'Physical' in line]

    # Write the file out again
    with open(name + '_core.geo', 'w') as file:
        for line in filedata:
            file.write(line)


def factor_interior(name):
    newname = name + '_interior.geo'
    shutil.copyfile(name + '.geo', newname)

    with open(newname, 'r') as file :
      filedata = file.readlines()

    filedata = [line for line in filedata if 'Physical Volume' in line]

    with open(newname, 'w+') as file :
        file.write("Include \"" + name + "_core.geo\";\n")
        for line in filedata:
            file.write(line)


def factor_dirichlet(name):
    newname = name + '_dirichlet.geo'
    shutil.copyfile(name + '.geo', newname)

    with open(newname, 'r') as file :
      filedata = file.readlines()

    filedata = [line for line in filedata if 'Physical Surface(2)' in line]

    with open(newname, 'w+') as file :
        file.write("Include \"" + name + "_core.geo\";\n")
        for line in filedata:
            file.write(line)


def factor_wall(name):
    newname = name + '_wall.geo'
    shutil.copyfile(name + '.geo', newname)

    with open(newname, 'r') as file :
      filedata = file.readlines()

    filedata = [line for line in filedata if 'Physical Surface(1)' in line]

    with open(newname, 'w+') as file :
        file.write("Include \"" + name + "_core.geo\";\n")
        for line in filedata:
            file.write(line)


def factor_interog(name):
    newname = name + '_interog.geo'
    shutil.copyfile(name + '.geo', newname)

    with open(newname, 'r') as file :
        filedata = file.readlines()

    filedata = [line for line in filedata if 'Physical Surface(2)' in line]
    for i, line in enumerate(filedata):
        if 'Physical Surface(2)' in line:
            filedata[i] = filedata[i].replace("Physical Surface(2)", "Physical Surface(11)")

    with open(newname, 'w+') as file :
        file.write("Include \"" + name + "_core.geo\";\n")
        for line in filedata:
            file.write(line)


def factor_farfield(name):
    newname = name + '_farfield.geo'
    shutil.copyfile(name + '.geo', newname)

    with open(newname, 'r') as file :
        filedata = file.readlines()

    filedata = [line for line in filedata if 'Physical Surface(2)' in line]
    for i, line in enumerate(filedata):
        if 'Physical Surface(2)' in line:
            filedata[i] = filedata[i].replace("Physical Surface(2)", "Physical Surface(9)")

    with open(newname, 'w+') as file :
        file.write("Include \"" + name + "_core.geo\";\n")
        for line in filedata:
            file.write(line)
