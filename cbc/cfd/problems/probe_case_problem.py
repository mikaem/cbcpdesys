from numpy import loadtxt, array, load
from cbc.pdesys import *
from cbc.cfd.tools.Probe import Probes, Probedict
import os

testcase = 1
refinement = 0
stationary = False
dt = 0.0001
timestep = 2000
mesh_filename = "/home/kent-and/Challenge/mesh_750k_BL_t.xml.gz"
if refinement==1: mesh_filename = "/home/kent-and/Challenge/mesh_2mio_BL_t.xml.gz"
if refinement==2: mesh_filename = "/home/kent-and/Challenge/mesh_4mio_BL_t.xml.gz"   
mesh = Mesh(mesh_filename)
mesh_filename = mesh_filename.split('/')[-1][:-7]
fileid = "Sat_Jan__7_23:52:57_2012"

xmlfile = "/home/mikaelmo/cbcpdesys/cbc/cfd/problems/{0}/testcase_{1}_dt={2}_{3}/timestep={4}".format(mesh_filename, testcase, dt, fileid, timestep)
#xmlfile = "/home/mikaelmo/cbcpdesys/cbc/cfd/problems/{0}/testcase_{1}_dt={2}_refinement_{3}/timestep={4}".format(mesh_filename, testcase, dt, refinement, timestep)
xmlfile = os.path.join(xmlfile, '{0}.xml.gz')

V = FunctionSpace(mesh, 'CG', 1)
#sys_comp = ['u0', 'u1', 'u2', 'p']
sys_comp = ['p']
cl = loadtxt('cl.dat')
probes = []
for i in range(cl.shape[0]):
    probes.append(array(cl[i, :3]))

# Set up and eval all probes 
probe_dict = Probedict((ui, Probes(probes, V, 1)) for ui in sys_comp)
q_ = dict((ui, Function(V, xmlfile.format(ui))) for ui in sys_comp)
for ui in sys_comp:
    q_[ui].gather()
probe_dict.probe(q_)

# Run through all the probes and collect the values in one single array that should be plotted against cl[:, 1]
# Because the probes live on different processors we need to reduce it to one single processor before dumping
# the array. However, I haven't figured out a way to reduce yet, so for now I reduce by storing the results in
# intermediate files that are deleted on exit 
x = zeros(cl.shape[0])
for ui in sys_comp:
    for i, probe in probe_dict[ui]:
        x[i] = probe.probes[0, 0]
        # Store value in a file
        array([x[i]]).dump(ui + '_' + str(i) + '.dat')

if MPI.process_number() == 0:
    for ui in sys_comp:
        for i in range(cl.shape[0]):
            f = load(ui + '_' + str(i) + '.dat')
            x[i] = f[0]
            os.system('rm ' + ui + '_' + str(i) + '.dat')
        x.dump(xmlfile[:-10] + ui + '_timestep_' + str(timestep) + '.probe')

