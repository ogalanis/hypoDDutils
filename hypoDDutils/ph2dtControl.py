class Ph2dtControl:
    """Control parameters for the ph2dt utility of hypoDD.

    Attributes:
    control_directory: The directory whrer the control file is located.
    control_file: The name of the control file.
    station_input: The name of the station file.
    phase_data: The name of the phase data file, which is ph2dt's input.
    minwght: Minimum pick weight [0 - 1 (best)]. Note that weights less than
             1.0e-5 are not considered in hypoDD.
    maxdist: Maximum distance (in km) between event pair and station.
    maxsep: Max. hypocentral separation between event pairs in km.
    maxngh: Max. number of neighbors per event.
    minlink: Min. number of links required to define a neighbor
    minobs: Min. number of links per pair saved.
    maxobs: Max. number of links per pair saved
            (ordered by distance from event pair).
    Methods:
    __init__: Initialization method.
    write_control_file: Writes the control file.
    """

    control_directory = "."
    control_file = "ph2dt.inp"
    station_input = "station.dat"
    phase_data = "phase.dat"
    minwght = 0
    maxdist = 500
    maxsep = 10
    maxngh = 10
    minlink = 8
    minobs = 8
    maxobs = 50

    def __init__(self, control_directory=".", control_file="ph2dt.inp",
                 station_input="station.dat", phase_data="phase.dat",
                 minwght=0, maxdist=500, maxsep=10, maxngh=10, minlink=8,
                 minobs=8, maxobs=50
                 ):
        """Initialization method for the ph2dt control class.
        """
        self.control_directory = control_directory
        self.control_file = control_file
        self.station_input = station_input
        self.phase_data =  phase_data
        self.minwght = minwght
        self.maxdist = maxdist
        self.maxsep = maxsep
        self.maxngh = maxngh
        self.minlink = minlink
        self.minobs = minobs
        self.maxobs = maxobs

    def write_control_file(self):
        print "preparing ph2dt control"
        print "working directory is {}".format(self.control_directory)
        full_filename="{}/{}".format(self.control_directory,
                                     self.control_file
                                     )
        print "writing ph2dt control file: {}".format(full_filename)
        with open(full_filename, "w") as f:
            control_file_format=("* {}\n"
                                 "*--- I/O FILES:\n"
                                 "* filename of station input:\n"
                                 "{}\n"
                                 "* filename of phase data input:\n"
                                 "{}\n"
                                 "*--- DATA SELECTION PARAMETERS:\n"
                                 "* MINWGHT MAXDIST MAXSEP MAXNGH "
                                 "MINLNK MINOBS MAXOBS\n"
                                 "  {:>7.4f} {:>7.2f} {:>6.2f} {:^6d} "
                                 "{:^6d} {:^6d} {:^6d}\n"
                                 )
            f.write(control_file_format.format(self.control_file,
                                               self.station_input,
                                               self.phase_data,
                                               self.minwght,
                                               self.maxdist,
                                               self.maxsep,
                                               self.maxngh,
                                               self.minlink,
                                               self.minobs,
                                               self.maxobs
                                               ))



