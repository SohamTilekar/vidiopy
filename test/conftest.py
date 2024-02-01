from vidiopy import VideoClip, VideoFileClip
import pytest


@pytest.fixture
def clip():
    return VideoClip()
