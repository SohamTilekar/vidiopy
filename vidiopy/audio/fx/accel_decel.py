from ..AudioClip import AudioClip


def accel_decel(audio: AudioClip, abruptness=1.0) -> AudioClip:
    if audio.duration is None:
        raise ValueError("Audio duration is not set")
    audio._original_dur = audio.duration / abruptness
    return audio
