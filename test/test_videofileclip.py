import pytest
import numpy as np
import numpy.typing as npt
from PIL import Image, ImageFilter
import os
import ffmpegio
import tempfile
from vidiopy import VideoFileClip, AudioClip


@pytest.fixture
def file_clip_no_audio():
    fil = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    clip = np.asarray(
        tuple(Image.new("RGB", (100, 100)) for _ in range(5)), dtype=np.uint8
    )
    print(clip)
    print(clip.shape)
    print(clip[0].shape)
    ffmpegio.video.write(fil, 5, clip, overwrite=True)
    yield VideoFileClip(fil, audio=False)
    os.remove(fil)


@pytest.fixture
def file_clip():
    fil = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    # making a 5 frame 100 100 video with 3 channels RGB, 8 per pixel, using numpy with random values
    clip = np.asarray(
        tuple(Image.new("RGB", (100, 100)) for _ in range(5)), dtype=np.uint8
    )
    ffmpegio.video.write(fil, 5, clip, overwrite=True)
    yield VideoFileClip(fil)
    os.remove(fil)


def test_init_no_audio(file_clip_no_audio: VideoFileClip):
    # Assert the attributes are set correctly
    assert file_clip_no_audio.filename
    assert isinstance(file_clip_no_audio.clip, np.ndarray)
    assert isinstance(file_clip_no_audio.clip[0], np.ndarray)
    assert file_clip_no_audio.clip.shape == (5, 100, 100, 3)
    assert file_clip_no_audio.fps == 5
    assert file_clip_no_audio.size == (100, 100)
    assert file_clip_no_audio.start == 0.0
    assert file_clip_no_audio.end == 1
    assert file_clip_no_audio._dur == 1

    assert file_clip_no_audio.audio is None


def test_init_audio(file_clip):
    # Assert the attributes are set correctly
    assert file_clip.filename
    assert isinstance(file_clip.clip, np.ndarray)
    assert isinstance(file_clip.clip[0], np.ndarray)
    assert file_clip.clip.shape == (5, 100, 100, 3)
    assert file_clip.fps == 5
    assert file_clip.size == (100, 100)
    assert file_clip.start == 0.0
    assert file_clip.end == 1
    assert file_clip._dur == 1

    assert file_clip.audio is not None
    assert isinstance(file_clip.audio, AudioClip)


def test_frame_transform(file_clip: VideoFileClip):
    # Define a transformation function
    def transform_func(frame: npt.NDArray):
        # Apply some transformation to the frame
        frame = np.array(Image.fromarray(frame).filter(ImageFilter.ModeFilter))
        return frame

    # Apply the transformation to the file clip
    old_clip = file_clip.copy()
    transformed_clip = file_clip.fl_frame_transform(transform_func)

    assert transformed_clip is file_clip
    assert transformed_clip is not old_clip
    assert isinstance(transformed_clip, VideoFileClip)
    assert transformed_clip.clip is not old_clip.clip
    assert np.array_equal(
        transformed_clip.clip[0],
        np.array(Image.fromarray(old_clip.clip[0]).filter(ImageFilter.ModeFilter)),
    )
    assert np.array_equal(
        transformed_clip.clip[1],
        np.array(Image.fromarray(old_clip.clip[1]).filter(ImageFilter.ModeFilter)),
    )
    assert np.array_equal(
        transformed_clip.clip[-1],
        np.array(Image.fromarray(old_clip.clip[-1]).filter(ImageFilter.ModeFilter)),
    )
    assert isinstance(transformed_clip.clip, np.ndarray)
    assert isinstance(transformed_clip.clip[0], np.ndarray)
    assert transformed_clip.clip.shape == (5, 100, 100, 3)
    assert transformed_clip.fps == 5
    assert transformed_clip.size == (100, 100)
    assert transformed_clip.start == 0.0
    assert transformed_clip.end == 1
    assert transformed_clip._dur == 1
    assert transformed_clip.audio is not None
    assert isinstance(transformed_clip.audio, AudioClip)


def test_clip_transform(file_clip: VideoFileClip):
    old_clip = file_clip.copy()

    # Define a transformation function
    def transform_func(frame: npt.NDArray[np.uint8], frame_time: float):
        # Apply some transformation to the frame
        # For example, resize the frame
        resized_frame = np.array(Image.fromarray(frame).resize((200, 200)))
        return resized_frame

    # Apply the transformation to the file clip
    transformed_clip = file_clip.fl_clip_transform(transform_func)

    assert transformed_clip is file_clip
    assert isinstance(transformed_clip, VideoFileClip)
    assert not np.array_equal(transformed_clip.clip, old_clip.clip)
    assert isinstance(transformed_clip.clip, np.ndarray)
    assert isinstance(transformed_clip.clip[0], np.ndarray)
    assert transformed_clip.clip.shape == (5, 200, 200, 3)
    assert transformed_clip.fps == 5
    assert transformed_clip.start == 0.0
    assert transformed_clip.end == 1
    assert transformed_clip._dur == 1
    assert transformed_clip.audio is not None
    assert isinstance(transformed_clip.audio, AudioClip)


def test_fx(file_clip: VideoFileClip):
    # Define a mock effect function
    def mock_effect_func(clip: VideoFileClip, *args, **kwargs):
        # Apply some mock effect to the clip
        # For example, change the clip duration
        clip._dur = 2
        return clip

    # Apply the effect function to the file clip
    old_clip = file_clip.copy()
    transformed_clip = file_clip.fx(mock_effect_func)

    assert transformed_clip is not old_clip
    assert isinstance(transformed_clip, VideoFileClip)
    assert transformed_clip._dur == 2
    assert transformed_clip.filename == old_clip.filename
    assert np.array_equal(transformed_clip.clip, old_clip.clip)
    assert transformed_clip.fps == old_clip.fps
    assert transformed_clip.size == old_clip.size
    assert transformed_clip.start == old_clip.start
    assert transformed_clip.end == old_clip.end
    assert transformed_clip.audio == old_clip.audio
    assert transformed_clip.audio is not None
    assert isinstance(transformed_clip.audio, AudioClip)


def test_sub_clip(file_clip: VideoFileClip):
    assert file_clip is file_clip.sub_clip()
    sub_clip = file_clip.sub_clip(t_start=0.5)
    assert sub_clip.end == 1
    assert sub_clip.duration == 0.5
    assert sub_clip.audio is not None
    assert isinstance(sub_clip.audio, AudioClip)
    assert sub_clip.audio.end == 1
    assert sub_clip.audio.duration == 0.5


def test_sub_clip_copy(file_clip: VideoFileClip):
    # testing method sub_clip_copy
    assert file_clip is not file_clip.sub_clip_copy()
    assert file_clip == file_clip.sub_clip_copy()
    sub_clip_copy = file_clip.sub_clip_copy(t_start=0.5)
    assert sub_clip_copy is not file_clip
    assert sub_clip_copy.end == 1
    assert sub_clip_copy.duration == 0.5
    assert sub_clip_copy.audio is not None
    assert isinstance(sub_clip_copy.audio, AudioClip)
    assert sub_clip_copy.audio.end == 1
    assert sub_clip_copy.audio.duration == 0.5


def test_make_frame_array(file_clip: VideoFileClip):
    # Test with duration set
    file_clip._dur = 1  # set duration
    t = 0.2  # time for which we want the frame
    expected_frame_index = int(t / (file_clip._dur / len(file_clip.clip)))
    expected_frame = np.array(file_clip.clip[expected_frame_index])
    assert np.array_equal(file_clip.make_frame_array(t), expected_frame)

    # Test without duration set
    file_clip._dur = None  # unset duration
    with pytest.raises(ValueError):
        file_clip.make_frame_array(t)


def test_make_frame_pil(file_clip: VideoFileClip):
    # Test with duration set
    file_clip._dur = 1  # set duration
    t = 0.2  # time for which we want the frame
    expected_frame_index = int(t / (file_clip._dur / len(file_clip.clip)))
    expected_frame = Image.fromarray(file_clip.clip[expected_frame_index])
    assert isinstance(file_clip.make_frame_pil(t), Image.Image)
    assert file_clip.make_frame_pil(t) == expected_frame

    # Test without duration set
    file_clip._dur = None  # unset duration
    with pytest.raises(ValueError):
        file_clip.make_frame_pil(t)


if __name__ == "__main__":
    pytest.main([__file__])
