from layer import Layer

class VelocityModel:
    """Describes a simple layered seismic wave velocity model.

    Attributes:
    ratio: The ratio of the P-wave velocity over the S-wave velocity.
    layers: a list of Layer objects describing the layers. The unmodified hypoDD
            software allows for up to 12 layers.
    Methods:
    __init__: Initialization method.
    """
    ratio = 1.73
    layers = [Layer(0.0, 3.77),
              Layer(1.0, 4.64),
              Layer(3.0, 5.34),
              Layer(6.0, 5.75),
              Layer(14.0, 6.22),
              Layer(25.0, 7.98)
              ]

    def  __init__(self, ratio=1.73, layers=[Layer(0.0, 3.77),
                                            Layer(1.0, 4.64),
                                            Layer(3.0, 5.34),
                                            Layer(6.0, 5.75),
                                            Layer(14.0, 6.22),
                                            Layer(25.0, 7.98)
                                            ]):
        """Initialization method for the velocity model class.
        """
        self.ratio = ratio
        self.layers = layers

