from vidiopy.video.VideoClip import VideoClip
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np


def gaussian_blur(video: VideoClip, radius=2):
    """Return a video with a Gaussian blur effect."""

    def _blur(frame: np.ndarray, radius=radius):
        return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(radius)))

    return video.fl_frame_transform(_blur, radius)


def box_blur(video: VideoClip, radius=2):
    """Return a video with a box blur effect."""

    def _blur(frame: np.ndarray, radius=radius):
        return np.array(Image.fromarray(frame).filter(ImageFilter.BoxBlur(radius)))

    return video.fl_frame_transform(_blur, radius)


def unsharp_mask(video: VideoClip, radius=0.5, percent=150, threshold=3):
    """Return a video with an unsharp mask effect."""

    def _mask(frame: np.ndarray, radius=radius, percent=percent, threshold=threshold):
        return np.array(
            Image.fromarray(frame).filter(
                ImageFilter.UnsharpMask(radius, percent, threshold)
            )
        )

    return video.fl_frame_transform(_mask, radius, percent, threshold)


def median_filter(video: VideoClip, size=3):
    """Return a video with a median filter effect."""

    def _filter(frame: np.ndarray, size=size):
        return np.array(Image.fromarray(frame).filter(ImageFilter.MedianFilter(size)))

    return video.fl_frame_transform(_filter, size)


def contrast(video: VideoClip, factor=1.0):
    """Return a video with a contrast effect."""

    def _contrast(frame: np.ndarray, factor=factor):
        enhancer = ImageEnhance.Contrast(Image.fromarray(frame))
        return np.array(enhancer.enhance(factor))

    return video.fl_frame_transform(_contrast, factor)


def brightness(video: VideoClip, factor=1.0):
    """Return a video with a brightness effect."""

    def _brightness(frame: np.ndarray, factor=factor):
        enhancer = ImageEnhance.Brightness(Image.fromarray(frame))
        return np.array(enhancer.enhance(factor))

    return video.fl_frame_transform(_brightness, factor)


def saturation(video: VideoClip, factor=1.0):
    """Return a video with a saturation effect."""

    def _saturation(frame: np.ndarray, factor=factor):
        enhancer = ImageEnhance.Color(Image.fromarray(frame))
        return np.array(enhancer.enhance(factor))

    return video.fl_frame_transform(_saturation, factor)


def sharpness(video: VideoClip, factor=1.0):
    """Return a video with a sharpness effect."""

    def _sharpness(frame: np.ndarray, factor=factor):
        enhancer = ImageEnhance.Sharpness(Image.fromarray(frame))
        return np.array(enhancer.enhance(factor))

    return video.fl_frame_transform(_sharpness, factor)
