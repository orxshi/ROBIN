import FreeCAD
import ObjectsFem
import femmesh.gmshtools

def mesh(component, component_name, doc):
    # Create mesh and mesh groups.

    assert component_name == 'main_body' or component_name == 'blade' or component_name == 'hub'

    mesh = ObjectsFem.makeMeshGmsh(doc, 'FEMMeshGmsh')
    mesh.ElementDimension = 3 # mesh is three-dimensional.
    mesh.Part = component;

    # Names of mesh groups to be used by GMSH.
    if component_name == 'blade' or component_name == 'hub':
        mg_interog = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, mesh, False, 'mg_interog')
    else:
        mg_farfield = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, mesh, False, 'mg_farfield')

    mg_wall = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, mesh, False, 'mg_wall')
    mg_volume = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, mesh, False, 'mg_volume')

    # Determine the wall faces of the component.
    wall_faces = []
    if component_name == 'blade' or component_name == 'hub':
        for i in range(4,len(component.Shape.Faces)+1):
            wall_faces.append((component, 'Face' + str(i)))
    else:
        for i in range(2,len(component.Shape.Faces)+1):
            wall_faces.append((component, 'Face' + str(i)))

    # Determine the interog faces of the component.
    interog = []
    if component_name == 'blade':
        for i in range(1,4):
            interog.append((component, 'Face' + str(i)))
    elif component_name == 'hub':
        for i in range(1,2):
            interog.append((cut_object, 'Face' + str(i)))

    # Set mesh groups.
    mg_wall.References = wall_faces
    mg_volume.References = (component, 'Solid1')

    if component_name == 'blade' or component_name == 'hub':
        mg_interog.References = interog
    else:
        mg_farfield.References = (component, 'Face1') # Face1 is the surface of the sphere.

    # Finally, create the mesh.
    gmsh_mesh = femmesh.gmshtools.GmshTools(mesh)
    gmsh_mesh.create_mesh()

#def meshbox():
#    obj = doc.addObject("Part::Feature","Box")
#    obj.Shape = box
#
#    mesh = ObjectsFem.makeMeshGmsh(doc, 'FEMMeshGmsh')
#    mesh.Part = obj
#
#    mg_outer = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_outer')
#    mg_vol = ObjectsFem.makeMeshGroup(App.ActiveDocument, mesh, False, 'mg_vol')
#
#    temp = []
#    for i in range(1,7):
#        temp.append((obj, 'Face' + str(i)))
#
#    mg_outer.References = temp
#    mg_vol.References = (obj, 'Solid1')
#
#    import femmesh.gmshtools as gmshtools
#    gmsh_mesh = gmshtools.GmshTools(mesh)
#    gmsh_mesh.create_mesh()
#
#    doc.removeObject("Box")
#    doc.removeObject("FEMMeshGmsh")
#    doc.removeObject("mg_outer")
#    doc.removeObject("mg_vol")
#    doc.recompute()
