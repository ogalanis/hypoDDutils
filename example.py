from obspy.core.event import Event,Origin,Catalog
from obspy.core.utcdatetime import UTCDateTime
from obspy.clients.fdsn import Client
# 1. Import HypoDDObject
from hypoDDutils.hypoDDobject import HypoDDObject

def main():
# 2. Get your events in an obspy Catalog object. Be sure to include the
#    arrivals, so that hypoDD has something to work on, as waveform
#    cross-correlation has not been implemented yet.
    client = Client("http://rdsa.knmi.nl")
    mycat = client.get_events( minmagnitude=0.0,
                               minlatitude=52.6,
                               minlongitude=6.0,
                               maxlatitude=53.8,
                               maxlongitude=7.5,
                               starttime=UTCDateTime("2015-01-01T00:00:00"),
                               includearrivals=True)

# 3. Initialize a hypoDD object. The working directory should contain the
#    binaries for ph2dt and hypoDD. You need the client argument to download
#    station metadata and waveforms* (*not implemented yet)
    myhypoDD=HypoDDObject(mycat,client,"./work")

# 4. Set values for ph2dt and hypoDD parameters (see manual for details), if
#    you don't want to use the default hypoDDutil values (you probably don't)
    myhypoDD.ph2dt_control.maxsep = 7.5
    myhypoDD.hypoDD_control.dist = 300
#   and so on. You can give values for all parameters, or for none.

# 5. Prepare the control files and input files
    myhypoDD.prepare_all()
# 6. Run ph2dt with the current configuration
    myhypoDD.run_ph2dt()
# 7. Run hypoDD with the current configuration
    myhypoDD.run_hypoDD()

# 8. Get the output in the form of a list of clusters (in the hypoDD sense)
#    a cluster is a catalog with some metadata, like whether hypoDD succeeded
#    with these events or how well connected* the cluster is (*not implemented
#    yet)
    clusters=myhypoDD.get_results()

    for cluster in clusters:
        print "hypoDD cluster ID: {}".format(cluster.hypoDD_id)
        print "cluster was relocated successfully: {}".format(
                                               cluster.successful_relocation
                                               )
        print cluster.catalog
        print

if __name__ == '__main__':
    main()

