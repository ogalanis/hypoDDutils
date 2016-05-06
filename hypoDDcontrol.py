from weight import Weight
from velocityModel import VelocityModel

class HypoDDControl:
    """Control parameters for hypoDD.

    Attributes:
    control_directory: The directory where the control file is located.
    control_file: The name of the control file.
    cc_dt_input: Filename of cross-corr diff. time input.
    ct_dt_input: Filename of catalog travel time input.
    initial_hypocenters: Filename of initial hypocenter input.
    station_input: Filename of station input.
    initial_hypocenters_output: Filename of initial hypocenter output.
    relocated_hypocenters_output: Filename of relocated hypocenter output.
    station_residual_output: Filename of station residual output.
    data_residual_output: Filename of data residual output.
    takeoff_angle_output: Filename of takeoff angle output.
    idat: Data type: 1 = cross correlation data only; 2 = absolute (catalog)
          data only; 3 = x-corr & catalog.
    ipha: Phase: 1 = P-wave; 2 = S-wave; 3 = P- & S-wave.
    dist: Max. distance between centroid of event cluster and stations.
    obscc, obsct: Min. number of x-corr, catalog links per event pair to form a
                  continuous cluster. 0 = no clustering performed. If IDAT = 3,
                  the sum of OBSCC and OBSCT is taken and used for both. 
    istart: Initial locations: 1 = start from cluster centroid; 2 = start from
            catalog locations.
    isolv: Least squares solution: 1 = singular value decomposition (SVD);
           2 = conjugate gradients (LSQR).
    weights: Data weighting by iteration. See class Weight.
    velocity_model: The velocity model to be used. See class VelocityModel.
    cid: Index of cluster to be relocated (0 = all).
    evid: ID of events to be relocated (8 per line). Blank for all events.
          The ID numbers are in free format.
    """

    control_directory = "."
    control_file = "hypoDD.inp"
    cc_dt_input = ""
    ct_dt_input = "dt.ct"
    initial_hypocenters = "event.dat"
    station_input = "station.dat"
    initial_hypocenters_output = "hypoDD.loc"
    relocated_hypocenters_output = "hypoDD.reloc"
    station_residual_output = "hypoDD.sta"
    data_residual_output = "hypoDD.res"
    takeoff_angle_output = "hypoDD.src"
    idat = 3
    ipha = 3
    dist = 400
    obscc = 0
    obsct = 8
    istart = 2
    isolv = 2
    weights = [Weight(niter=10, wtccp=-9, wtccs=-9, wrcc=-9, wdcc=-9,
                      wtctp=1, wtcts=0.5, wrct=3, wdct=3, damp=10)
              ]
    velocity_model = VelocityModel()    
    cid = 0
    evid = []

    def __init__(self, control_directory=".", control_file="hypoDD.inp",
                 cc_dt_input="", ct_dt_input="dt.ct",
                 initial_hypocenters="event.dat", station_input="station.dat",
                 initial_hypocenters_output="hypoDD.loc",
                 relocated_hypocenters_output="hypoDD.reloc",
                 station_residual_output="hypoDD.sta",
                 data_residual_output="hypoDD.res",
                 takeoff_angle_output="hypoDD.src", idat=3, ipha=3, dist=400,
                 obscc=0, obsct=8, istart=2, isolv=2,
                 weights=[Weight(niter=10, wtccp=-9, wtccs=-9, wrcc=-9, wdcc=-9,
                          wtctp=1, wtcts=0.5, wrct=3, wdct=3, damp=10)
                          ],
                 velocity_model=VelocityModel(), cid=0, evid=[] 
                 ):
        """Initialization method for the HypoDDControl object.
        """
        self.control_directory = control_directory
        self.control_file = control_file
        self.cc_dt_input = cc_dt_input
        self.ct_dt_input = ct_dt_input
        self.initial_hypocenters = initial_hypocenters
        self.station_input = station_input
        self.initial_hypocenters_output = initial_hypocenters_output
        self.relocated_hypocenters_output = relocated_hypocenters_output
        self.station_residual_output = station_residual_output
        self.data_residual_output = data_residual_output
        self.takeoff_angle_output = takeoff_angle_output
        self.idat = idat
        self.ipha = ipha
        self.dist = dist
        self.obscc = obscc
        self.obsct = obsct
        self.istart = istart
        self.isolv = isolv
        self.weights = weights
        self.velocity_model = velocity_model   
        self.cid = cid
        self.evid = evid

    def write_control_file(self):
        print "preparing hypoDD control"
        print "working directory is {}".format(self.control_directory)
        full_filename="{}/{}".format(self.control_directory,
                                     self.control_file
                                     )
        print "writing ph2dt control file: {}".format(full_filename)

        nlay = len(self.velocity_model.layers)
        nset = len(self.weights)

        with open(full_filename, "w") as f:
            control_file_format_1=("* {}\n"
                                   "*--- INPUT FILE SELECTION\n"
                                   "* filename of cross-corr diff. time input "
                                   "(blank if not available):\n"
                                   "{}\n"
                                   "* filename of catalog travel time input "
                                   "(blank if not available):\n"
                                   "{}\n"
                                   "* filename of initial hypocenter input:\n"
                                   "{}\n"
                                   "* filename of station input:\n"
                                   "{}\n"
                                   "*\n"
                                   "*--- OUTPUT FILE SELECTION\n"
                                   "* filename of initial hypocenter output "
                                   "(if blank: output to hypoDD.loc):\n"
                                   "{}\n"
                                   "* filename of relocated hypocenter output "
                                   "(if blank: output to hypoDD.reloc):\n"
                                   "{}\n"
                                   "* filename of station residual output "
                                   "(if blank: no output written):\n"
                                   "{}\n"
                                   "* filename of data residual output "
                                   "(if blank: no output written):\n"
                                   "{}\n"
                                   "* filename of takeoff angle output "
                                   "(if blank: no output written):\n"
                                   "{}\n"
                                   "*\n"
                                   "*--- DATA SELECTION:\n"
                                   "* IDAT IPHA DIST\n"
                                   "{} {} {}\n"
                                   "*\n"
                                   "*--- EVENT CLUSTERING:\n"
                                   "* OBSCC OBSCT\n"
                                   "{} {}\n" 
                                   "*\n"
                                   "*--- SOLUTION CONTROL:\n" 
                                   "* ISTART ISOLV NSET\n"
                                   "{} {} {}\n"
                                   "*\n"
                                   "*--- DATA WEIGHTING AND REWEIGHTING:\n"
                                   "* NITER WTCCP WTCCS WRCC WDCC WTCTP WTCTS "
                                   "WRCT WDCT DAMP\n"
                                   )
            f.write(control_file_format_1.format(self.control_file,
                                             self.cc_dt_input,
                                             self.ct_dt_input,
                                             self.initial_hypocenters,
                                             self.station_input,
                                             self.initial_hypocenters_output,
                                             self.relocated_hypocenters_output,
                                             self.station_residual_output,
                                             self.data_residual_output,
                                             self.takeoff_angle_output,
                                             self.idat,
                                             self.ipha,
                                             self.dist,
                                             self.obscc,
                                             self.obsct,
                                             self.istart,
                                             self.isolv,
                                             nset
                                             ))
            control_file_format_2="{} {} {} {} {} {} {} {} {} {}\n"
            for weight in self.weights:
                f.write(control_file_format_2.format(weight.niter,
                                                   weight.wtccp,
                                                   weight.wtccs,
                                                   weight.wrcc,
                                                   weight.wdcc,
                                                   weight.wtctp,
                                                   weight.wtcts,
                                                   weight.wrct,
                                                   weight.wdct,
                                                   weight.damp
                                                   ))
            control_file_format_3=("*\n"
                                   "*--- MODEL SPECIFICATIONS:\n"
                                   "* NLAY RATIO\n"
                                   "{} {}\n"
                                   "* TOP:\n"
                                   )
            f.write(control_file_format_3.format(nlay,
                                                 self.velocity_model.ratio
                                                 ))
            control_file_format_4=" {}"
            for layer in self.velocity_model.layers:
                f.write(control_file_format_4.format(layer.top))
            f.write("\n* VEL:\n".format())
            for layer in self.velocity_model.layers:
                f.write(control_file_format_4.format(layer.vel))
            control_file_format_5=("\n*\n"
                                   "*--- CLUSTER/EVENT SELECTION:\n"
                                   "* CID\n"
                                   "{}\n"
                                   )
            f.write(control_file_format_5.format(self.cid))
            f.write("* ID\n".format())
            n=len(self.evid)
            k=n//8
            m=n-8*k
            control_file_format_6="{}\n"
            for i in range(1,k+1):
                f.write(control_file_format_6.format(
                     " ".join(str(x) for x in self.evid[i*8-8:i*8])
                     ))
            f.write(control_file_format_6.format(
                     " ".join(str(x) for x in self.evid[n-m:n])
                     ))



