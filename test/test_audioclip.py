import os
import tempfile
import ffmpegio
import pytest
from vidiopy.audio.AudioClip import AudioClip
import numpy as np


def test_AudioClip_init():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Verify the instance variables
    assert clip.fps == 30
    assert clip._original_dur == 10.0
    assert clip._audio_data is None
    assert clip.channels is None
    assert clip._st == 0.0
    assert clip._ed == 10.0


def test_AudioClip_eq():
    # Create two instances of AudioClip with the same properties
    clip1 = AudioClip(duration=10.0, fps=30)
    clip2 = AudioClip(duration=10.0, fps=30)

    # Verify that the instances are equal
    assert clip1 == clip2

    assert clip1 != clip2.set_duration(5.0)


def test_AudioClip_set_data():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Create an audio data array
    audio_data = np.array([1, 2, 3, 4, 5])

    # Set the audio data using the set_data method
    clip.set_data(audio_data)

    # Verify that the audio data is set correctly
    assert np.array_equal(clip.audio_data, audio_data)


def test_AudioClip_set_fps():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Set the fps using the set_fps method
    clip.set_fps(60)

    # Verify that the fps is set correctly
    assert clip.fps == 60


def test_AudioClip_get_duration():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Get the duration using the get_duration method
    duration = clip.get_duration

    # Verify that the duration is correct
    assert duration == 10.0


def test_AudioClip_set_duration():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Set the duration using the set_duration method
    clip.set_duration(5.0)

    # Verify that the duration is set correctly
    assert clip.get_duration == 5.0


def test_AudioClip_start_end():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Set the start and end values using the set_start and set_end methods
    clip.set_start(2.0)
    clip.set_end(8.0)

    # Verify that the start and end values are set correctly
    assert clip.start == 2.0
    assert clip.end == 8.0


def test_AudioClip_get_frame_at_t():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Set the audio data
    audio_data = np.array([1, 2, 3, 4, 5])
    clip.set_data(audio_data)

    # Set the start and end values
    clip.set_start(2.0)
    clip.set_end(8.0)

    # Get the frame at time t
    frame = clip.get_frame_at_t(4.0)

    # Verify that the frame is correct
    assert frame == 2

    # Test with t outside the duration
    with pytest.raises(IndexError):
        clip.get_frame_at_t(11.0)

    # Test with fps not set
    clip.fps = None
    with pytest.raises(ValueError):
        clip.get_frame_at_t(4.0)

    # Test with audio data not set
    clip.set_data(None)
    with pytest.raises(ValueError):
        clip.get_frame_at_t(4.0)

    # Test with duration not set
    clip.set_data(audio_data)
    clip._original_dur = None
    with pytest.raises(ValueError):
        clip.get_frame_at_t(4.0)


def test_AudioClip_iterate_frames_at_fps():
    clip = AudioClip()

    # Set the audio data

    with pytest.raises(ValueError):
        for frame in clip.iterate_frames_at_fps():
            pass

    clip.set_fps(2)

    with pytest.raises(ValueError):
        for frame in clip.iterate_frames_at_fps(2):
            pass

    audio_data = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
    clip.set_data(audio_data)

    with pytest.raises(ValueError):
        for frame in clip.iterate_frames_at_fps():
            pass

    clip.set_duration(1)

    for frame in clip.iterate_frames_at_fps():
        assert frame in audio_data

    for frame in clip.iterate_frames_at_fps(2):
        assert frame in audio_data

    assert np.array_equal(
        np.array([frame for frame in clip.iterate_frames_at_fps(10)]), audio_data
    )


def test_AudioClip_iterate_all_frames():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Set the audio data
    audio_data = np.array([1, 2, 3, 4, 5])
    clip.set_data(audio_data)

    # Iterate over all frames
    frames = [frame for frame in clip.iterate_all_frames()]

    # Verify that all frames are present
    assert np.array_equal(frames, audio_data)

    clip._audio_data = None
    with pytest.raises(ValueError):
        for frame in clip.iterate_all_frames():
            pass


def test_AudioClip_fl_frame_transform():
    # Create an instance of AudioClip
    clip = AudioClip()

    # Test when self._audio_data is not set
    with pytest.raises(ValueError):
        clip.fl_frame_transform(lambda x: x)

    # Create an audio data array
    audio_data = np.array([[1, 2], [3, 4], [5, 6]])
    clip.set_data(audio_data)

    # Test when a function is applied to each frame of the audio data
    clip.fl_frame_transform(lambda frame: frame * 2)
    assert np.array_equal(clip._audio_data, np.array([[2, 4], [6, 8], [10, 12]]))


def test_AudioClip_fl_clip_transform():
    # Create an instance of AudioClip
    clip = AudioClip()

    # Test when self._audio_data is not set
    with pytest.raises(ValueError):
        clip.fl_clip_transform(lambda x: x)

    # Create an audio data array
    audio_data = np.array([[1, 2], [3, 4], [5, 6]])
    clip.set_data(audio_data)

    # Test when a function is applied to the entire audio data
    def multiply_data(clip, factor):
        clip._audio_data *= factor

    clip.fl_clip_transform(multiply_data, 2)
    assert np.array_equal(clip._audio_data, np.array([[2, 4], [6, 8], [10, 12]]))


def test_AudioClip_sub_clip():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0)

    # Test when self._audio_data is not set
    with pytest.raises(ValueError):
        clip.sub_clip()

    # Create an audio data array
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)

    # Test when self.duration is not set
    clip._original_dur = None
    with pytest.raises(ValueError):
        clip.sub_clip()

    # Test when neither start nor end is provided
    clip = AudioClip(duration=10.0)
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)
    clip._original_dur = 10.0
    clip.sub_clip()
    assert np.array_equal(clip._audio_data, audio_data)

    # Test when only start is provided
    clip = AudioClip(duration=10.0)
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)
    clip.set_data(audio_data)
    clip.sub_clip(start=2)
    assert np.array_equal(clip._audio_data, np.array([3, 4, 5, 6, 7, 8, 9, 10]))

    # Test when only end is provided
    clip = AudioClip(duration=10.0)
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)
    clip.set_data(audio_data)
    clip.sub_clip(end=8)
    assert np.array_equal(clip._audio_data, np.array([1, 2, 3, 4, 5, 6, 7, 8]))

    # Test when both start and end are provided
    clip = AudioClip(duration=10.0)
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)
    clip.set_data(audio_data)
    clip.sub_clip(start=2, end=8)
    assert np.array_equal(clip._audio_data, np.array([3, 4, 5, 6, 7, 8]))

    # Test when end is greater than self.duration
    with pytest.raises(ValueError):
        clip.sub_clip(end=11)


def test_AudioClip_sub_clip_copy():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0)

    # Test when self._audio_data is not set
    with pytest.raises(ValueError):
        clip.sub_clip_copy()

    # Create an audio data array
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)

    # Test when self.duration is not set
    clip._original_dur = None
    with pytest.raises(ValueError):
        clip.sub_clip_copy()

    # Test when neither start nor end is provided
    clip = AudioClip(duration=10.0)
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)
    clip._original_dur = 10.0
    sub_clip = clip.sub_clip_copy()
    assert np.array_equal(sub_clip._audio_data, audio_data)

    # Test when only start is provided
    clip = AudioClip(duration=10.0)
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)
    sub_clip = clip.sub_clip_copy(start=2)
    assert np.array_equal(sub_clip._audio_data, np.array([3, 4, 5, 6, 7, 8, 9, 10]))

    # Test when only end is provided
    clip = AudioClip(duration=10.0)
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)
    sub_clip = clip.sub_clip_copy(end=8)
    assert np.array_equal(sub_clip._audio_data, np.array([1, 2, 3, 4, 5, 6, 7, 8]))

    # Test when both start and end are provided
    clip = AudioClip(duration=10.0)
    audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clip.set_data(audio_data)
    sub_clip = clip.sub_clip_copy(start=2, end=8)
    assert np.array_equal(sub_clip._audio_data, np.array([3, 4, 5, 6, 7, 8]))

    # Test when end is greater than self.duration
    with pytest.raises(ValueError):
        clip.sub_clip_copy(end=11)


def test_AudioClip_write_audiofile():
    # Create an instance of AudioClip
    clip = AudioClip(duration=10.0, fps=30)

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_file.close()
    temp_file = temp_file.name

    try:
        # Test when self._audio_data is not set
        with pytest.raises(ValueError):
            clip.write_audiofile(temp_file)

        # Create an audio data array
        audio_data = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
        clip.channels = 1
        clip.set_data(audio_data)

        # Test when fps is not set
        clip.fps = None
        with pytest.raises(ValueError):
            clip.write_audiofile(temp_file)

        # Test when self.duration and self.end are not set
        clip.fps = 30
        clip._original_dur = None
        clip.end = None
        with pytest.raises(ValueError):
            clip.write_audiofile(temp_file)

        # Test when self.channels is not set
        clip._original_dur = 10.0
        clip.channels = None
        with pytest.raises(ValueError):
            clip.write_audiofile(temp_file)

        # Test successful write
        clip.channels = 1
        clip.write_audiofile(temp_file)
        assert os.path.exists(temp_file)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_write_audioclip():
    clip = AudioClip(duration=1, fps=44100)
    clip.set_data(np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]))
    clip.channels = 1

    fname = ""
    try:
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        fname = temp_file.name
        temp_file.close()
        clip.write_audiofile(fname)
        assert os.path.exists(fname)
        assert ffmpegio.probe.audio_streams_basic(fname)[0]["duration"] == 1
        assert ffmpegio.audio.read(fname)[1].shape == (44100, 1)
    finally:
        if fname:
            os.remove(fname)
