def modifygeo(name):
    import shutil
    shutil.copyfile('/tmp/shape2mesh.geo', '/home/orhan/ROBIN/' + name + '.geo')

    with open(name + '.geo', 'r') as file :
      filedata = file.readlines()

    filedata = [line for line in filedata if not 'SaveAll' in line]

    for i, line in enumerate(filedata):
        if 'Mesh.Format' in line:
            filedata[i] = 'Mesh.Format = 1;\n'
        if 'Save' in line:
            filedata[i] =  "Save \"" + name + ".msh\";"
        if 'mg_fus' in line:
            filedata[i] = filedata[i].replace("\"mg_fus\"", "1")
        if 'mg_wing' in line:
            filedata[i] = filedata[i].replace("\"mg_wing\"", "1")
        if 'mg_outer' in line:
            filedata[i] = filedata[i].replace("\"mg_outer\"", "2")
        if 'mg_vol' in line:
            filedata[i] = filedata[i].replace("\"mg_vol\"", "1")

    for i, line in enumerate(filedata):
        if 'Save' in line:
            filedata.insert(i-1, 'Mesh.MshFileVersion = 2.2;\n');
            break

    # Write the file out again
    with open(name + '.geo', 'w') as file:
        for line in filedata:
            file.write(line)
