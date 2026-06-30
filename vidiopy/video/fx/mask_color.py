from vidiopy.video.VideoClip import VideoClip
import numpy as np
from PIL import Image

def mask_color(clip: VideoClip, color: tuple[int, int, int], threshold: int = 10) -> VideoClip:
    """
    Returns a video clip where the specified color is made transparent (Chroma Key).
    """
    original_make_frame_array = clip.make_frame_array
    original_make_frame_pil = clip.make_frame_pil

    def process_array(frame):
        if frame.shape[2] == 3:
            rgba = np.concatenate([frame, np.full((frame.shape[0], frame.shape[1], 1), 255, dtype=np.uint8)], axis=2)
        else:
            rgba = frame.copy()
            
        r, g, b = color
        
        dist = np.sqrt(
            (rgba[:, :, 0].astype(np.int32) - r) ** 2 +
            (rgba[:, :, 1].astype(np.int32) - g) ** 2 +
            (rgba[:, :, 2].astype(np.int32) - b) ** 2
        )
        
        rgba[:, :, 3] = np.where(dist < threshold, 0, rgba[:, :, 3])
        return rgba

    def modified_make_frame_array(t):
        frame = original_make_frame_array(t)
        return process_array(frame)

    def modified_make_frame_pil(t):
        arr = modified_make_frame_array(t)
        return Image.fromarray(arr, mode="RGBA")

    clip.make_frame_array = modified_make_frame_array
    clip.make_frame_pil = modified_make_frame_pil
    return clip
