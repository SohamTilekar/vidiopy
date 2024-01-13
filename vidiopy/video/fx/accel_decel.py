from pydub import effects


def accel_decel(clip, abruptness=1.0):
    """\
    TODO: Add a Support for Slowing Down Video
    """
    # TODO: Add a Support for Slowing Down Video
    old_dur = clip.duration
    if abruptness <= 0:
        raise
    clip.duration = clip.duration / abruptness
    clip.end = clip.end / abruptness
    if clip.audio:
        clip._sync_audio_video_s_e_d()
        if clip.audio.clip:
            print(abruptness)
            audio = effects.speedup(clip.audio.clip,
                                    playback_speed=abruptness)
            clip.audio.clip = audio
        clip._sync_audio_video_s_e_d()
    return clip
