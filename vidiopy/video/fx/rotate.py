from vidiopy.video.VideoClip import VideoClip
import numpy as np
from PIL import Image

def rotate(clip: VideoClip, angle: float, resample: Image.Resampling = Image.Resampling.BICUBIC, expand: bool = False) -> VideoClip:
    """
    Rotates the video clip by the given angle (in degrees).
    """
    original_make_frame_array = clip.make_frame_array
    original_make_frame_pil = clip.make_frame_pil

    def modified_make_frame_pil(t):
        img = original_make_frame_pil(t)
        return img.rotate(angle, resample=resample, expand=expand)

    def modified_make_frame_array(t):
        return np.array(modified_make_frame_pil(t))

    clip.make_frame_array = modified_make_frame_array
    clip.make_frame_pil = modified_make_frame_pil
    
    if expand:
        # We need to compute the new size
        # A simple way is to process one frame and get its size
        try:
            sample_img = original_make_frame_pil(0)
            clip.size = sample_img.rotate(angle, resample=resample, expand=expand).size
        except Exception:
            pass
            
    return clip
