from PIL.Image import Palette


def convert(clip, mode=None, matrix=None, dither=None, palette=Palette.WEB, colors=256):
    clip.fl_frame_transform(lambda frame, *args, **
                            kwargs: frame.convert(*args, **kwargs), mode, matrix, dither, palette, colors)
    return clip
