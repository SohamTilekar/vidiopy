from vidiopy.video.VideoClip import VideoClip
import numpy as np
from PIL import Image

def fadein(clip: VideoClip, duration: float, initial_color: tuple[int, int, int] = (0, 0, 0)) -> VideoClip:
    """
    Fades in the clip over the specified duration.
    """
    original_make_frame_array = clip.make_frame_array
    original_make_frame_pil = clip.make_frame_pil

    def modified_make_frame_array(t):
        frame = original_make_frame_array(t)
        if t < duration:
            factor = t / duration
            if initial_color == (0, 0, 0):
                frame = (frame * factor).astype(np.uint8)
            else:
                bg = np.full_like(frame, initial_color, dtype=np.float32)
                frame = (frame * factor + bg * (1 - factor)).astype(np.uint8)
        return frame

    def modified_make_frame_pil(t):
        arr = modified_make_frame_array(t)
        return Image.fromarray(arr)

    clip.make_frame_array = modified_make_frame_array
    clip.make_frame_pil = modified_make_frame_pil
    return clip
