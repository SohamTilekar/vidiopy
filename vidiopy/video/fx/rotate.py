from typing import Callable
from PIL import Image
Image.Image.rotate


def rotate(clip, angle: float | Callable[[float], float], center: tuple[float, float] | None = None, bg_color=(0, 0, 0), expand=False):
    # TODO: Add the Support to the expand Parameter
    if expand:
        raise NotImplementedError('expand = True is not Implemented')
    if callable(angle):
        clip.fl_clip(_rotate_clip, angle=lambda t: angle(t), center=center,
                     bg_color=bg_color, expand=expand)
    else:
        clip.fl_frame_transform(_rotate_ft, angle=lambda t: angle, center=center,
                                bg_color=bg_color, expand=expand)
    return clip


def _rotate_ft(frame: Image.Image, angle, center, expand, bg_color):
    frame.rotate(angle=angle, center=center, expand=expand, fillcolor=bg_color)


def _rotate_clip(angle, center, bg_color, expand, _do_not_pass):
    return _do_not_pass['frame'].rotate(
        angle=angle(_do_not_pass['frame_time']), center=center, fillcolor=bg_color, expand=expand)
