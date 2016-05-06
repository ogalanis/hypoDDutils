class Weight:
    """Iteration dependent weighting parameters for hypoDD.

    Attributes:
    niter: Number of iterations for the set of weighting parameters that follow.
    wtccp, wtccs: Weight for cross-corr P-wave, S-wave data. -9 = data not used.
    wtctp, wtcts: Weight for catalog P-wave, S-wave data. -9 = data not used.
    wrcc, wrct: Cutoff threshold for outliers located on the tails of the
                cross-corr, catalog data.
                0<1 = absolute threshold in sec (static cutoff).
                >=1 = factor to multiply standard deviation (dynamic cutoff).
                -9 = no outlier removed.
    wdcc, wdct: Max. event separation distance [km] for x-corr data, catalog
                data. -9 = not activated.
    damp: Damping (only for HypoDDControl.isolv= 2).
    Methods:
    __init__: Initialization method.
    """
    niter = 5
    wtccp = -9
    wtccs = -9
    wrcc = -9
    wdcc = -9
    wtctp = 1
    wtcts = 0.5
    wrct = -9
    wdct = -9
    damp = 1

    def __init__(self, niter=5, wtccp=-9, wtccs=-9, wrcc=-9, wdcc=-9,
                 wtctp=1, wtcts=0.5, wrct=-9, wdct=-9, damp=1
                 ):
        """Initializaton method for the weighting parameters class.
        """
        self.niter = niter
        self.wtccp = wtccp
        self.wtccs = wtccs
        self.wrcc = wrcc
        self.wdcc = wdcc
        self.wtctp = wtctp
        self.wtcts = wtcts
        self.wrct = wrct
        self.wdct = wdct
        self.damp = damp



