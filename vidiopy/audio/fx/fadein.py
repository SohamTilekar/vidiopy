from vidiopy.audio.AudioClip import AudioClip
import copy

def fadein(clip: AudioClip, duration: float) -> AudioClip:
    """
    Fades in the audio clip over the specified duration.
    """
    original_get_frame_at_t = copy.copy(clip.get_frame_at_t)

    def new_get_frame_at_t(t: int | float):
        frame = original_get_frame_at_t(t)
        if t < duration:
            return frame * (t / duration)
        return frame

    clip.get_frame_at_t = new_get_frame_at_t
    return clip
