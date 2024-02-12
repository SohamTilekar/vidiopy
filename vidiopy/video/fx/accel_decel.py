from typing import Callable

from vidiopy.video.VideoClip import VideoClip


def accel_decel(
    clip: VideoClip,
    new_duration: Callable[[int | float], int | float] | float | int | None = None,
    ratio: int | float = 1,
):
    if new_duration is None and ratio == 1:
        ...
    elif ratio != 1:
        if clip.duration is not None:
            new_dur = ratio * clip.duration
            new_end = ratio * clip.end if clip.end else None
            new_start = ratio * clip.start
            clip.start = new_start
            clip.end = new_end
            clip._dur = new_dur
        else:
            raise ValueError("Clip Duration is Not Set")
    elif new_duration is not None:
        if callable(new_duration):
            clip.fl_time_transform(new_duration)
        elif isinstance(new_duration, (int, float)):
            if clip._dur is not None:
                clip.start = new_duration / clip._dur * clip.start
                clip.end = (
                    (new_duration / clip._dur * clip.end)
                    if clip.end is not None
                    else None
                )
                clip._dur = new_duration
            else:
                raise ValueError("Clip Duration is Not Set")
    clip._sync_audio_video_s_e_d()
    return clip
