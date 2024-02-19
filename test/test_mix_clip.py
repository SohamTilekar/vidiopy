from email.mime import audio
import sys
import pytest
from vidiopy.video.mixing_clip import composite_videoclips, concatenate_videoclips
from vidiopy import ImageClip, ImageSequenceClip, SilenceClip, AudioArrayClip
from PIL import Image


def test_composite_videoclips():
    # Create some mock VideoClip objects
    clip1 = ImageClip(Image.new("RGB", (60, 30), "red"), duration=10, fps=30)
    audio1 = SilenceClip(duration=10)
    clip1.set_audio(audio1)
    clip2 = ImageClip(Image.new("RGB", (15, 15), "blue"), duration=20, fps=30)
    audio2 = SilenceClip(duration=20)
    clip2.set_audio(audio2)
    clips = [clip1, clip2]

    # Test when use_bg_clip is True and fps is provided
    result = composite_videoclips(clips, fps=30, use_bg_clip=True)
    assert isinstance(result, ImageSequenceClip)
    assert result.fps == 30
    assert result.duration == 10

    # Test when use_bg_clip is False and fps is provided
    result = composite_videoclips(clips, fps=30, use_bg_clip=False)
    assert isinstance(result, ImageSequenceClip)
    assert result.fps == 30
    assert result.duration == 20

    # Test when audio is False
    result = composite_videoclips(clips, fps=30, use_bg_clip=False, audio=False)
    assert result.audio is None

    # Test when audio is True but clips have no audio
    clip1.audio = None
    clip2.audio = None
    clips = [clip1, clip2]
    result = composite_videoclips(clips, fps=30, use_bg_clip=False, audio=True)
    assert isinstance(result.audio, AudioArrayClip)

    # Test when audio is True and clips have audio
    clip1.audio = SilenceClip(duration=10)
    clip2.audio = SilenceClip(duration=20)
    clips = [clip1, clip2]
    result = composite_videoclips(clips, fps=30, use_bg_clip=False, audio=True)
    assert isinstance(result.audio, AudioArrayClip)
    assert result.audio.duration == 20

    # Test when clips have no duration
    clip1._dur = None
    clip1.end = None
    clip2._dur = None
    clip2.end = None
    clips = [clip1, clip2]
    with pytest.raises(ValueError):
        composite_videoclips(clips, fps=30, use_bg_clip=False)

    # Test when clips have no size
    clip1.size = None
    clip2.size = None
    clips = [clip1, clip2]
    with pytest.raises(ValueError):
        composite_videoclips(clips, fps=30, use_bg_clip=False)


def test_concatenate_videoclips():
    # Create some mock VideoClip objects
    clip1 = ImageClip(Image.new("RGB", (60, 30), "red"), duration=10, fps=30)
    audio1 = SilenceClip(duration=10)
    clip1.set_audio(audio1)
    clip2 = ImageClip(Image.new("RGB", (15, 15), "blue"), duration=20, fps=30)
    audio2 = SilenceClip(duration=20)
    clip2.set_audio(audio2)
    clips = [clip1, clip2]

    # Test when scaling_strategy is None
    result = concatenate_videoclips(clips, fps=30, scaling_strategy="scale_same")
    assert isinstance(result, ImageSequenceClip)
    assert result.fps == 30
    assert result.duration == 30

    # Test when scaling_strategy is True
    result = concatenate_videoclips(clips, fps=30, scaling_strategy="scale_up")
    assert isinstance(result, ImageSequenceClip)
    assert result.fps == 30
    assert result.duration == 30

    # Test when scaling_strategy is False
    result = concatenate_videoclips(clips, fps=30, scaling_strategy="scale_down")
    assert isinstance(result, ImageSequenceClip)
    assert result.fps == 30
    assert result.duration == 30

    # Test when scaling_strategy is not bool or None
    with pytest.raises(TypeError):
        concatenate_videoclips(clips, fps=30, scaling_strategy="invalid")

    # Test when audio is False
    result = concatenate_videoclips(clips, fps=30, audio=False)
    assert result.audio is None

    # Test when audio is True but clips have no audio
    clip1.audio = None
    clip2.audio = None
    clips = [clip1, clip2]
    result = concatenate_videoclips(clips, fps=30, audio=True)
    assert result.audio is not None

    # Test when audio is True and clips have audio
    clip1.audio = SilenceClip(duration=10)
    clip2.audio = SilenceClip(duration=20)
    clips = [clip1, clip2]
    result = concatenate_videoclips(clips, fps=30, audio=True)
    assert result.audio is not None

    # Test when clips have no duration
    clip1._dur = None
    clip1.end = None
    clip2._dur = None
    clip2.end = None
    clips = [clip1, clip2]
    with pytest.raises(ValueError):
        concatenate_videoclips(clips, fps=30)

    # Test when clips have no size
    clip1.size = None
    clip2.size = None
    clips = [clip1, clip2]
    with pytest.raises(ValueError):
        concatenate_videoclips(clips, fps=30)
