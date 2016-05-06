from obspy import Catalog

class Cluster:
    """ Describe a cluster of events. Like a Catalog with metadata.

    Attributes:
        hypoDD_id (int): The ID assigned to the cluster by hypoDD
        successful_relocation (bool): True if the cluster was successfuly
            relocated by hypoDD. False otherwise.
        catalog (Catalog): An obspy Catalog object, containing the events of
            this cluster.
    """

    hypoDD_id = None
    event_ids = []
    successful_relocation = False
    catalog = None
    connectedness = None
    # TODO (@ogalanis) Add connectedness information

    def __init__(self):
        """ Initialization method for Cluster.
        """
        self.hypoDD_id = None
        self.event_ids = None
        self.successful_relocation = False
        self.catalog = None
        self.connectedness = None



