from typing import Any
from copy import deepcopy
import imageio as iio
import imageio_ffmpeg as iiof
import numpy as np


class VideoClip():
    def __init__(self, start: float = 0.0, end: float | None = None, duration: float | None = None, is_mask=False) -> None:
        self.start: float = start
        self.end: float | None = end
        self.duration: float | None = duration
        self.audio: Any = None
        self.relative_pos: bool = False
        self.pos = lambda t: (0, 0)
        self.is_mask: bool = is_mask
        self.size: tuple[int, int] = (0, 0)
        self.fps: float | int = 0

    def width(self):
        return self.size[0]
    
    def height(self):
        return self.size[1]
    
    def aspect_ratio(self):
        return self.width() / self.height()
    
    ...