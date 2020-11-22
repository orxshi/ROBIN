import shutil

def modifygeo(name, shapename, cx, cy, cz):
    shutil.copyfile('/tmp/shape2mesh.geo', '/home/orhan/ROBIN/' + name + '.geo')
    #shutil.copyfile('/tmp/Cut_Geometry.brep', '/home/orhan/ROBIN/' + name + '.brep')
    brep = '/tmp/' + shapename + '_Geometry.brep'
    shutil.copyfile(brep, '/home/orhan/ROBIN/' + name + '.brep')

    with open(name + '.geo', 'r') as file :
      filedata = file.readlines()

    filedata = [line for line in filedata if not 'SaveAll' in line]
    filedata = [line for line in filedata if not 'Save' in line]
    filedata = [line for line in filedata if not 'Mesh  3' in line]
    filedata = [line for line in filedata if not 'Coherence' in line]

    for i, line in enumerate(filedata):
        if 'Mesh.Format' in line:
            filedata[i] = 'Mesh.Format = 1;\n'
        if 'Order' in line:
            filedata[i] = 'Mesh.ElementOrder = 1;\n'
        if 'Save' in line:
            filedata[i] =  "Save \"" + name + ".msh\";"
        if 'Merge' in line:
            filedata[i] =  "Merge \"" + name + ".brep\";\n"
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

    filedata.append('Mesh.MshFileVersion = 2.2;\n\n')

    filedata.append('lc = 1;\n')
    filedata.append('Field[1] = Distance;\n')
    if shapename == 'Cut':
        filedata.append('Field[1].FacesList = {' + matches[0] + '};\n')
        filedata.append('Field[1].NNodesByEdge = 100;\n')
    elif shapename == 'Box':
        filedata.append('Point(111)={' + str(cx) + ', ' + str(cy) + ', ' + str(cz) + '};\n')
        filedata.append('Field[1].NodesList = {111};\n')
    filedata.append('Field[2] = MathEval;\n')
    filedata.append('Field[2].F = Sprintf("F1/3 + %g", lc / 1000);\n')
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
