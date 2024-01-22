from vidiopy.audio.AudioClip import AudioClip
from vidiopy.audio.fx.accel_decel import accel_decel
import pytest
import numpy as np
import ffmpegio
from vidiopy.audio.AudioClip import AudioFileClip
from rich import print, traceback
traceback.install()

(ffmpegio.set_path(r'D:\soham_code\vidiopy\vidiopy\binary'))


@pytest.fixture()
def audio_clip():
    return AudioClip()


def test_init(audio_clip):
    assert audio_clip
    assert audio_clip.fps is None
    assert audio_clip._original_dur is None
    assert audio_clip._audio_data is None
    assert audio_clip.channels is None
    assert audio_clip._st is None
    assert audio_clip._ed is None


def test_audio_data(audio_clip):
    with pytest.raises(ValueError, match="AudioClip._audio_data is None"):
        audio_clip.audio_data

    audio_data = np.array([1, 2, 3])
    audio_clip.audio_data = audio_data
    assert np.array_equal(audio_clip.audio_data, audio_data)


def test_set_data(audio_clip):
    audio_data = np.array([1, 2, 3])
    audio_clip.set_data(audio_data)
    assert np.array_equal(audio_clip.audio_data, audio_data)


def test_duration(audio_clip):
    assert audio_clip.duration is None

    audio_clip.duration = 10.0
    assert audio_clip.duration == 10.0

    with pytest.raises(AttributeError, match="Not Allowed to set duration"):
        audio_clip.duration = 20.0

    audio_clip.set_duration(30.0)
    assert audio_clip.duration == 30.0


def test_start(audio_clip):
    assert audio_clip.start is None

    audio_clip.start = 2.0
    assert audio_clip.start == 2.0

    audio_clip.set_start(3.0)
    assert audio_clip.start == 3.0


def test_end(audio_clip):
    assert audio_clip.end is None

    audio_clip.end = 10.0
    assert audio_clip.end == 10.0

    audio_clip.set_end(20.0)
    assert audio_clip.end == 20.0


def test_get_frame_at_t(audio_clip):
    audio_clip.fps = 24
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    audio_clip._original_dur = 5.0

    assert np.array_equal(audio_clip.get_frame_at_t(0.0), np.array([1]))
    assert np.array_equal(audio_clip.get_frame_at_t(1.0), np.array([3]))
    assert np.array_equal(audio_clip.get_frame_at_t(2.5), np.array([6]))
    assert np.array_equal(audio_clip.get_frame_at_t(5.0), np.array([]))


def test_iterate_frames_at_fps(audio_clip):
    audio_clip.fps = 24
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    audio_clip._original_dur = 5.0

    frames = list(audio_clip.iterate_frames_at_fps(12))
    assert len(frames) == 3
    assert np.array_equal(frames[0], np.array([1]))
    assert np.array_equal(frames[1], np.array([4]))
    assert np.array_equal(frames[2], np.array([7]))


def test_iterate_all_frames(audio_clip):
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    frames = list(audio_clip.iterate_all_frames())
    assert len(frames) == 5
    assert np.array_equal(frames[0], np.array([1]))
    assert np.array_equal(frames[1], np.array([2]))
    assert np.array_equal(frames[2], np.array([3]))
    assert np.array_equal(frames[3], np.array([4]))
    assert np.array_equal(frames[4], np.array([5]))


def test_fl_frame_transform(audio_clip):
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    audio_clip.fl_frame_transform(lambda frame: frame * 2)
    assert np.array_equal(audio_clip.audio_data, np.array([2, 4, 6, 8, 10]))


def test_fl_clip_transform(audio_clip):
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    audio_clip.fl_clip_transform(lambda clip: clip.set_start(2.0))
    assert audio_clip.start == 2.0


def test_trim_audio_in_place(audio_clip):
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    audio_clip._original_dur = 5.0

    audio_clip.trim_audio_in_place(start=1.0, end=4.0)
    assert np.array_equal(audio_clip.audio_data, np.array([2, 3, 4]))
    assert audio_clip.duration == 3.0


def test_trim_audio(audio_clip):
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    audio_clip._original_dur = 5.0

    trimmed_audio = audio_clip.trim_audio(start=1.0, end=4.0)
    assert np.array_equal(trimmed_audio.audio_data, np.array([2, 3, 4]))
    assert trimmed_audio.duration == 3.0


def test_copy(audio_clip):
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    audio_clip._original_dur = 5.0

    copied_audio = audio_clip.copy()
    assert np.array_equal(copied_audio.audio_data, audio_clip.audio_data)
    assert copied_audio.duration == audio_clip.duration


def test_getitem(audio_clip):
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    audio_clip._original_dur = 5.0

    trimmed_audio = audio_clip[1:4]
    assert np.array_equal(trimmed_audio.audio_data, np.array([2, 3, 4]))
    assert trimmed_audio.duration == 3.0


def test_write_audiofile(audio_clip):
    audio_clip.fps = 24
    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    audio_clip._original_dur = 5.0
    audio_clip.channels = 2

    with pytest.raises(ValueError, match="Frames per second (fps) is not set"):
        audio_clip.write_audiofile("test.wav")

    audio_clip.fps = 24

    with pytest.raises(ValueError, match="Audio data is not set"):
        audio_clip.write_audiofile("test.wav")

    audio_clip._audio_data = np.array([1, 2, 3, 4, 5])
    audio_clip._original_dur = 5.0

    with pytest.raises(ValueError, match="Original duration is not set"):
        audio_clip.write_audiofile("test.wav")

    audio_clip.duration = 5.0

    with pytest.raises(ValueError, match="Channels is not set"):
        audio_clip.write_audiofile("test.wav")

    audio_clip.channels = 2

    with pytest.raises(ValueError, match="File already exists. Please use a different filename or delete the existing file or put `overwrite=True`."):
        audio_clip.write_audiofile("test.wav", overwrite=False)

    audio_clip.write_audiofile("test.wav", overwrite=True)
    # Add assertions for writing audio file


def test_accel_decel():
    audio_clip = AudioClip()
    audio_clip.duration = 10.0

    accelerated_audio = accel_decel(audio_clip, abruptness=0.5)
    assert accelerated_audio.duration == 20.0

    audio_clip.duration = 20.0

    decelerated_audio = accel_decel(audio_clip, abruptness=2.0)
    assert decelerated_audio.duration == 10.0
