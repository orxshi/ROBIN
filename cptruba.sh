tar cf heli.tar \
    fuspyl_core.geo \
    fuspyl_interior.geo \
    fuspyl_wall.geo \
    fuspyl_dirichlet.geo \
    fuspyl.brep \
    wing0_core.geo \
    wing0_interior.geo \
    wing0_wall.geo \
    wing0_dirichlet.geo \
    wing0.brep \
    wing1_core.geo \
    wing1_interior.geo \
    wing1_wall.geo \
    wing1_dirichlet.geo \
    wing1.brep \
    wing2_core.geo \
    wing2_interior.geo \
    wing2_wall.geo \
    wing2_dirichlet.geo \
    wing2.brep \
    wing3_core.geo \
    wing3_interior.geo \
    wing3_wall.geo \
    wing3_dirichlet.geo \
    wing3.brep

scp heli.tar osibliyev@172.16.10.1:/truba/home/osibliyev/Tailor3D/msh/heli
