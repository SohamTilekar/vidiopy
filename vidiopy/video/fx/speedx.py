from vidiopy.video.VideoClip import VideoClip

def speedx(clip: VideoClip, factor: float) -> VideoClip:
    """
    Returns a new clip playing `factor` times faster than the original.
    """
    if factor <= 0:
        raise ValueError("speedx factor must be positive.")
    
    new_clip = clip.fl_time_transform(lambda t: t * factor)
    
    if new_clip.duration is not None:
        new_clip.duration /= factor
    if new_clip.end is not None:
        new_clip.end = (new_clip.start if new_clip.start else 0) + new_clip.duration
        
    return new_clip
