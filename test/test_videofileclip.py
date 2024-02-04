import os
from pathlib import Path

import pytest
from PIL import Image, ImageFilter, ImageEnhance
from vidiopy import VideoFileClip, SilenceClip


@pytest.fixture
def clip_random_audio():
    pth = Path(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "media/auto_test_media/test_video_random_5f_np.zeros(100, 100, 3).mkv",
            )
        )
    )
    return VideoFileClip(pth)


@pytest.fixture
def clip_random_no_audio():
    pth = Path(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "media/auto_test_media/test_video_random_5f_np.zeros(100, 100, 3).mkv",
            )
        )
    )
    return VideoFileClip(
        pth,
        audio=False,
    )


def test_init_clip_audio(clip_random_audio: VideoFileClip):
    assert clip_random_audio.audio is not None
    assert clip_random_audio.audio.duration == clip_random_audio.duration
    assert clip_random_audio.audio.start == clip_random_audio.start
    assert clip_random_audio.audio.end == clip_random_audio.end

    assert clip_random_audio.size == (100, 100)
    assert clip_random_audio.fps == 5
    assert clip_random_audio.clip is not None
    assert isinstance(clip_random_audio.clip, tuple)
    assert isinstance(clip_random_audio.clip[0], Image.Image)
    assert len(clip_random_audio.clip) == 5


def test_init_clip_no_audio(clip_random_no_audio: VideoFileClip):
    assert clip_random_no_audio.audio is None

    assert clip_random_no_audio.size == (100, 100)
    assert clip_random_no_audio.fps == 5
    assert clip_random_no_audio.clip is not None
    assert isinstance(clip_random_no_audio.clip, tuple)
    assert isinstance(clip_random_no_audio.clip[0], Image.Image)
    assert len(clip_random_no_audio.clip) == 5


def test_clip_fl_frame_transform(clip_random_no_audio: VideoFileClip):
    def frame_t(frame: Image.Image, *args, **kwargs):
        return frame.filter(ImageFilter.SHARPEN)

    old_clip: tuple[Image.Image, ...] = clip_random_no_audio.clip
    clip_random_no_audio.fl_frame_transform(frame_t)
    assert clip_random_no_audio.clip != old_clip
    assert isinstance(clip_random_no_audio.clip, tuple)
    assert isinstance(clip_random_no_audio.clip[0], Image.Image)
    assert len(clip_random_no_audio.clip) == 5
    assert clip_random_no_audio.clip[0] == frame_t(old_clip[0])


def test_clip_fl_clip_transform(clip_random_no_audio: VideoFileClip):
    def clip_t(frame: Image.Image, frame_time: float, *args, **kwargs):
        # Create a Sharpness object from the image
        enhancer = ImageEnhance.Sharpness(frame)

        # Increase the sharpness
        # The factor 2.0 gives a sharpened image, factor 1.0 gives the original image, and factor 0.0 gives a blurred image
        sharper_image = enhancer.enhance(frame_time)

        return sharper_image

    old_clip: tuple[Image.Image, ...] = clip_random_no_audio.clip
    clip_random_no_audio.fl_clip_transform(clip_t)
    assert clip_random_no_audio.clip != old_clip
    assert isinstance(clip_random_no_audio.clip, tuple)
    assert isinstance(clip_random_no_audio.clip[0], Image.Image)
    assert len(clip_random_no_audio.clip) == 5
    assert clip_random_no_audio.clip[0] == clip_t(old_clip[0], 0.0)


def test_clip_sub_clip(clip_random_no_audio: VideoFileClip):
    old_clip = clip_random_no_audio.clip
    clip_random_no_audio.sub_clip(t_end=0.5)
    assert clip_random_no_audio.duration == 0.5
    assert clip_random_no_audio.start == 0.0
    assert clip_random_no_audio.end == 0.5
    assert clip_random_no_audio.clip != old_clip
    assert len(clip_random_no_audio.clip) < len(old_clip)
    assert isinstance(clip_random_no_audio.clip, tuple)
    assert isinstance(clip_random_no_audio.clip[0], Image.Image)


def test_clip_sub_clip_copy(clip_random_no_audio: VideoFileClip):
    old_clip = clip_random_no_audio.clip
    new_clip_copy = clip_random_no_audio.sub_clip_copy(t_end=0.5)
    assert new_clip_copy.duration == 0.5
    assert new_clip_copy.start == 0.0
    assert new_clip_copy.end == 0.5
    assert new_clip_copy.clip != old_clip
    assert len(new_clip_copy.clip) != len(old_clip)
    assert isinstance(new_clip_copy.clip, tuple)
    assert isinstance(new_clip_copy.clip[0], Image.Image)
    assert clip_random_no_audio is new_clip_copy


def test_make_frame_pil(clip_random_no_audio: VideoFileClip):
    assert clip_random_no_audio.make_frame_pil(0.0) == clip_random_no_audio.clip[0]
    assert clip_random_no_audio.make_frame_pil(1) == clip_random_no_audio.clip[-1]
    assert (
        clip_random_no_audio.make_frame_pil(0.5) == clip_random_no_audio.clip[2]
        or clip_random_no_audio.make_frame_pil(0.5) == clip_random_no_audio.clip[3]
    )
    assert clip_random_no_audio.make_frame_pil(0.5) != clip_random_no_audio.clip[0]

    with pytest.raises(ValueError):
        clip_random_no_audio._dur = None
        clip_random_no_audio.make_frame_pil(1)


def test_make_frame_array(clip_random_audio: VideoFileClip):
    assert (
        clip_random_audio.make_frame_array(0.0).shape[:-1]
        == clip_random_audio.clip[0].size
    )
    assert (
        clip_random_audio.make_frame_array(1).shape[:-1]
        == clip_random_audio.clip[-1].size
    )
    assert (
        clip_random_audio.make_frame_array(0.5).shape[:-1]
        == clip_random_audio.clip[2].size
    )
    assert (
        clip_random_audio.make_frame_array(0.5).shape != clip_random_audio.clip[0].size
    )

    with pytest.raises(ValueError):
        clip_random_audio._dur = None
        clip_random_audio.make_frame_array(1)
