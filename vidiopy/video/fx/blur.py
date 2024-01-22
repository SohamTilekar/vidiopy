from typing import Callable
from PIL import Image, ImageFilter


def box_blur(clip, radius: float | Callable[[float], float] = 2):
    if callable(radius):
        clip.fl_clip(lambda radius, _do_not_pass: _do_not_pass['frame'].filter(
            ImageFilter.BoxBlur(radius(_do_not_pass['frame_time']))), radius=lambda t: radius(t))
    else:
        clip.fl_frame_transform(
            (lambda frame, radius: frame.filter(
                ImageFilter.BoxBlur(radius)
            )),
            radius=radius)
    return clip


def gaussian_blur(clip, radius: float | Callable[[float], float] = 2):
    if callable(radius):
        clip.fl_clip(lambda radius, _do_not_pass: _do_not_pass['frame'].filter(
            ImageFilter.GaussianBlur(radius(_do_not_pass['frame_time']))), radius=lambda t: radius(t))
    else:
        clip.fl_frame_transform(
            (lambda frame, radius: frame.filter(
                ImageFilter.GaussianBlur(radius)
            )),
            radius=radius)
    return clip


def median_blur(clip, size: float | Callable[[float], float] = 2):
    if callable(size):
        clip.fl_clip(lambda size, _do_not_pass: _do_not_pass['frame'].filter(
            ImageFilter.MedianFilter(size(_do_not_pass['frame_time']))), size=lambda t: size(t))
    else:
        clip.fl_frame_transform(
            (lambda frame, size: frame.filter(
                ImageFilter.MedianFilter(size)
            )),
            size=size)
    return clip


def un_sharp(clip, radius: float | Callable[[float], float] = 2):
    if callable(radius):
        clip.fl_clip(lambda radius, _do_not_pass: _do_not_pass['frame'].filter(
            ImageFilter.UnsharpMask(radius(_do_not_pass['frame_time']))), radius=lambda t: radius(t))
    else:
        clip.fl_frame_transform(
            (lambda frame, radius: frame.filter(
                ImageFilter.UnsharpMask(radius)
            )),
            radius=radius)
    return clip
