from vidiopy.audio.AudioClip import AudioClip
import copy

def volumex(clip: AudioClip, factor: float) -> AudioClip:
    """
    Multiplies the volume of the audio clip by a given factor.
    """
    original_get_frame_at_t = copy.copy(clip.get_frame_at_t)

    def new_get_frame_at_t(t: int | float):
        frame = original_get_frame_at_t(t)
        return frame * factor

    clip.get_frame_at_t = new_get_frame_at_t
    return clip
