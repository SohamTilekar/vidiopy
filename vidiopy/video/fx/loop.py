from vidiopy.video.VideoClip import VideoClip

def loop(clip: VideoClip, n: int = None, duration: float = None) -> VideoClip:
    """
    Returns a clip that loops the current clip.
    If `n` is provided, loops the clip `n` times.
    If `duration` is provided, loops the clip until it reaches `duration`.
    If neither is provided, loops infinitely.
    """
    if clip.duration is None:
        raise ValueError("loop requires a clip with a defined duration.")
    
    new_clip = clip.fl_time_transform(lambda t: t % clip.duration)
    
    if duration is not None:
        new_clip.duration = duration
    elif n is not None:
        new_clip.duration = clip.duration * n
    else:
        new_clip.duration = None
        
    if new_clip.duration is not None:
        new_clip.end = (new_clip.start if new_clip.start else 0) + new_clip.duration
    else:
        new_clip.end = None
    
    return new_clip
