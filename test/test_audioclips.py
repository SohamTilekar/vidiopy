import tempfile
import os
import numpy as np
from vidiopy.audio.AudioClip import (
    SilenceClip,
    AudioFileClip,
    AudioArrayClip,
    AudioClip,
    concatenate_audioclips,
)


def test_SilenceClip_init():
    duration = 5
    fps = 44100
    channels = 2
    silence_clip = SilenceClip(duration, fps, channels)

    assert silence_clip.fps == fps
    assert silence_clip._original_dur == duration
    assert silence_clip.channels == channels
    assert np.array_equal(
        silence_clip._audio_data, np.zeros((int(duration * fps), channels))
    )


def test_AudioFileClip_init():
    # Arrange
    path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    path.close()
    path = path.name
    SilenceClip(10, 44100, 2).write_audiofile(path, fps=44100)
    duration = 10.0

    try:
        # Act
        audio_clip = AudioFileClip(path, duration)

        assert audio_clip.fps == 44100
        assert audio_clip._original_dur == duration
        assert audio_clip.channels == 2
        assert np.array_equal(
            audio_clip._audio_data, np.zeros((int(duration * 44100), 2))
        )
    finally:
        # Cleanup
        os.remove(path)


def test_AudioArrayClip_init():
    # Arrange
    audio_data = np.array([[1, 2], [3, 4], [5, 6]])
    fps = 44100
    duration = 3.0

    # Act
    audio_clip = AudioArrayClip(audio_data, fps, duration)

    # Assert
    assert audio_clip.fps == fps
    assert audio_clip._original_dur == duration
    assert audio_clip.channels == 2
    assert np.array_equal(audio_clip._audio_data, audio_data)
