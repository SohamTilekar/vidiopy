import pytest
import numpy as np
from PIL import Image
from vidiopy import ColorClip
from vidiopy.video.fx import (
    fadein, fadeout, speedx, time_mirror, loop, 
    resize, rotate, margin, invert_colors, blackwhite, mask_color
)

@pytest.fixture
def base_clip():
    # A 5-second red clip at 30 fps
    return ColorClip(color="red", size=(100, 100), fps=30, duration=5)

def test_mask_color():
    clip = ColorClip(color=(0, 255, 0), size=(100, 100), fps=30, duration=5)
    masked = mask_color(clip, color=(0, 255, 0), threshold=10)
    frame = masked.make_frame_array(0)
    # Alpha channel should be 0 because the color matches exactly
    assert frame[0, 0, 3] == 0

def test_fadein(base_clip):
    faded = fadein(base_clip, duration=2)
    assert faded.duration == base_clip.duration
    frame0 = faded.make_frame_array(0)
    frame1 = faded.make_frame_array(1)
    frame2 = faded.make_frame_array(2)
    # At t=0 it should be black (0) or heavily faded
    assert np.all(frame0 == 0)
    # At t=1 it should be 50% red
    assert np.all(frame1[:, :, 0] < 255)
    # At t=2 it should be fully red
    assert np.all(frame2[:, :, 0] == 255)

def test_fadeout(base_clip):
    faded = fadeout(base_clip, duration=2)
    frame_end = faded.make_frame_array(5)
    frame_mid = faded.make_frame_array(4)
    assert np.all(frame_end == 0)
    assert np.all(frame_mid[:, :, 0] < 255)

def test_speedx(base_clip):
    sped = speedx(base_clip, factor=2)
    assert sped.duration == 2.5
    assert sped.end == 2.5

def test_time_mirror(base_clip):
    mirrored = time_mirror(base_clip)
    assert mirrored.duration == 5
    # Just checking it runs without error
    frame = mirrored.make_frame_array(1)
    assert frame.shape == (100, 100, 4)

def test_loop(base_clip):
    looped = loop(base_clip, n=3)
    assert looped.duration == 15
    looped_dur = loop(base_clip, duration=10)
    assert looped_dur.duration == 10

def test_resize(base_clip):
    resized = resize(base_clip, new_size=(50, 50))
    assert resized.size == (50, 50)
    frame = resized.make_frame_array(0)
    assert frame.shape == (50, 50, 4)

def test_rotate(base_clip):
    rotated = rotate(base_clip, angle=90, expand=True)
    frame = rotated.make_frame_array(0)
    assert frame.shape == (100, 100, 4)

def test_margin(base_clip):
    margined = margin(base_clip, top=10, bottom=10, left=10, right=10)
    assert margined.size == (120, 120)
    frame = margined.make_frame_array(0)
    assert frame.shape == (120, 120, 4)

def test_invert_colors(base_clip):
    inverted = invert_colors(base_clip)
    frame = inverted.make_frame_array(0)
    # Red is (255, 0, 0), inverted is (0, 255, 255)
    assert frame[0, 0, 0] == 0
    assert frame[0, 0, 1] == 255
    assert frame[0, 0, 2] == 255

def test_blackwhite(base_clip):
    bw = blackwhite(base_clip)
    frame = bw.make_frame_array(0)
    # Grayscale RGB means R=G=B
    assert frame[0, 0, 0] == frame[0, 0, 1] == frame[0, 0, 2]
