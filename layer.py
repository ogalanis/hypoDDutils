class Layer:
    """Describes a single layer in a layered velocity model.
    
    Attributes:
    top: The depth of the top of the layer.
    vel: P-wave velocity inside this model.
    Methods:
    __init__: Initialization method.
    """
    top = 0.0
    vel = 3.77

    def __init__(self, top=0.0, vel=3.77):
        """Initialization method for the layer class.
        """
        self.top = top
        self.vel = vel



