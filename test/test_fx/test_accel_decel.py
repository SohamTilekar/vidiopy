import pytest
import numpy
from vidiopy import Data2ImageClip
from vidiopy.video.VideoClip import VideoClip
from vidiopy.video.fx.accel_decel import accel_decel


def test_accel_decel():
    # Making a Numpy array image of random integer
    image = numpy.random.randint(0, 256, (100, 100, 3), dtype=numpy.uint8)
    clip = Data2ImageClip(image, fps=5)

    # Test when new_duration is None and ratio is 1.5
    with pytest.raises(ValueError):
        accel_decel(clip.copy(), ratio=1.5)

    clip = Data2ImageClip(image, fps=5, duration=10)
    clip.end = None
    clip = accel_decel(clip.copy(), ratio=2)
    assert clip.duration == 20
    assert clip.end == None
    assert clip.start == 0
    assert clip.fps == 5

    # Test when new_duration is a callable
    clip = accel_decel(clip.copy(), new_duration=lambda x: x * 2)
    assert clip.duration == 20
    assert clip.end == None
    assert clip.start == 0
    assert clip.fps == 5

    # Test when new_duration is an int or float
    clip = accel_decel(clip.copy(), new_duration=20)
    assert clip.duration == 20
    assert clip.end == None
    assert clip.start == 0
    assert clip.fps == 5

    # Test when clip duration is not set
    clip = Data2ImageClip(image, fps=5)
    with pytest.raises(ValueError):
        accel_decel(clip.copy(), new_duration=20)
