from vidiopy.audio.AudioClip import AudioClip

def audio_loop(clip: AudioClip, n: int = None, duration: float = None) -> AudioClip:
    """
    Returns an audio clip that loops the current clip.
    """
    if clip.duration is None:
        raise ValueError("audio_loop requires a clip with a defined duration.")
    
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
