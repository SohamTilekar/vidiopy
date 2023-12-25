from typing import (Any, Callable, Self, Optional, Generator,
                    )
import os
import tempfile
from copy import copy as _copy
import imageio as iio
import ffmpegio
import numpy as np

class Clip():
    ...