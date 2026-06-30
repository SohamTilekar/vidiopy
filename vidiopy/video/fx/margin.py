from vidiopy.video.VideoClip import VideoClip
import numpy as np
from PIL import Image, ImageOps

def margin(clip: VideoClip, top: int = 0, right: int = 0, bottom: int = 0, left: int = 0, color: tuple[int, int, int] = (0, 0, 0)) -> VideoClip:
    """
    Adds a margin around the video clip.
    """
    original_make_frame_array = clip.make_frame_array
    original_make_frame_pil = clip.make_frame_pil

    def modified_make_frame_pil(t):
        img = original_make_frame_pil(t)
        return ImageOps.expand(img, border=(left, top, right, bottom), fill=color)

    def modified_make_frame_array(t):
        return np.array(modified_make_frame_pil(t))

    clip.make_frame_array = modified_make_frame_array
    clip.make_frame_pil = modified_make_frame_pil
    if clip.size is not None:
        clip.size = (clip.size[0] + left + right, clip.size[1] + top + bottom)
    return clip
