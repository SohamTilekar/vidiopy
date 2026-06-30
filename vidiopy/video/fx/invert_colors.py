from vidiopy.video.VideoClip import VideoClip
import numpy as np
from PIL import Image, ImageOps

def invert_colors(clip: VideoClip) -> VideoClip:
    """
    Inverts the colors of the video clip.
    """
    original_make_frame_array = clip.make_frame_array
    original_make_frame_pil = clip.make_frame_pil

    def modified_make_frame_pil(t):
        img = original_make_frame_pil(t)
        return ImageOps.invert(img.convert("RGB"))

    def modified_make_frame_array(t):
        return np.array(modified_make_frame_pil(t))

    clip.make_frame_array = modified_make_frame_array
    clip.make_frame_pil = modified_make_frame_pil
    return clip
