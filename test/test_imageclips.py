import pytest
from PIL import Image, ImageEnhance, ImageFont
import os
import numpy as np
from vidiopy import ImageClip, ImageSequenceClip, Data2ImageClip, ColorClip, TextClip


@pytest.fixture
def imageclip():
    return ImageClip(Image.new("RGB", (100, 100)), 5, 1)


def test_imageclip_init():
    clip = ImageClip(Image.new("RGB", (100, 100)), 5, 1)
    assert clip.image == Image.new("RGB", (100, 100))
    assert clip.size == (100, 100)
    assert clip.fps == 5
    assert clip.duration == 1 == clip.end
    assert clip.imagepath is None

    clip2 = ImageClip(np.zeros((100, 100, 3), dtype=np.uint8), 5, 1)
    assert clip2.size == (100, 100)
    assert clip2.fps == 5
    assert clip2.duration == 1 == clip2.end
    assert clip2.imagepath is None
    assert clip2.image == Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))

    media_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "media/auto_test_media",
            "black(100, 100).jpg",
        )
    )

    clip3 = ImageClip(media_path, 5, 1)
    assert clip3.size == (1000, 1000)
    assert clip3.fps == 5
    assert clip3.duration == 1 == clip3.end
    assert clip3.imagepath == media_path
    assert clip3.image == Image.open(media_path)

    clip4 = ImageClip(Image.new("RGB", (100, 100)))
    assert clip4.size == (100, 100)
    assert clip4.fps == None
    assert clip4.duration == None == clip4.end
    assert clip4.imagepath is None
    assert clip4.image == Image.new("RGB", (100, 100))

    clip5 = ImageClip(Image.new("RGB", (100, 100)), 5)
    assert clip5.size == (100, 100)
    assert clip5.fps == 5
    assert clip5.duration == None == clip5.end
    assert clip5.imagepath is None
    assert clip5.image == Image.new("RGB", (100, 100))

    clip6 = ImageClip(Image.new("RGB", (100, 100)), None, 1)
    assert clip6.size == (100, 100)
    assert clip6.fps == None
    assert clip6.duration == 1 == clip6.end
    assert clip6.imagepath is None
    assert clip6.image == Image.new("RGB", (100, 100))


def test_fl_frame_transform(imageclip: ImageClip):
    # Define a simple transformation function

    old_image = imageclip.copy()

    def sharpier(image: Image.Image, strength):
        enhancer = ImageEnhance.Sharpness(image)
        sharpened_image = enhancer.enhance(strength)
        return ImageClip(sharpened_image)

    # Apply the transformation
    imageclip.fl_frame_transform(sharpier, strength=2)

    assert imageclip.image != old_image
    assert imageclip.image != old_image.image
    assert imageclip.image.size == old_image.image.size


def test_fl_clip_transform(imageclip: ImageClip):
    with pytest.raises(ValueError):
        imageclip.fl_clip_transform(lambda x: x)


def test_sub_fx(imageclip: ImageClip):
    with pytest.raises(ValueError):
        imageclip.sub_fx(lambda x: x)


def test_sub_clip(imageclip: ImageClip):
    n_clip = imageclip.sub_clip()
    assert n_clip is imageclip

    imageclip.sub_clip(0.2, 0.8)
    assert imageclip.start == 0.2
    assert imageclip.end == 0.8
    assert imageclip.duration == 0.8

    imageclip.duration = None
    imageclip.end = None
    imageclip.sub_clip(0.2, 0.8)
    assert imageclip.start == 0.2
    assert imageclip.end == 0.8


def test_make_frame_array(imageclip: ImageClip):
    assert np.array_equal(imageclip.make_frame_array(0.0), np.array(imageclip.image))
    imageclip.image = None
    with pytest.raises(ValueError):
        imageclip.make_frame_array(0.0)


def test_make_frame_pil(imageclip: ImageClip):
    assert imageclip.make_frame_pil(0.0) == imageclip.image
    imageclip.image = None
    with pytest.raises(ValueError):
        imageclip.make_frame_pil(0.0)


def test_to_video_clip(imageclip: ImageClip):
    # Call to_video_clip method
    video_clip: ImageSequenceClip = imageclip.to_video_clip(
        fps=24, duration=10.0, start=2.0, end=12.0
    )

    # Assert that the returned object is an instance of ImageSequenceClip
    assert isinstance(video_clip, ImageSequenceClip)

    # Assert that the fps, duration, start, and end attributes are correctly set
    assert video_clip.fps == 24
    assert video_clip.duration == 10.0
    assert video_clip.start == 2.0
    assert video_clip.end == 12.0

    # Assert that the number of frames is correct
    assert len(video_clip.clip) == 24 * 10.0

    # Assert that the audio attribute is None (since we didn't set it in the ImageClip)
    assert video_clip.audio is None


def test_data2imageclip():
    # Test with numpy array data
    data_array = np.random.randint(0, 255, size=(480, 640, 3), dtype=np.uint8)
    clip1 = Data2ImageClip(data=data_array, fps=30, duration=5)
    assert isinstance(clip1.image, Image.Image)
    assert clip1.size == (640, 480)
    assert clip1.fps == 30
    assert clip1.duration == 5

    # Test with PIL Image data
    data_image = Image.new("RGB", (640, 480), color="red")
    clip2 = Data2ImageClip(data=data_image, fps=24, duration=10)
    assert isinstance(clip2.image, Image.Image)
    assert clip2.size == (640, 480)
    assert clip2.fps == 24
    assert clip2.duration == 10

    # Test with unsupported data type
    with pytest.raises(TypeError):
        Data2ImageClip(data="unsupported data type", fps=24, duration=10)


def test_colorclip_init():
    color = "red"
    mode = "RGB"
    size = (500, 500)
    fps = 30
    duration = 5

    clip = ColorClip(color=color, mode=mode, size=size, fps=fps, duration=duration)

    assert clip.color == color
    assert clip.mode == mode
    assert clip.size == size
    assert clip.fps == fps
    assert clip.duration == duration
    assert isinstance(clip.image, Image.Image)


def test_colorclip_set_size():
    clip = ColorClip(color="red", size=(500, 500), fps=30, duration=5)
    new_size = (800, 600)
    clip.set_size(new_size)
    assert clip.size == new_size
    assert clip.image.size == new_size


def test_textclip_initialization():
    text = "Test Text"
    font_size = 30
    txt_color = "red"
    bg_color = "blue"
    fps = 24
    duration = 5.0

    text_clip = TextClip(
        text,
        font_size=font_size,
        txt_color=txt_color,
        bg_color=bg_color,
        fps=fps,
        duration=duration,
    )

    assert text_clip.text == text
    assert text_clip.font_size == font_size
    assert text_clip.txt_color == txt_color
    assert text_clip.bg_color == bg_color
    assert text_clip.fps == fps
    assert text_clip.duration == duration

    # Check that the font is an instance of ImageFont.FreeTypeFont or ImageFont.ImageFont
    assert isinstance(text_clip.font, (ImageFont.FreeTypeFont, ImageFont.ImageFont))

    # Check that the image is not None
    assert text_clip.image is not None
