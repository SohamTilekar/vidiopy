from vidiopy.video.VideoClip import VideoClip
import numpy as np
from PIL import Image, ImageOps

def blackwhite(clip: VideoClip) -> VideoClip:
    """
    Converts the video clip to grayscale (black and white).
    """
    original_make_frame_array = clip.make_frame_array
    original_make_frame_pil = clip.make_frame_pil

    def modified_make_frame_pil(t):
        img = original_make_frame_pil(t)
        return ImageOps.grayscale(img).convert("RGB") # Keep RGB format

    def modified_make_frame_array(t):
        return np.array(modified_make_frame_pil(t))

    clip.make_frame_array = modified_make_frame_array
    clip.make_frame_pil = modified_make_frame_pil
    return clip
