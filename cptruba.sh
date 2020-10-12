tar cf heli.tar \
    fuspyl.geo \
    fuspyl.brep \
    wing0.geo \
    wing0.brep \
    wing1.geo \
    wing1.brep \
    wing2.geo \
    wing2.brep \
    wing3.geo \
    wing3.brep

scp heli.tar osibliyev@172.16.10.1:/truba/home/osibliyev/Tailor3D/msh/heli
