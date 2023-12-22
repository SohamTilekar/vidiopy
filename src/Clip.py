from copy import deepcopy
import imageio as iio
import imageio_ffmpeg as iiof
import numpy as np

class Clip():
    
    def __init__(self) -> None:
        pass

    def copy(self):
        return deepcopy(self)