from PIL import Image, ImageEnhance
from ..VideoClips import VideoClip


def contrast(clip: VideoClip, strength: float = 2):
    if callable(strength):
        clip.fl_clip(lambda level, _do_not_pass: ImageEnhance.Contrast(
            _do_not_pass['frame']).enhance(level(_do_not_pass['frame_time'])), level=strength)
    else:
        clip.fl_frame_transform(lambda frame, level: ImageEnhance.Contrast(
            frame).enhance(level), strength)
    return clip


def brightness(clip: VideoClip, strength: float = 2):
    if callable(strength):
        clip.fl_clip(lambda level, _do_not_pass: ImageEnhance.Brightness(
            _do_not_pass['frame']).enhance(level(_do_not_pass['frame_time'])), level=strength)
    else:
        clip.fl_frame_transform(lambda frame, level: ImageEnhance.Brightness(
            frame).enhance(level), strength)
    return clip


def sharpness(clip: VideoClip, strength: float = 2):
    if callable(strength):
        clip.fl_clip(lambda level, _do_not_pass: ImageEnhance.Sharpness(
            _do_not_pass['frame']).enhance(level(_do_not_pass['frame_time'])), level=strength)
    else:
        clip.fl_frame_transform(lambda frame, level: ImageEnhance.Sharpness(
            frame).enhance(level), strength)
    return clip


def color(clip: VideoClip, strength: float = 2):
    if callable(strength):
        clip.fl_clip(lambda level, _do_not_pass: ImageEnhance.Color(
            _do_not_pass['frame']).enhance(level(_do_not_pass['frame_time'])), level=strength)
    else:
        clip.fl_frame_transform(lambda frame, level: ImageEnhance.Color(
            frame).enhance(level), strength)
    return clip
