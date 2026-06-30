from vidiopy.video.VideoClip import VideoClip

def time_mirror(clip: VideoClip) -> VideoClip:
    """
    Returns a clip that plays the current clip backwards.
    """
    if clip.duration is None:
        raise ValueError("time_mirror requires a clip with a defined duration.")
    
    return clip.fl_time_transform(lambda t: clip.duration - t)
