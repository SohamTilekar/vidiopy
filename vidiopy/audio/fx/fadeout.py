from vidiopy.audio.AudioClip import AudioClip
import copy

def fadeout(clip: AudioClip, duration: float) -> AudioClip:
    """
    Fades out the audio clip over the specified duration at the end of the clip.
    """
    if clip.duration is None:
        raise ValueError("fadeout requires a clip with a defined duration.")

    original_get_frame_at_t = copy.copy(clip.get_frame_at_t)

    def new_get_frame_at_t(t: int | float):
        frame = original_get_frame_at_t(t)
        time_left = clip.duration - t
        if time_left < duration and time_left >= 0:
            return frame * (time_left / duration)
        return frame

    clip.get_frame_at_t = new_get_frame_at_t
    return clip
