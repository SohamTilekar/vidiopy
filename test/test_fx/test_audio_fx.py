import pytest
import numpy as np
from vidiopy.audio.AudioClip import AudioClip
from vidiopy.audio.fx import volumex, fadein, fadeout, audio_loop

@pytest.fixture
def base_audio():
    # A simple AudioClip mock that returns constant 1.0 array
    clip = AudioClip()
    clip.fps = 44100
    clip.duration = 5
    clip._st = 0
    clip._ed = 5
    def mock_get_frame_at_t(t):
        return np.ones((2, 1024))
    clip.get_frame_at_t = mock_get_frame_at_t
    return clip

def test_volumex(base_audio):
    quiet = volumex(base_audio, 0.5)
    frame = quiet.get_frame_at_t(1)
    assert np.all(frame == 0.5)

def test_audio_fadein(base_audio):
    faded = fadein(base_audio, duration=2)
    # At t=1, factor should be 1/2 = 0.5
    frame1 = faded.get_frame_at_t(1)
    assert np.all(frame1 == 0.5)
    # At t=3, factor should be 1.0
    frame3 = faded.get_frame_at_t(3)
    assert np.all(frame3 == 1.0)

def test_audio_fadeout(base_audio):
    faded = fadeout(base_audio, duration=2)
    # At t=4, time_left is 1, so factor should be 1/2 = 0.5
    frame4 = faded.get_frame_at_t(4)
    assert np.all(frame4 == 0.5)

def test_audio_loop(base_audio):
    looped = audio_loop(base_audio, n=2)
    assert looped.duration == 10
    looped_dur = audio_loop(base_audio, duration=7)
    assert looped_dur.duration == 7
