from obspy.core.event.origin import OriginUncertainty
from obspy.core.utcdatetime import UTCDateTime


def time2hypoDDdate(time):
    """Extract the date from a UTCDateTime object in hypoDD format.

    The format used by hypoDD is an integer constructed by the year, month and
    day put together (YYYYMMDD). This means that month and day should be
    zero-padded.
    """
    return int(time.strftime("%Y%m%d"))


def time2hypoDDtime(time):
    """Extract the time from a UTCDateTime object in hypoDD format.

    The format used by hypoDD is an integer constructed by the hour, minute,
    second and hundredths of second put together (HHMMSSss). Any leading zeros
    are discarded.
    """
    timestr = time.strftime("%H%M%S%f")
    timestr = timestr[0:8]
    return int(timestr)


class HypoDDInput:
    """Input used by the hypoDD earthquake location program.

    Attributes:
    input_directory: The directory where the input files are located.
    hypocenter_input: The name of the hypocenter input file ('event.dat')
    station_input: The name of the station input file ('station.dat')
    catalog_tt_input: The name of the catalog travel time input file ('dt.cc')
    catalog_cc_input: The name of the cross correlation differential time input
                      file ('dt.cc')
    Methods:
    __init__: Initialization method.
    prepare_hypocenter_input: Prepares the hypocenter input file.
    prepare_station_input: Prepares the station input file.
    prepare_catalog_tt_input: Prepares the catalog travel time input file.
    prepare_all: Prepares all the above files.
    """

    catalog=None
    client=None
    input_directory = "."
    hypocenter_input = "event.dat"
    station_input = "station.dat"
    catalog_tt_input = None
    catalog_cc_input = None

    def __init__(self, catalog, client, input_directory=".",
                 hypocenter_input="event.dat", station_input="station.dat",
                 catalog_tt_input = None, catalog_cc_input = None
                 ):
        """Initialization method for the HypoDDinput class.

        Arguments:
        catalog: An obspy Catalog object which contains the events to be
                 processed
        client : An obspy Client object which is used to provide phase (picks)
                 information
        """
        self.catalog = catalog
        self.client = client
        self.input_directory = input_directory
        self.hypocenter_input = hypocenter_input
        self.station_input = station_input
        self.catalog_tt_input = catalog_tt_input
        self.catalog_cc_input = catalog_cc_input

    def prepare_hypocenter_input(self):
        """Prepare the hypocenter input file for hypoDD.

        The hypocenter input is the file normaly named 'event.dat', which
        contains hypocenter parameters for the events to be located.
        """
        full_filename = "{}/{}".format(self.input_directory,
                                       self.hypocenter_input
                                       )
        print "preparing initial hypocenter input file: {}".format(
                                                        full_filename
                                                        )
        with open(full_filename, "w") as f:
            for idx,evt in enumerate(self.catalog):
                orig = evt.preferred_origin()
                origin_time = orig.time
                lat = orig.latitude
                lon = orig.longitude
                dep = orig.depth / 1000.0  # Converting m to km.
                # TODO (@ogalanis) Currently it assumes that there is no
                # horizontal and vertical uncertainty information in the catalog
                # which is true for the KNMI catalog, but not for other
                # catalogs.
                # It should be fixed to use this information when available.
                #dh  = orig.origin_uncertainty
                errh = 0.0
                errv = 0.0
                rms=orig.quality.standard_error
                if rms is None:
                    rms = 0.0
                mag = evt.preferred_magnitude()
                magnitude = mag.mag
                # hypoDD uses 0.0 to denote no magnitude. However, given that
                # a) hypoDD does not use magnitudes for anything and
                # b) it is possible to have a magnitude of 0.0 in the catalog
                # we use the smallest number that fits in the 4.1f format.
                if magnitude is None:
                    magnitude = -9.9
                hypocenter_input_format = ("{:>8d}  {:>8d} {:>9.4f} {:>10.4f} "
                                         "{:>10.4f} {:>4.1f} {:>7.2f} {:>7.2f} "
                                         "{:>6.2f} {:>10d}\n"
                                         )
                f.write(hypocenter_input_format.format(
                                   time2hypoDDdate(origin_time),
                                   time2hypoDDtime(origin_time),
                                   lat,
                                   lon,
                                   dep,
                                   magnitude,
                                   errh,
                                   errv,
                                   rms,
                                   idx+1   # Start from 1, not 0.
                                   ))

    def prepare_station_input(self):
        """Prepare the station input file for hypoDD.
 
        The station input file is the file normally named 'station.dat', which
        contains the coordinates of the stations used for location
        """
        stations = []
        bulk = []
        distantPast = UTCDateTime("1900-01-01T00:00:00")
        distantFuture = UTCDateTime("3000-01-01T00:00:00")
        full_filename = "{}/{}".format(self.input_directory,
                                       self.station_input
                                       )
        print "preparing station input file: {}".format(full_filename)
        with open(full_filename, "w") as f:
            for evt in self.catalog:
                for pick in evt.picks:
                    sta = pick.waveform_id.station_code
                    if sta not in stations:
                        stations.append(sta)
            for sta in stations:
                bulk.append(("*", sta, "*", "*", distantPast, distantFuture))
            inv = self.client.get_stations_bulk(bulk)
            for net in inv:
                for sta in net:
                    station_input_format = "{:<7} {:>12.6f} {:>12.6f}\n"
                    f.write(station_input_format.format(sta.code,
                                                        sta.latitude,
                                                        sta.longitude
                                                        ))

    def prepare_catalog_tt_input(self):
        print "preparing catalog travel time input file: {}".format(
                                                       self.catalog_tt_input
                                                       )
        # TODO(@ogalanis) This one can wait, as there is a hypoDD
        # utility program that has its functionality.

    def prepare_cc_tt_input(self):
        print "preparing cross correlation differential time input: {}".format(
                                                    self.catalog_cc_input
                                                    )
        # TODO(@ogalanis)

    def prepare_all(self):
        """Prepare all input files for hypoDD.

        These files are:
        Initial hypocenter input, normally named 'event.dat'
        Station input, normally named 'station.dat'
        Catalog travel time input, normally named 'dt.ct'
        """
        print "preparing hypoDD input"
        print "working directory is {}".format(self.input_directory)
        self.prepare_hypocenter_input()
        self.prepare_station_input()
        if self.catalog_tt_input is not None:
            self.prepare_catalog_tt_input()
        if self.catalog_cc_input is not None:
            self.prepare_catalog_cc_input()
    

