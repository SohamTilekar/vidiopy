from vidiopy.video.VideoClip import VideoClip
import numpy as np
from PIL import Image

def resize(clip: VideoClip, new_size: tuple[int, int] = None, height: int = None, width: int = None) -> VideoClip:
    """
    Returns a video clip that is resized to the specified size.
    """
    if new_size is not None:
        size = new_size
    elif height is not None and clip.size is not None:
        size = (int(clip.size[0] * (height / clip.size[1])), height)
    elif width is not None and clip.size is not None:
        size = (width, int(clip.size[1] * (width / clip.size[0])))
    else:
        raise ValueError("Must provide either new_size, height, or width.")
    
    original_make_frame_array = clip.make_frame_array
    original_make_frame_pil = clip.make_frame_pil

    def modified_make_frame_array(t):
        frame = original_make_frame_array(t)
        img = Image.fromarray(frame)
        return np.array(img.resize(size, Image.Resampling.LANCZOS))

    def modified_make_frame_pil(t):
        img = original_make_frame_pil(t)
        return img.resize(size, Image.Resampling.LANCZOS)

    clip.make_frame_array = modified_make_frame_array
    clip.make_frame_pil = modified_make_frame_pil
    clip.size = size
    return clip
