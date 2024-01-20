from pydub import effects
from ...audio.AudioClip_native import AudioFileClip
from ...video.VideoClips import VideoClip


def accel_decel(clip: VideoClip, abruptness=1.0):
    if abruptness <= 0:
        raise ValueError("abruptness must be greater than 0")
    if clip.duration is None:
        raise ValueError("clip must have a duration")
    if clip.end is not None:
        clip.end = clip.end / abruptness
    clip.duration = clip.duration / abruptness
    if clip.audio:
        clip._sync_audio_video_s_e_d()
        if clip.audio._original_dur:
            clip.audio._original_dur = clip.audio._original_dur / abruptness
        clip._sync_audio_video_s_e_d()
    return clip
