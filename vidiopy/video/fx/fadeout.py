from vidiopy.video.VideoClip import VideoClip
import numpy as np
from PIL import Image

def fadeout(clip: VideoClip, duration: float, final_color: tuple[int, int, int] = (0, 0, 0)) -> VideoClip:
    """
    Fades out the clip over the specified duration at the end of the clip.
    Requires the clip to have a defined duration.
    """
    if clip.duration is None:
        raise ValueError("fadeout requires a clip with a defined duration.")

    original_make_frame_array = clip.make_frame_array
    original_make_frame_pil = clip.make_frame_pil

    def modified_make_frame_array(t):
        frame = original_make_frame_array(t)
        time_left = clip.duration - t
        if time_left < duration and time_left >= 0:
            factor = time_left / duration
            if final_color == (0, 0, 0):
                frame = (frame * factor).astype(np.uint8)
            else:
                bg = np.full_like(frame, final_color, dtype=np.float32)
                frame = (frame * factor + bg * (1 - factor)).astype(np.uint8)
        return frame

    def modified_make_frame_pil(t):
        arr = modified_make_frame_array(t)
        return Image.fromarray(arr)

    clip.make_frame_array = modified_make_frame_array
    clip.make_frame_pil = modified_make_frame_pil
    return clip
