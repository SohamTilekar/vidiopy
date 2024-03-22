import pytest
from PIL import Image
from pathlib import Path
from vidiopy import ImageSequenceClip, SilenceClip
import numpy as np


@pytest.fixture
def image_sequence_clip():
    # Create a sequence of 5 images
    sequence = tuple(Image.new("RGB", (100, 100)) for _ in range(5))
    return ImageSequenceClip(sequence, fps=5)


@pytest.fixture
def image_files(tmp_path) -> list[str]:
    paths: list[str] = []
    for i in range(5):
        img = Image.new("RGB", (60, 30), color=(73, 109, 137))
        path = tmp_path / f"image{i}.png"
        img.save(path)
        paths.append(str(path))
    return paths


def test_init(image_files: list[str]):
    # testing audio
    audio = SilenceClip(duration=1)
    clip = ImageSequenceClip(tuple(image_files), fps=5, audio=audio)
    assert clip.audio == audio
    assert clip.duration == len(image_files) / 5
    assert clip.fps == 5

    # testing with a tuple[str] of file paths
    clip = ImageSequenceClip(tuple(image_files), fps=5)
    assert isinstance(clip, ImageSequenceClip)
    assert clip.fps == 5
    assert clip.duration == len(image_files) / 5

    # testing with a list[Path] of file paths
    paths = [Path(path) for path in image_files]
    clip = ImageSequenceClip(tuple(paths), fps=5)
    assert isinstance(clip, ImageSequenceClip)
    assert clip.fps == 5
    assert clip.duration == len(image_files) / 5

    # testing with a tuple[Image.Image]
    images = [Image.open(path) for path in image_files]
    clip = ImageSequenceClip(tuple(images), fps=5)
    assert isinstance(clip, ImageSequenceClip)
    assert clip.fps == 5
    assert clip.duration == len(image_files) / 5

    # testing with a tuple[np.ndarray]
    arrays = [np.array(img) for img in images]
    clip = ImageSequenceClip(tuple(arrays), fps=5)
    assert isinstance(clip, ImageSequenceClip)
    assert clip.fps == 5
    assert clip.duration == len(image_files) / 5


def test_eq(image_sequence_clip: ImageSequenceClip):
    # Create another ImageSequenceClip with the same properties
    sequence = tuple(Image.new("RGB", (100, 100)) for _ in range(5))
    other_clip = ImageSequenceClip(sequence, fps=5)
    assert image_sequence_clip == other_clip

    # Change a property and assert they are not equal
    other_clip.fps = 10
    assert image_sequence_clip != other_clip


def test_make_frame_array(image_sequence_clip: ImageSequenceClip):
    # Test with a time within the duration of the clip
    frame_array = image_sequence_clip.make_frame_array(0.5)
    assert isinstance(frame_array, np.ndarray)
    assert frame_array.shape == (100, 100, 3)


def test_make_frame_pil(image_sequence_clip: ImageSequenceClip):
    # Test with a time within the duration of the clip
    frame_pil = image_sequence_clip.make_frame_pil(0.5)
    assert isinstance(frame_pil, Image.Image)


def test_fl_frame_transform(image_sequence_clip: ImageSequenceClip):
    # Define a transformation function
    def transform_func(frame: np.ndarray):
        # Convert to grayscale
        return np.array(Image.fromarray(frame).convert("L"))

    # Apply the transformation to the clip
    transformed_clip = image_sequence_clip.fl_frame_transform(transform_func)
    assert isinstance(transformed_clip, ImageSequenceClip)
    assert all(Image.fromarray(frame).mode == "L" for frame in transformed_clip.clip)


if __name__ == "__main__":
    pytest.main([__file__])
