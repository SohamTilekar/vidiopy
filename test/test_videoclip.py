import pytest
from vidiopy import VideoClip
from PIL import Image, ImageChops
from vidiopy import AudioClip, SilenceClip
from fractions import Fraction
import numpy as np


@pytest.fixture
def clip():
    return VideoClip()


def test_initialization(clip: VideoClip):
    assert isinstance(clip, VideoClip)
    assert clip.start == 0.0
    assert clip.end is None
    assert clip.duration is None
    assert clip.audio is None
    assert clip.fps is None
    assert clip.size is None
    assert clip.relative_pos is False
    assert callable(clip.pos)
    assert (0, 0) == clip.pos(0)


def test__iter__(clip: VideoClip):
    # raises ValueError if fps is not set
    with pytest.raises(ValueError):
        for _ in clip:
            pass

    clip.fps = 30
    clip.end = 1

    with pytest.raises(NotImplementedError):
        for _ in clip:
            pass
    clip.make_frame_array = lambda t: np.zeros((100, 100, 3), dtype=np.uint8)
    clip.fps = 1
    clip.end = 1
    for frame in clip:
        assert np.array_equal(frame, np.zeros((100, 100, 3), dtype=np.uint8))


def test_width_height(clip: VideoClip):
    with pytest.raises(ValueError):
        clip.width
    with pytest.raises(ValueError):
        clip.height
    clip.size = (100, 200)
    assert clip.width == 100
    assert clip.height == 200


def test_aspect_ratio(clip: VideoClip):
    with pytest.raises(ValueError):
        clip.aspect_ratio
    clip.size = (100, 200)
    assert clip.aspect_ratio == Fraction(100, 200)


def test_start_setter_getter(clip: VideoClip):
    assert clip.start == 0.0
    clip.start = 1.0
    assert clip.start == 1.0
    clip._dur = 2.0
    clip.audio = AudioClip()
    clip.start = 0.0
    assert clip.audio.start == 0.0
    assert clip.start == clip._st
    clip.set_start(2.0)
    assert clip.start == 2.0


def test_end_setter_getter(clip: VideoClip):
    assert clip.end is None
    clip.end = 1.0
    assert clip.end == 1.0
    clip._dur = 2.0
    clip.audio = AudioClip()
    clip.end = 10.0
    assert clip.audio.end == 10.0
    clip.set_end(2.0)
    assert clip.end == 2.0


def test_duration_setter_getter(clip: VideoClip):
    assert clip._dur == clip.duration == None
    with pytest.raises(ValueError):
        clip.duration = 1.0

    clip._dur = 2.0
    assert clip.duration == 2.0


def test_pos(clip: VideoClip):
    assert (
        clip.pos(0) == (0, 0)
        and clip.pos(1) == (0, 0)
        and clip.pos(2.2) == (0, 0)
        and clip.pos(-1) == (0, 0)
    )
    clip.set_position((100, 200))
    assert (
        clip.pos(0) == (100, 200)
        and clip.pos(1) == (100, 200)
        and clip.pos(2.2) == (100, 200)
        and clip.pos(-1) == (100, 200)
    )
    clip.size = (100, 200)
    clip.set_position((0.1, 0.3), relative=True)
    assert clip.pos(0) == (int(100 * 0.1), int(200 * 0.3))
    assert (
        clip.pos(0) == (100 * 0.1, 200 * 0.3)
        and clip.pos(1) == (100 * 0.1, 200 * 0.3)
        and clip.pos(2.2) == (100 * 0.1, 200 * 0.3)
        and clip.pos(-1) == (100 * 0.1, 200 * 0.3)
    )
    # using lambda
    clip.set_position(lambda t: (int(t + t), int(t * t)))
    assert (
        clip.pos(0) == (0, 0)
        and clip.pos(1) == (int(1 + 1), int(1 * 1))
        and clip.pos(2.2) == (int(2.2 + 2.2), int(2.2 * 2.2))
        and clip.pos(-1) == (int(-1 + -1), 1)
    )
    clip.set_position(lambda t: ((t * 0.1), 0.5), relative=True)
    assert (
        clip.pos(0) == (int(100 * 0), int(200 * 0.5))
        and clip.pos(100) == (int(100 * 10), int(200 * 0.5))
        and clip.pos(200) == (int(100 * 20), int(200 * 0.5))
        and clip.pos(-1) == (int(100 * -0.1), int(200 * 0.5))
    )


def test_set_audio(clip: VideoClip):
    audio_clip = AudioClip(10.0, 44100)
    clip._st = 1.0
    clip._ed = 11.0
    clip.set_audio(audio_clip)
    assert clip.audio
    assert clip.audio.start == 1.0
    assert clip.audio.end == 11.0


def test_set_fps(clip: VideoClip):
    fps = 30.0
    clip.set_fps(fps)
    assert clip.fps == fps


def test_without_audio(clip: VideoClip):
    assert clip.without_audio() == clip
    clip.set_audio(AudioClip())
    assert clip.without_audio().audio is None


def test_copy(clip: VideoClip):
    clip_copy: VideoClip = clip.copy()
    assert clip_copy is not clip
    assert clip_copy == clip
    assert clip_copy.__dict__ == clip.__dict__
    clip_clip_copy = clip_copy.__copy__()
    assert clip_clip_copy is not clip_copy and clip_clip_copy is not clip
    assert clip_clip_copy == clip_copy and clip_clip_copy == clip
    assert (
        clip_clip_copy.__dict__ == clip_copy.__dict__
        and clip_clip_copy.__dict__ == clip.__dict__
    )


def test_make_frame_array(clip):
    with pytest.raises(NotImplementedError):
        clip.make_frame_array(0)


def test_make_frame_pil(clip):
    with pytest.raises(NotImplementedError):
        clip.make_frame_pil(0)


def test_get_frame(clip: VideoClip):
    img_arr = np.zeros((100, 100, 3), dtype=np.uint8)
    clip.make_frame_array = lambda t: img_arr
    clip.make_frame_pil = lambda t: Image.fromarray(img_arr)
    x = clip.get_frame(0, is_pil=None)
    assert isinstance(x, np.ndarray) and np.array_equal(x, img_arr.copy())
    y = clip.get_frame(0, is_pil=False)
    assert isinstance(y, np.ndarray) and np.array_equal(y, img_arr.copy())
    z = clip.get_frame(0, is_pil=True)
    assert isinstance(z, Image.Image) and np.array_equal(np.array(z), img_arr.copy())


def test_iterate_frames_pil_t(clip: VideoClip):
    # Test when end is set
    clip.end = 1
    clip.make_frame_pil = lambda t: Image.new("RGB", (100, 100))
    frames = tuple(clip.iterate_frames_pil_t(30))
    assert len(frames) == 30
    assert all(isinstance(frame, Image.Image) for frame in frames)

    # Test when duration is set
    clip.end = None
    clip.duration = 1
    frames = tuple(clip.iterate_frames_pil_t(30))
    assert len(frames) == 30
    assert all(isinstance(frame, Image.Image) for frame in frames)

    # Test when neither end nor duration is set
    clip.end = None
    clip._dur = None
    with pytest.raises(ValueError):
        tuple(clip.iterate_frames_pil_t(30))


def test_iterate_frames_array_t(clip: VideoClip):
    # Test when end is set
    clip.end = 1
    clip.make_frame_array = lambda t: np.zeros((100, 100, 3), dtype=np.uint8)
    frames = tuple(clip.iterate_frames_array_t(30))
    assert len(frames) == 30
    assert all(isinstance(frame, np.ndarray) for frame in frames)
    assert all(frame.shape == (100, 100, 3) for frame in frames)

    # Test when duration is set
    clip.end = None
    clip.duration = 1
    frames = tuple(clip.iterate_frames_array_t(30))
    assert len(frames) == 30
    assert all(isinstance(frame, np.ndarray) for frame in frames)
    assert all(frame.shape == (100, 100, 3) for frame in frames)

    # Test when neither end nor duration is set
    clip.end = None
    clip._dur = None
    with pytest.raises(ValueError):
        tuple(clip.iterate_frames_array_t(30))


def test_time_transform(clip: VideoClip):
    clip.make_frame_array = lambda t: t * t
    clip.make_frame_pil = lambda t: t + t
    t_timp = lambda t: t + 1
    assert clip.make_frame_array(1) == 1
    assert clip.make_frame_pil(1) == 2
    clip.fl_time_transform(t_timp)
    assert clip.make_frame_array(1) == 4
    assert clip.make_frame_pil(1) == 4


def test_sync_audio_video_s_e_d(clip: VideoClip):
    # Set the start, end, and duration of the clip
    clip.start = 1
    clip.end = 2
    clip.duration = 1

    # Set the audio of the clip
    clip.audio = AudioClip()

    # Call the method to synchronize the audio and video
    clip._sync_audio_video_s_e_d()

    # Check if the start, end, and duration of the audio match the video
    assert clip.audio.start == clip.start
    assert clip.audio.end == clip.end
    assert clip.audio._original_dur == clip.duration
