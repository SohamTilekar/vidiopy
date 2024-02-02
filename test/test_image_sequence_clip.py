from vidiopy import ImageSequenceClip, SilenceClip
from pathlib import Path
import numpy as np
import os
import pytest
from PIL import Image


@pytest.fixture
def imagesequenceclip() -> tuple[ImageSequenceClip, tuple[Image.Image, ...]]:
    c: list[Image.Image] = []
    for i in range(1, 23):
        c.append(Image.new("RGB", (100, 100), (i, i, i)))
    clip = ImageSequenceClip(tuple(c), duration=1, audio=SilenceClip(5))
    return clip, tuple(c)


def test_image_sequence_clip_init_path_to_folder():
    media_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "media/sequence")
    )

    clip = ImageSequenceClip(media_path, fps=4)
    assert len(clip.clip) == 22
    assert clip.fps == 4
    assert clip.duration == 22 / 4
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    clip = ImageSequenceClip(Path(media_path), fps=4)
    assert len(clip.clip) == 22
    assert clip.fps == 4
    assert clip.duration == 22 / 4
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    clip = ImageSequenceClip(media_path, duration=5)
    assert len(clip.clip) == 22
    assert clip.fps == 22 / 5
    assert clip.duration == 5
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    clip = ImageSequenceClip(Path(media_path), duration=5)
    assert len(clip.clip) == 22
    assert clip.fps == 22 / 5
    assert clip.duration == 5
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    with pytest.raises(ValueError):
        ImageSequenceClip(media_path)

    with pytest.raises(ValueError):
        ImageSequenceClip(Path(media_path))

    clip = ImageSequenceClip(media_path, fps=5, audio=SilenceClip(5))
    assert isinstance(clip.audio, SilenceClip)
    assert clip.audio.duration == 5
    assert clip.audio.fps == 44100

    clip = ImageSequenceClip(Path(media_path), fps=5, audio=SilenceClip(5))
    assert isinstance(clip.audio, SilenceClip)
    assert clip.audio.duration == 5
    assert clip.audio.fps == 44100


def test_image_sequence_clip_init_path_to_files():
    media_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "media/sequence")
    )

    files = [
        os.path.join(media_path, file)
        for file in os.listdir(media_path)
        if os.path.isfile(os.path.join(media_path, file))
        and os.path.splitext(file)[1].lower()
        in set(Image.registered_extensions().keys())
    ]
    files.sort()
    files = tuple(files)

    clip = ImageSequenceClip(files, fps=4)
    assert len(clip.clip) == 22
    assert clip.fps == 4
    assert clip.duration == 22 / 4
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    clip = ImageSequenceClip(files, duration=5)
    assert len(clip.clip) == 22
    assert clip.fps == 22 / 5
    assert clip.duration == 5
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    with pytest.raises(ValueError):
        ImageSequenceClip(files)

    clip = ImageSequenceClip(files, fps=5, audio=SilenceClip(5))
    assert isinstance(clip.audio, SilenceClip)
    assert clip.audio.duration == 5
    assert clip.audio.fps == 44100

    files = [
        Path(os.path.join(media_path, file))
        for file in os.listdir(media_path)
        if os.path.isfile(os.path.join(media_path, file))
        and os.path.splitext(file)[1].lower()
        in set(Image.registered_extensions().keys())
    ]
    files.sort()
    files = tuple(files)

    clip = ImageSequenceClip(files, fps=4)
    assert len(clip.clip) == 22
    assert clip.fps == 4
    assert clip.duration == 22 / 4
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    clip = ImageSequenceClip(files, duration=5)
    assert len(clip.clip) == 22
    assert clip.fps == 22 / 5
    assert clip.duration == 5
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    with pytest.raises(ValueError):
        ImageSequenceClip(files)

    clip = ImageSequenceClip(files, fps=5, audio=SilenceClip(5))
    assert isinstance(clip.audio, SilenceClip)
    assert clip.audio.duration == 5
    assert clip.audio.fps == 44100


def test_image_sequence_clip_init_tuples_images():
    media_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "media/sequence")
    )

    files = [
        os.path.join(media_path, file)
        for file in os.listdir(media_path)
        if os.path.isfile(os.path.join(media_path, file))
        and os.path.splitext(file)[1].lower()
        in set(Image.registered_extensions().keys())
    ]
    files.sort()
    files = tuple(files)

    images = tuple(map(Image.open, files))

    clip = ImageSequenceClip(images, fps=4)
    assert len(clip.clip) == 22
    assert clip.fps == 4
    assert clip.duration == 22 / 4
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    clip = ImageSequenceClip(images, duration=5)
    assert len(clip.clip) == 22
    assert clip.fps == 22 / 5
    assert clip.duration == 5
    assert clip.clip[0] == Image.open(os.path.join(media_path, "mouth0001.png"))
    assert clip.clip[1] == Image.open(os.path.join(media_path, "mouth0002.png"))
    assert clip.clip[-1] == Image.open(os.path.join(media_path, "mouth0022.png"))

    with pytest.raises(ValueError):
        ImageSequenceClip(images)

    clip = ImageSequenceClip(images, fps=5, audio=SilenceClip(5))
    assert isinstance(clip.audio, SilenceClip)
    assert clip.audio.duration == 5
    assert clip.audio.fps == 44100


def test_image_sequence_clip_init_numpy_array():
    media_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "media/sequence")
    )

    files = [
        os.path.join(media_path, file)
        for file in os.listdir(media_path)
        if os.path.isfile(os.path.join(media_path, file))
        and os.path.splitext(file)[1].lower()
        in set(Image.registered_extensions().keys())
    ]
    files.sort()
    files = tuple(files)

    images = tuple(map(Image.open, files))
    images = tuple(map(np.array, images))

    clip = ImageSequenceClip(images, fps=4)
    assert len(clip.clip) == 22
    assert clip.fps == 4
    assert clip.duration == 22 / 4
    assert np.array_equal(
        np.array(clip.clip[0]),
        np.array(Image.open(os.path.join(media_path, "mouth0001.png"))),
    )
    assert np.array_equal(
        np.array(clip.clip[1]),
        np.array(Image.open(os.path.join(media_path, "mouth0002.png"))),
    )
    assert np.array_equal(
        np.array(clip.clip[-1]),
        np.array(Image.open(os.path.join(media_path, "mouth0022.png"))),
    )

    clip = ImageSequenceClip(images, duration=5)
    assert len(clip.clip) == 22
    assert clip.fps == 22 / 5
    assert clip.duration == 5
    assert np.array_equal(
        np.array(clip.clip[0]),
        np.array(Image.open(os.path.join(media_path, "mouth0001.png"))),
    )
    assert np.array_equal(
        np.array(clip.clip[1]),
        np.array(Image.open(os.path.join(media_path, "mouth0002.png"))),
    )
    assert np.array_equal(
        np.array(clip.clip[-1]),
        np.array(Image.open(os.path.join(media_path, "mouth0022.png"))),
    )

    with pytest.raises(ValueError):
        ImageSequenceClip(images)

    clip = ImageSequenceClip(images, fps=5, audio=SilenceClip(5))
    assert isinstance(clip.audio, SilenceClip)
    assert clip.audio.duration == 5
    assert clip.audio.fps == 44100


def test_make_frame_array(
    imagesequenceclip: tuple[ImageSequenceClip, tuple[ImageSequenceClip]]
):
    clip, seq = imagesequenceclip
    assert isinstance(clip.make_frame_array(0), np.ndarray)
    assert np.array_equal(clip.make_frame_array(0), np.array(seq[0]))
    assert np.array_equal(clip.make_frame_array(1), np.array(seq[-1]))


def test_make_frame_pil(
    imagesequenceclip: tuple[ImageSequenceClip, tuple[ImageSequenceClip]]
):
    clip, seq = imagesequenceclip
    assert isinstance(clip.make_frame_pil(0), Image.Image)
    assert clip.make_frame_pil(0) == seq[0]
    assert clip.make_frame_pil(1) == seq[-1]
