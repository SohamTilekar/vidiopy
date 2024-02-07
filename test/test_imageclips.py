import sys
import tempfile
import pytest
from PIL import Image
import numpy as np
from pathlib import Path
from vidiopy import ImageClip, ImageSequenceClip


@pytest.fixture
def image_clip():
    img = Image.new("RGB", (60, 30), color="red")
    return ImageClip(img, fps=30, duration=5)


def test_init():
    # Test initialization with PIL Image
    image_clip = ImageClip(Image.new("RGB", (60, 30)), fps=30, duration=5)
    assert image_clip.fps == 30
    assert image_clip.duration == 5
    assert image_clip.start == 0.0
    assert image_clip.end == 5
    assert image_clip.size == (60, 30)

    # Test initialization with numpy array
    image_clip = ImageClip(np.array(Image.new("RGB", (60, 30))), fps=30, duration=5)
    assert image_clip.fps == 30
    assert image_clip.duration == 5
    assert image_clip.start == 0.0
    assert image_clip.end == 5
    assert image_clip.size == (60, 30)

    # Test initialization with file path
    pth = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    Image.new("RGB", (60, 30)).save(pth)
    image_clip = ImageClip(pth, fps=30, duration=5)
    assert image_clip.fps == 30
    assert image_clip.duration == 5
    assert image_clip.start == 0.0
    assert image_clip.end == 5
    assert image_clip.size == (60, 30)

    # Test initialization with pathlib.Path object
    image_clip = ImageClip(Path(pth), fps=30, duration=5)
    assert image_clip.fps == 30
    assert image_clip.duration == 5
    assert image_clip.start == 0.0
    assert image_clip.end == 5
    assert image_clip.size == (60, 30)


def test_eq(image_clip: ImageClip):
    img = Image.new("RGB", (60, 30), color="red")
    other_clip = ImageClip(img, fps=30, duration=5)
    assert image_clip == other_clip


def test_duration(image_clip: ImageClip):
    image_clip.duration = 10
    assert image_clip.duration == 10


def test_set_duration(image_clip: ImageClip):
    image_clip.set_duration(10)
    assert image_clip.duration == 10


def test_fl_frame_transform(image_clip: ImageClip):
    def transform(img):
        return img.rotate(90)

    image_clip.fl_frame_transform(transform)
    assert image_clip.image == transform(image_clip.image)


def test_fl_clip_transform(image_clip: ImageClip):
    with pytest.raises(ValueError):
        image_clip.fl_clip_transform(None)


def test_fx(image_clip: ImageClip):
    def func():
        pass

    assert image_clip.fx(func) == image_clip


def test_sub_clip(image_clip: ImageClip):
    new_ = image_clip.sub_clip(1, 4)
    assert new_ is image_clip
    assert image_clip.start == 1
    assert image_clip.end == 4


def test_sub_clip_copy(image_clip: ImageClip):
    new_ = image_clip.sub_clip_copy(1, 4)
    assert new_ is not image_clip
    assert new_.start == 1
    assert new_.end == 4


def test_make_frame_array(image_clip: ImageClip):
    assert np.array_equal(image_clip.make_frame_array(0), np.array(image_clip.image))


def test_make_frame_pil(image_clip: ImageClip):
    assert image_clip.make_frame_pil(0) == image_clip.image


def test_to_video_clip():
    # Create an ImageClip instance
    image_clip = ImageClip(Image.new("RGB", (60, 30)), fps=30, duration=5)

    # Test with specified fps and duration
    video_clip = image_clip.to_video_clip(fps=30, duration=5)
    assert video_clip.fps == 30
    assert video_clip.duration == 5
    assert video_clip.start == 0.0
    assert video_clip.end == 5.0
    assert isinstance(video_clip, ImageSequenceClip)

    # Test without specified fps and duration
    image_clip.fps = 24
    image_clip.duration = 10
    video_clip = image_clip.to_video_clip()
    assert video_clip.fps == 24
    assert video_clip.duration == 10
    assert video_clip.start == 0.0
    assert video_clip.end == 5.0
    assert isinstance(video_clip, ImageSequenceClip)

    # Test with fps and duration not set in ImageClip instance
    image_clip = ImageClip()
    with pytest.raises(ValueError):
        video_clip = image_clip.to_video_clip()

    # Test with fps not set in ImageClip instance
    image_clip.duration = 10
    with pytest.raises(ValueError):
        video_clip = image_clip.to_video_clip()

    # Test with duration not set in ImageClip instance
    image_clip = ImageClip()
    image_clip.fps = 24
    with pytest.raises(ValueError):
        video_clip = image_clip.to_video_clip()


if __name__ == "__main__":
    pytest.main([__file__, *sys.argv])
