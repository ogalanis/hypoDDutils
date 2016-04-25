from subprocess import call
import os
import math
from obspy.core.event import Event,Origin,Catalog
from obspy.core.event.base import CreationInfo
from obspy.core.event.magnitude import Magnitude
from ph2dtControl import Ph2dtControl
from ph2dtInput import Ph2dtInput
from hypoDDcontrol import HypoDDControl
from hypoDDinput import HypoDDInput
from cluster import Cluster
from obspy.core.utcdatetime import UTCDateTime
import info

class HypoDDObject:
    """ Describes a run of the hypoDD earthquake location program.

    Attributes:
    catalog: A Catalog object containing the earthquakes to be processed.
    client: A Client object used to acquire event/station information.
    directory: The working directory.
    ph2dt_executable: The name of the ph2dt executable.
    hypoDD_executable: The name of the hypoDD executable.
    ph2dt_control: A Ph2dtControl object describing the ph2dt parameters.
    ph2dt_input: A Ph2dtInput object describing the ph2dt input.
    hypoDD_control: A HypoDDControl object describing the hypoDD parameters.
    hypoDD_input: A HypoDDInput object describing the hypoDD input.
    Methods:
    __init__: Initialization method.
    prepare_all: Prepare control and input files for ph2dt and hypoDD.
    run_ph2dt: Run ph2dt with the current configuration.
    run_hypODD: Run hypoDD with the current configuration.
    """

    catalog = None
    client = None
    directory = "."
    ph2dt_executable = "ph2dt"
    hypoDD_executable = "hypoDD"
    ph2dt_control = Ph2dtControl()
    ph2dt_input = Ph2dtInput(catalog)
    hypoDD_control = HypoDDControl()
    hypoDD_input = HypoDDInput(catalog, client, directory)

    def __init__(self, catalog=None, client=None, directory=".",
                 ph2dt_executable="ph2dt", hypoDD_executable="hypoDD"
                 ):
        """ Initialization method for HypoDDObject.
        """
        self.catalog=catalog
        self.client=client
        self.directory=directory
        self.ph2dt_executable = ph2dt_executable
        self.hypoDD_executable = hypoDD_executable
        self.ph2dt_control = Ph2dtControl(control_directory=directory)
        self.ph2dt_input = Ph2dtInput(catalog, input_directory=directory)
        self.hypoDD_control = HypoDDControl(control_directory=directory)
        self.hypoDD_input = HypoDDInput(catalog, client, directory)

    def prepare_all(self):
        """ Prepare control and input files for ph2dt and hypoDD.
        """
        self.ph2dt_control.write_control_file()
        self.hypoDD_control.write_control_file()
        self.ph2dt_input.prepare_catalog_abs_tt_input()
        self.hypoDD_input.prepare_all()

    def run_ph2dt(self):
        """ Run ph2dt with the current configuration.
        """
        cwd=os.getcwd()
        os.chdir(self.directory)
        call(["./"+self.ph2dt_executable, self.ph2dt_control.control_file])
        os.chdir(cwd)

    def run_hypoDD(self):
        """ Run hypoDD with the current configuration. 
        """
        cwd=os.getcwd()
        os.chdir(self.directory)
        call(["./"+self.hypoDD_executable, self.hypoDD_control.control_file])
        os.chdir(cwd)

    def get_results(self):
        cids = []
        clusters = []
        results_file = "{}/{}".format(self.hypoDD_control.control_directory,
                              self.hypoDD_control.relocated_hypocenters_output
                              )
        with open(results_file, "r") as f:
            for line in f:
                num = line.split()
                evid = num[0]
                lat = float(num[1])
                lon = float(num[2])
                dep = 1000 * float(num[3])  # km to m
                errx = num[7]
                erry = num[8]
                errz = num[9]
                yr = int(num[10])
                mo = int(num[11])
                dy = int(num[12])
                hr = int(num[13])
                mi = int(num[14])
                sc = float(num[15])
                mag = num[16]
                nccp = num[17]
                nccs = num[18]
                nctp = num[19]
                ncts = num[20]
                rcc = num[21]
                rct = num[22]
                cid = num[23]
                if cid not in cids:
                    cids.append(cid)
                    clusters.append(Cluster())
                    clusters[-1].hypoDD_id=cid
                    clusters[-1].successful_relocation=True
                    clusters[-1].catalog=Catalog()
                origin=Origin()
                isec = int ( math.floor( sc ))
                micsec = int ( ( sc - isec) * 1000000 )
                origin.time = UTCDateTime(yr, mo, dy, hr, mi, isec, micsec)
                origin.longitude = lon
                origin.latitude = lat
                origin.depth = dep
                origin.method_id = "hypoDD"
                # TODO (@ogalanis): Add time/location errors (when
                # appropriate. Add quality and origin_uncertainty. Add arrivals.
                event=Event()
                event.creation_info=CreationInfo()
                event.creation_info.author = __package__
                event.creation_info.version = info.__version__
                event.origins=[origin]
                event.magnitude=Magnitude()
                event.magnitude.mag=mag
                idx=cids.index(cid)
                clusters[idx].catalog.events.append(event)


        return clusters



