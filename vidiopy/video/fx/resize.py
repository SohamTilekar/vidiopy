from typing import Callable
from moviepy.video.fx.resize import resize
from PIL.Image import Image
Image.resize


def resize(clip, newsize: None | tuple[float, float] | tuple[int, int] = None, height: int | None = None, width: int | None = None):
    w: int = clip.size[0]
    h: int = clip.size[1]

    if newsize is not None:
        ...
    elif height is not None:
        newsize = (w * height // h, height)

    elif width is not None:
        newsize = (width, h*width // w)
    elif width is not None and height is not None:
        newsize = (width, height)
    else:
        raise
    clip.size = newsize
    return clip.fl_frame_transform(
        lambda frame, size: frame.resize(size),
        newsize
    )
