from vidiopy.video.VideoClip import VideoClip
from PIL import Image, ImageFilter, ImageEnhance


def gaussian_blur(video: VideoClip, radius=2):
    """Return a video with a Gaussian blur effect."""

    def _blur(frame: Image.Image, radius=radius):
        return frame.filter(ImageFilter.GaussianBlur(radius))

    return video.fl_frame_transform(_blur, radius)


def box_blur(video: VideoClip, radius=2):
    """Return a video with a box blur effect."""

    def _blur(frame: Image.Image, radius=radius):
        return frame.filter(ImageFilter.BoxBlur(radius))

    return video.fl_frame_transform(_blur, radius)


def unsharp_mask(video: VideoClip, radius=0.5, percent=150, threshold=3):
    """Return a video with an unsharp mask effect."""

    def _mask(frame: Image.Image, radius=radius, percent=percent, threshold=threshold):
        return frame.filter(ImageFilter.UnsharpMask(radius, percent, threshold))

    return video.fl_frame_transform(_mask, radius, percent, threshold)


def median_filter(video: VideoClip, size=3):
    """Return a video with a median filter effect."""

    def _filter(frame: Image.Image, size=size):
        return frame.filter(ImageFilter.MedianFilter(size))

    return video.fl_frame_transform(_filter, size)


def contrast(video: VideoClip, factor=1.0):
    """Return a video with a contrast effect."""

    def _contrast(frame: Image.Image, factor=factor):
        enhancer = ImageEnhance.Contrast(frame)
        return enhancer.enhance(factor)

    return video.fl_frame_transform(_contrast, factor)


def brightness(video: VideoClip, factor=1.0):
    """Return a video with a brightness effect."""

    def _brightness(frame: Image.Image, factor=factor):
        enhancer = ImageEnhance.Brightness(frame)
        return enhancer.enhance(factor)

    return video.fl_frame_transform(_brightness, factor)


def saturation(video: VideoClip, factor=1.0):
    """Return a video with a saturation effect."""

    def _saturation(frame: Image.Image, factor=factor):
        enhancer = ImageEnhance.Color(frame)
        return enhancer.enhance(factor)

    return video.fl_frame_transform(_saturation, factor)


def sharpness(video: VideoClip, factor=1.0):
    """Return a video with a sharpness effect."""

    def _sharpness(frame: Image.Image, factor=factor):
        enhancer = ImageEnhance.Sharpness(frame)
        return enhancer.enhance(factor)

    return video.fl_frame_transform(_sharpness, factor)
