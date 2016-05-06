class Connectedness:
    """ Describe the connectedness of a cluster of events.
    """

    catalog_P = []
    catalog_S = []
    cross_corr_P = []
    cross_corr_S = []

    def __init__(self):
        """ Initialization method for cluster.
        """
        self.catalog_P = []
        self.catalog_S = []
        self.cross_corr_P = []
        self.cross_corr_S = []
