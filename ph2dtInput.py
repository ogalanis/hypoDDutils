class Ph2dtInput:
    """Input used by the ph2dt utility of hypoDD.

    Attributes:
    input_directory: The directory where the input file is located.
    catalog_abs_tt_input: The name of the input file.
    Methods:
    __init__(self,catalog)
    prepare_catalog_abs_tt_input(self)
    """

    input_directory = "."
    catalog_abs_tt_input = "phase.dat"

    def __init__(self, catalog, input_directory=".",
                 catalog_abs_tt_input="phase.dat"
                 ):
        """Initialization method for the HypoDDinput class.

        Arguments:
        catalog: An obspy Catalog object which contains the events to be
                 processed
        """
        self.catalog = catalog
        self.input_directory = input_directory
        self.catalog_abs_tt_input = catalog_abs_tt_input

    def prepare_catalog_abs_tt_input(self):
        """Prepare the catalog absolute travel time input file for hypoDD.

        The catalog absolute travel time input is the file normally named
        'phase.dat', which contains hypocenter parameters and absolute arrival
        times from all events to all stations.
        """
        weights = []
        print "preparing ph2dt input"
        print "working directory is {}".format(self.input_directory)
        full_filename = "{}/{}".format(self.input_directory,
                                       self.catalog_abs_tt_input
                                       )
        print "preparing catalog absolute travel time input file: {}".format(
                                                     full_filename 
                                                     )
        with open(full_filename, "w") as f:
            for idx, evt in enumerate(self.catalog):
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
                hypocenter_input_format = ("# {:>4d} {:>2d} {:>2d} {:>2d} "
                                           "{:>2d} {:>5.2f} {:>9.4f} {:>10.4f} "
                                           "{:>10.4f} {:>4.1f} {:>7.2f} "
                                           "{:>7.2f} {:>6.2f} {:>10d}\n"
                                           )
                f.write(hypocenter_input_format.format(
                            origin_time.year,
                            origin_time.month,
                            origin_time.day,
                            origin_time.hour,
                            origin_time.minute,
                            origin_time.second + origin_time.microsecond/1.0e6,
                            lat,
                            lon,
                            dep,
                            magnitude,
                            errh,
                            errv,
                            rms,
                            idx+1   # Start from 1, not 0.
                            ))
                for arr in orig.arrivals:
                    weights.append( (arr.pick_id, arr.time_weight) )
                for pick in evt.picks:
                    pick_weight = 1.0
                    #for pair in weights:
                    #    if pair[0] == pick.resource_id:
                    #        pick_weight=pair[1]
                    # TODO(@ogalanis) The code above returns the weight
                    # used for the computation of this origin. It is not
                    # necessarily a measure of the uncertainty of the pick. See
                    # if you can use the onset, when available.
                    pick_format = ("{:<7} {:>12.6f} {:>7.4f} {:<1}\n")
                    f.write(pick_format.format(pick.waveform_id.station_code,
                                               pick.time.__sub__(origin_time),
                                               pick_weight,
                                               pick.phase_hint
                                               ))



