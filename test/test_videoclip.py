import os
import tempfile
import ffmpegio
import pytest
from fractions import Fraction
from PIL import Image
import numpy as np
from vidiopy import VideoClip, SilenceClip, AudioClip


@pytest.fixture
def vid_clip():
    return VideoClip()


def test_init():
    obj = VideoClip()

    # Check if the superclass is initialized correctly
    assert isinstance(obj, VideoClip)

    # Check the initial values of time-related properties
    assert obj._st == 0.0
    assert obj._ed is None
    assert obj._dur is None

    # Check the initial values of video and audio properties
    assert obj.audio is None
    assert obj.fps is None
    assert obj.size is None

    # Check the initial values of position-related properties
    assert callable(obj.pos)
    assert obj.relative_pos is False


def test_width(vid_clip: VideoClip):
    # Test when size is set
    vid_clip.size = (1920, 1080)
    assert vid_clip.width == 1920

    # Test when size is not set
    vid_clip.size = None
    with pytest.raises(ValueError):
        vid_clip.width


def test_height(vid_clip: VideoClip):
    # Test when size is set
    vid_clip.size = (1920, 1080)
    assert vid_clip.height == 1080

    # Test when size is not set
    vid_clip.size = None
    with pytest.raises(ValueError):
        vid_clip.height


def test_aspect_ratio(vid_clip: VideoClip):
    # Test when size is set
    vid_clip.size = (1920, 1080)
    assert vid_clip.aspect_ratio == Fraction(1920, 1080)

    # Test when size is not set
    vid_clip.size = None
    with pytest.raises(ValueError):
        vid_clip.aspect_ratio


def test_start(vid_clip: VideoClip):
    # Test when start is set
    vid_clip.start = 2.5
    assert vid_clip.start == 2.5

    # Test when start is None
    vid_clip.start = None
    assert vid_clip.start is None

    # Test when start is set and audio exists
    vid_clip.audio = AudioClip()
    vid_clip.start = 1.0
    assert vid_clip.start == 1.0
    assert vid_clip.audio.start == 1.0

    # Test set_start method
    vid_clip.set_start(3.0)
    assert vid_clip.start == 3.0


def test_end(vid_clip: VideoClip):
    # Test when end is set
    vid_clip.end = 5.0
    assert vid_clip.end == 5.0

    # Test when end is None
    vid_clip.end = None
    assert vid_clip.end is None

    # Test when end is set and audio exists
    vid_clip.audio = AudioClip()
    vid_clip.end = 10.0
    assert vid_clip.end == 10.0
    assert vid_clip.audio.end == 10.0

    # Test set_end method
    vid_clip.set_end(7.5)
    assert vid_clip.end == 7.5


def test_duration(vid_clip: VideoClip):
    # Test when duration is set
    vid_clip._dur = 10.0
    assert vid_clip.duration == 10.0

    # Test when duration is None
    vid_clip._dur = None
    assert vid_clip.duration is None

    # Test when duration is set and audio exists
    vid_clip.audio = AudioClip()
    vid_clip._dur = 5.0
    assert vid_clip.duration == 5.0

    # Test set_duration method
    with pytest.raises(ValueError):
        vid_clip.set_duration(15.0)
    with pytest.raises(ValueError):
        vid_clip.duration = 0.0
    assert vid_clip.duration == 5.0


def test_set_pos(vid_clip: VideoClip):
    vid_clip.size = (100, 200)

    vid_clip.set_position((50, 50))
    assert vid_clip.pos(0) == (50, 50)
    assert vid_clip.pos(0.0) == (50, 50)
    assert vid_clip.pos(1) == (50, 50)

    vid_clip.set_position((0.5, 0.5), relative=True)
    assert vid_clip.pos(0) == (50, 100)
    assert vid_clip.pos(0.0) == (50, 100)
    assert vid_clip.pos(1) == (50, 100)

    p = lambda t: ((t + t), t * t)
    vid_clip.set_position(p)
    assert vid_clip.pos(0) == (0, 0)
    assert vid_clip.pos(0.5) == (1, 0)  # not 0.25 because it convert it to int
    assert vid_clip.pos(1) == (2, 1)

    p = lambda t: (0.5, t * t)
    vid_clip.set_position(p, relative=True)
    assert vid_clip.pos(0) == (50, 0)
    assert vid_clip.pos(0.5) == (50, 50)
    assert vid_clip.pos(1) == (50, 200)


def test_set_audio(vid_clip: VideoClip):
    # Test when audio is set
    audio_clip = AudioClip()
    vid_clip.set_audio(audio_clip)
    assert vid_clip.audio == audio_clip
    assert vid_clip.audio.start == vid_clip.start
    assert vid_clip.audio.end == vid_clip.end

    # Test when audio is None
    vid_clip.set_audio(None)
    assert vid_clip.audio is None


def test_without_audio(vid_clip: VideoClip):
    # Test without_audio method
    audio_clip = AudioClip()
    vid_clip.set_audio(audio_clip)
    assert vid_clip.audio is not None
    vid_clip.without_audio()
    assert vid_clip.audio is None


def test_set_fps(vid_clip: VideoClip):
    # Test when fps is set
    vid_clip.set_fps(30)
    assert vid_clip.fps == 30

    # Test when fps is set with float value
    vid_clip.set_fps(29.97)
    assert vid_clip.fps == 29.97

    # Test when fps is set with negative value
    vid_clip.set_fps(0)

    # Test when fps is set with string value
    with pytest.raises(TypeError):
        vid_clip.set_fps("30")  # type: ignore


def test_copy(vid_clip: VideoClip):
    # Create a new instance of VideoClip
    new_clip = vid_clip.copy()

    # Check if the new instance is of the same class
    assert isinstance(new_clip, VideoClip)

    # Check if the new instance is not the same as the original instance
    assert new_clip is not vid_clip

    # Check if the attributes of the new instance are the same as the original instance
    assert new_clip.__dict__ == vid_clip.__dict__

    # Create a new instance of VideoClip
    new_clip = vid_clip.__copy__()

    # Check if the new instance is of the same class
    assert isinstance(new_clip, VideoClip)

    # Check if the new instance is not the same as the original instance
    assert new_clip is not vid_clip

    # Check if the attributes of the new instance are the same as the original instance
    assert new_clip.__dict__ == vid_clip.__dict__


# Test the `make_frame_array` method
def test_make_frame_array(vid_clip: VideoClip):
    with pytest.raises(NotImplementedError):
        vid_clip.make_frame_array(0)


# Test the `make_frame_pil` method
def test_make_frame_pil(vid_clip: VideoClip):
    with pytest.raises(NotImplementedError):
        vid_clip.make_frame_pil(0)


def test_get_frame(vid_clip: VideoClip):
    # Create a dummy image array
    img_arr = np.zeros((100, 100, 3), dtype=np.uint8)

    # Override the `make_frame_array` method to return the dummy image array
    vid_clip.make_frame_array = lambda t: img_arr

    # Override the `make_frame_pil` method to return a PIL Image from the dummy image array
    vid_clip.make_frame_pil = lambda t: Image.fromarray(img_arr)

    # Test `get_frame` method when `is_pil` is None
    x = vid_clip.get_frame(0, is_pil=None)
    assert isinstance(x, np.ndarray) and np.array_equal(x, img_arr.copy())

    # Test `get_frame` method when `is_pil` is False
    y = vid_clip.get_frame(0, is_pil=False)
    assert isinstance(y, np.ndarray) and np.array_equal(y, img_arr.copy())

    # Test `get_frame` method when `is_pil` is True
    z = vid_clip.get_frame(0, is_pil=True)
    assert isinstance(z, Image.Image) and np.array_equal(np.array(z), img_arr.copy())


def test_iterate_frames_pil_t(vid_clip: VideoClip):
    # Test when end is set
    vid_clip.end = 1
    vid_clip.make_frame_pil = lambda t: Image.new("RGB", (100, 100))
    frames = tuple(vid_clip.iterate_frames_pil_t(30))
    assert len(frames) == 31
    assert all(isinstance(frame, Image.Image) for frame in frames)

    # Test when duration is set
    vid_clip.end = None
    vid_clip._dur = 1
    frames = tuple(vid_clip.iterate_frames_pil_t(30))
    assert len(frames) == 31
    assert all(isinstance(frame, Image.Image) for frame in frames)

    # Test when neither end nor duration is set
    vid_clip.end = None
    vid_clip._dur = None
    with pytest.raises(ValueError):
        tuple(vid_clip.iterate_frames_pil_t(30))


def test_iterate_frames_array_t(vid_clip: VideoClip):
    # Test when end is set
    vid_clip.end = 1
    vid_clip.make_frame_array = lambda t: np.zeros((100, 100, 3), dtype=np.uint8)
    frames = tuple(vid_clip.iterate_frames_array_t(30))
    assert len(frames) == 31
    assert all(isinstance(frame, np.ndarray) for frame in frames)
    assert all(frame.shape == (100, 100, 3) for frame in frames)

    # Test when duration is set
    vid_clip.end = None
    vid_clip._dur = 1
    frames = tuple(vid_clip.iterate_frames_array_t(30))
    assert len(frames) == 31
    assert all(isinstance(frame, np.ndarray) for frame in frames)
    assert all(frame.shape == (100, 100, 3) for frame in frames)

    # Test when neither end nor duration is set
    vid_clip.end = None
    vid_clip._dur = None
    with pytest.raises(ValueError):
        tuple(vid_clip.iterate_frames_array_t(30))


def test_time_transform(vid_clip: VideoClip):
    vid_clip.make_frame_array = lambda t: t * t
    vid_clip.make_frame_pil = lambda t: t + t
    t_timp = lambda t: t + 1
    assert vid_clip.make_frame_array(1) == 1
    assert vid_clip.make_frame_pil(1) == 2
    vid_clip.fl_time_transform(t_timp)
    assert vid_clip.make_frame_array(1) == 4
    assert vid_clip.make_frame_pil(1) == 4


def test_sync_audio_video_s_e_d(vid_clip: VideoClip):
    # Set the start, end, and duration of the clip
    vid_clip.start = 1
    vid_clip.end = 2
    vid_clip._dur = 1

    # Set the audio of the clip
    vid_clip.audio = AudioClip()

    # Call the method to synchronize the audio and video
    vid_clip._sync_audio_video_s_e_d()

    # Check if the start, end, and duration of the audio match the video
    assert vid_clip.audio.start == vid_clip.start
    assert vid_clip.audio.end == vid_clip.end
    assert vid_clip.audio._original_dur == vid_clip.duration


def write_videofile(vid_clip: VideoClip):
    vid_clip.set_end(1)
    vid_clip.set_fps(5)
    vid_clip.make_frame_array = lambda t: np.zeros((100, 100, 3), dtype=np.uint8)
    pth = ""
    try:
        pth = tempfile.NamedTemporaryFile(suffix=".mp4", delete=True).name
        vid_clip.write_videofile(pth, audio=False)
    except Exception as e:
        raise e
    finally:
        if os.path.exists(pth) and pth:
            os.remove(pth)
    assert ffmpegio.video.read(pth)[1][0] == vid_clip.make_frame_array(0)
    assert len(ffmpegio.video.read(pth)[1]) == 6


def write_videofile_audio(vid_clip: VideoClip):
    vid_clip.set_end(1)
    vid_clip.set_fps(5)
    vid_clip.make_frame_array = lambda t: np.zeros((100, 100, 3), dtype=np.uint8)
    vid_clip.audio = SilenceClip(vid_clip.end, 44100, 2)
    pth = ""
    try:
        pth = tempfile.NamedTemporaryFile(suffix=".mp4", delete=True).name
        vid_clip.write_videofile(pth, audio=True)
    except Exception as e:
        raise e
    finally:
        if os.path.exists(pth) and pth:
            os.remove(pth)
    assert ffmpegio.video.read(pth)[1][0] == vid_clip.make_frame_array(0)
    assert len(ffmpegio.video.read(pth)[1]) == 6
    assert ffmpegio.probe.audio_streams_basic(pth)
