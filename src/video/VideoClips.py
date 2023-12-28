from fractions import Fraction
import os
from pathlib import Path
from typing import (Callable, override,
                    )
from copy import copy as _copy
from PIL import Image
import ffmpegio
# from ..Clip import Clip
# from ..audio.AudioClip import AudioClip
import numpy as np
from PIL import Image, ImageColor, ImageFont, ImageDraw

class Clip:...
class AudioClip:...

type Num = int | float
type NumOrNone = Num | None

class VideoClip(Clip):
    def __init__(self) -> None:
        super().__init__()
        self.start: Num = 0.0
        self.end: NumOrNone = None
        self.duration: NumOrNone = None
        self.audio: AudioClip | None = None
        self.fps: NumOrNone = None
        self.size: tuple[int, int] | None = None
        self.pos = lambda t: (0, 0)
        self.make_frame: Callable[..., np.ndarray] = lambda t: (_ for _ in ()).throw(Exception('Make Frame is Not Set.'))
        self.make_frame_pil = lambda t: (_ for _ in ()).throw(Exception('Make Frame pil is Not Set.'))
        self.make_frame_any = lambda t: (_ for _ in ()).throw(Exception('Make Frame any is Not Set.'))
        self.relative_pos = False

    @property
    def width(self):
        if self.size is not None:
            return self.size[0]
        else:
            raise ValueError("Size is not set")
    w = width
    @property
    def height(self):
        if self.size is not None:
            return self.size[1]
        else:
            raise ValueError("Size is not set")
    h = height
    @property
    def aspect_ratio(self):
        if isinstance(self.w, int) and isinstance(self.w, int):
            return Fraction(self.w, self.h)
        else:
            raise ValueError("Size is not set")
    
    def set_start(self, t, change_end=True):
        self.start = t
        if (self.duration is not None) and change_end:
            self.end = t + self.duration
        elif self.end is not None:
            self.duration = self.end - self.start\
    
    def set_end(self, t, change_start=True):
        self.end = t
        if self.end is None: return
        if self.start is None:
            if self.duration is not None:
                self.start = max(0, t - self.duration)
        else:
            self.duration = self.end - self.start
    
    def set_duration(self, t, change_end=True):
        self.duration = t

        if change_end:
            self.end = None if (t is None) else (self.start + t)
        else:
            if self.duration is None:
                raise Exception("Cannot change clip start when new"
                                "duration is None")
            self.start = self.end - t
    
    def set_position(self, pos, relative=False):
        self.relative_pos = relative
        if hasattr(pos, '__call__'):
            self.pos = pos
        else:
            self.pos = lambda t: pos

    def without_audio(self):
        self.audio = None

    def set_make_frame(self, func):
        self.make_frame = func

    def set_make_frame_pil(self, func):
        self.make_frame_pil = func

    def set_make_frame_any(self, func):
        self.make_frame_any = func

    def set_fps(self, fps):
        self.fps = fps
    


    def get_frame(self, t, is_pil=None):
        if is_pil is not None:
            return self.make_frame_any(t)
        elif is_pil == True:
            return self.make_frame_pil(t)
        else:
            return self.make_frame(t)

    def itrate_all_frames_array(self):
        x = 0
        while 1 > x:
            yield np.zeros((self.h, self.w, 3), dtype=np.uint8)
            x+=1
        raise ValueError("Iterate all clip Methood Is not Set")

    def itrate_all_frames_pil(self):
        x = 0
        while 1 > x:
            yield np.zeros((self.h, self.w, 3), dtype=np.uint8)
            x+=1
        raise ValueError("Iterate all clip Methood Is not Set")

    def iterate_frames_pil_t(self, fps: Num):
        time_dif = 1 / fps
        x = 0
        if self.duration is not None:
            while x <= self.duration:
                yield self.get_frame(x, is_pil=True)
                x += time_dif

    def iterate_frames_array_t(self, fps: Num):
        time_dif = 1 / fps
        x = 0
        if self.duration is not None:
            while x <= self.duration:
                yield self.get_frame(x, is_pil=False)
                x += time_dif

    def write_videofile(self, filename, fps=None, codec=None,   
                        bitrate=None, audio=False, audio_fps=44100,
                        preset="medium", pixel_format=None,
                        audio_codec=None, audio_bitrate=None,
                        write_logfile=False, verbose=True,
                        threads=None, ffmpeg_params: dict[str, str] | None = None,
                        logger='bar', over_write_output=True):
        
        video_np = np.asarray(tuple(self.iterate_frames_array_t(fps if fps else self.fps if self.fps else (_ for _ in ()
                                                                                                            ).throw(Exception('Make Frame is Not Set.')))))

        ffmpeg_options = {
            'preset': preset,
            **({'i': "audio -map 0:v -map 1:a -c:v copy -c:a copy"} if audio else {}),
            **(ffmpeg_params if ffmpeg_params is not None else {}),
            **({'c:v': codec} if codec else {}),
            **({'b:v': bitrate} if bitrate else {}),
            **({'pix_fmt': pixel_format} if pixel_format else {}),
            **({'c:a': audio_codec} if audio_codec else {}),
            **({'ar': audio_fps} if audio_fps else {}),
            **({'b:a': audio_bitrate} if audio_bitrate else {}),
            **({'threads': threads} if threads else {}),
        }

        ffmpegio.video.write(filename, 
                             fps if fps else self.fps if self.fps else (_ for _ in ()).throw(Exception('Make Frame is Not Set.')),
                             video_np,
                             overwrite=over_write_output,
                             show_log=True,
                             **ffmpeg_options)

    def write_imagesequence(self, nameformat, fps=None, dir='.', logger='bar'):
        frame_number = 0

        def save_frame(frame, frame_number):
            file_path = os.path.join(dir, str(frame_number)+nameformat)
            frame.save(file_path)

        if dir!='.' and not os.path.exists(dir):
            os.makedirs(dir)

        if fps:
            for frame in self.iterate_frames_pil_t(fps):
                save_frame(frame, frame_number)
                frame_number += 1
        else:
            if self.fps and self.duration:
                for frame in self.iterate_frames_pil_t(self.fps):
                    save_frame(frame, frame_number)
                    frame_number += 1
            else:
                print("Warning: FPS is not provided, and fps and duration are not set.")

                for frame in self.itrate_all_frames_pil():
                    save_frame(frame, frame_number)
                    frame_number += 1

    def to_ImageClip(self, t):
        return Data2ImageClip(self.get_frame(t))

class VideoFileClip(VideoClip):
    def __init__(self, filename, ffmpeg_options=None):
        super().__init__()
        video_data = ffmpegio.probe.video_streams_basic(filename)[0]
        self.clip = self._import_video_clip(filename, ffmpeg_options)
        self.fps: float = float(video_data['frame_rate'])
        self.size = (video_data['width'], video_data['height'])
        self.start = 0.0
        self.end = self.duration = video_data['duration']
        self.set_make_frame(self.make_frame_sub_cls)
        self.set_make_frame_pil(self.make_frame_pil_sub_cls)

    def _array2image(self):
        if isinstance(self.clip[0], np.ndarray):
            new_clip = []
            for frame in self.clip:
                new_clip.append(Image.fromarray(frame))
            self.clip = np.array(new_clip)
        elif isinstance(self.clip[0], Image.Image):
            ...
        elif self.clip is None:
            raise ValueError("Clip is not Set.")
        else:
            raise ValueError("Clip is not an image or numpy array")

    def _image2array(self):
        if isinstance(self.clip[0], Image.Image):
            new_clip = []
            for frame in self.clip:
                new_clip.append(np.asarray(frame))
            self.clip = np.array(new_clip)
        elif isinstance(self.clip[0], np.ndarray):
           ...
        elif self.clip is None:
            raise ValueError("Clip is not Set.")
        else:
            raise ValueError("Clip is not an image or numpy array")

    def make_frame_any_sub_cls(self, t):
        frame_num = t*self.fps
        return self.clip[int(frame_num)]

    def make_frame_sub_cls(self, t):
        frame_num = t*self.fps
        return np.array(self.clip[int(frame_num)])

    def make_frame_pil_sub_cls(self, t):
        frame_num = t*self.fps
        return Image.fromarray(self.clip[int(frame_num)])

    @override
    def iterate_frames_array_t(self, fps: Num):
        frame_t_dif = (1 / fps)
        st_0 = 0.0
        self._image2array()
        while st_0 < self.duration if self.duration is not None else (_ for _ in ()).throw(Exception('Duration is Not Set.')):
            yield self.make_frame(st_0)
            st_0 += frame_t_dif

    @override
    def iterate_frames_pil_t(self, fps: Num):
        frame_t_dif = (1 / fps)
        st_0 = 0.0
        self._array2image()
        while st_0 < self.duration if self.duration is not None else fps if fps else (_ for _ in ()).throw(Exception('Duration is Not Set.')):
            yield self.make_frame_pil(st_0)
            st_0 += frame_t_dif

    def _import_video_clip(self, file_name, ffmpeg_options):
        options = {
                            **(ffmpeg_options if ffmpeg_options else {})
        }
        return ffmpegio.video.read(file_name, show_log=True, **options)[1]

class ImageClip(VideoClip):
    
    def __init__(self, image: str | Path | None = None, fps: NumOrNone = None, duration: NumOrNone = None):
        super().__init__()
        self.image = self._import_image(image) if image else None
        self.set_make_frame_any(self.make_frame_any_image_clip)
        self.set_make_frame(self.make_frame_image_clip)
        self.set_make_frame_pil(self.make_frame_pil_image_clip)
        self.fps = fps
        self.duration = duration
        self.start = 0.0
        self.end = self.duration

    def _import_image(self, image):
        return Image.open(image)

    def _array2image(self):
        if isinstance(self.image, np.ndarray):
            return Image.fromarray(self.image)
        elif isinstance(self.image, Image.Image):
            return self.image
        elif self.image is None:
            raise ValueError("image is not Set.")
        else:
            raise ValueError("image is not an image or numpy array")

    def _image2array(self):
        if isinstance(self.image, Image.Image):
            return np.array(self.image)
        elif isinstance(self.image, np.ndarray):
            return self.image
        elif self.image is None:
            raise ValueError("image is not Set.")
        else:
            raise ValueError("image is not an image or numpy array")

    def make_frame_image_clip(self, t):
        self._image2array()
        return self.image

    def make_frame_any_image_clip(self, t):
        return self.image

    def make_frame_pil_image_clip(self, t):
        self._array2image()
        return self.image

class Data2ImageClip(ImageClip):
    def __init__(self, data: np.ndarray | Image.Image, fps: NumOrNone = None, duration: NumOrNone = None):
        super().__init__(fps=fps, duration=duration)
        self.image = self._import_image(data)

    @override
    def _import_image(self, image):
        if isinstance(image, np.ndarray):
            return Image.fromarray(image)
        elif isinstance(image, Image.Image):
            return image
        else:
            raise TypeError(f"{type(image)} is not an Image.Image or numpy array Type.")

class ImageSequenceClip(VideoClip):
    def __init__(self, images: str | Path | list[str | Path | Image.Image | np.ndarray] | np.ndarray, fps: NumOrNone = None):
        super().__init__()
        self.images = self._import_images(images)
        self.set_make_frame(self.make_frame_sub_cls)
        self.set_make_frame_pil(self.make_frame_pil_sub_cls)
        self.fps = fps
        self.duration = (len(self.images)*(fps if fps is not None else 0) if fps else None)
        self.start = 0.0
        self.end = self.duration

    def _import_images(self, images):
            if isinstance(images, (str, Path)):
                images_path = Path(images)
                if images_path.is_dir():
                    supported_extensions = {ext.lower() for ext in Image.registered_extensions()}
                    image_files = tuple(sorted([file for file in images_path.iterdir() if file.is_file() and file.suffix.lower() in supported_extensions]))
                    return tuple(Image.open(str(image)) for image in image_files)
                else:
                    raise ValueError(f"{images} is not a directory.")
            elif isinstance(images, (list, tuple, set)):
                return tuple(Image.open(str(image)) for image in images)
            elif isinstance(images, np.ndarray):
                return tuple(Image.fromarray(image) for image in images)
            else:
                raise ValueError("Invalid input. Provide a directory path, a list/tuple/set of paths, or a NumPy array.")

    def set_fps(self, fps: Num):
        self.fps = fps
        self.duration = len(self.images)*fps

    def _array2image(self):
        if isinstance(self.images[0], np.ndarray):
            self.images = tuple(Image.fromarray(image) for image in self.images)
        elif isinstance(self.images[0], Image.Image):
            ...

    def _image2array(self):
        if isinstance(self.images[0], Image.Image):
            self.images = tuple(np.array(image) for image in self.images)
        elif isinstance(self.images[0], np.ndarray):
            ...

    def make_frame_sub_cls(self, t):
        self._image2array()
        if self.fps is None or self.duration is None:
            raise ValueError("FPS and duration must be set before generating frames.")

        frame_index = int(t * self.fps)
        if frame_index >= len(self.images):
            raise ValueError(f"Frame index {frame_index} exceeds the number of images in the sequence.")

        return self.images[frame_index]

    def make_frame_pil_sub_cls(self, t):
        self._array2image()
        if self.fps is None or self.duration is None:
            raise ValueError("FPS and duration must be set before generating frames.")
        frame_index = int(t * self.fps)
        if frame_index >= len(self.images):
            raise ValueError(f"Frame index {frame_index} exceeds the number of images in the sequence.")
        return self.images[frame_index]

    @override
    def iterate_frames_array_t(self, fps: Num):
        frame_t_dif = (1 / fps)
        st_0 = 0.0
        while st_0 < self.duration if self.duration is not None else (_ for _ in ()).throw(Exception('Duration is Not Set.')):
            yield self.make_frame(st_0)
            st_0 += frame_t_dif

    @override
    def iterate_frames_pil_t(self, fps: Num):
        frame_t_dif = (1 / fps)
        st_0 = 0.0
        while st_0 < self.duration if self.duration is not None else (_ for _ in ()).throw(Exception('Duration is Not Set.')):
            yield self.make_frame_pil(st_0)
            st_0 += frame_t_dif

class ColorClip(Data2ImageClip):
    def __init__(self, color: str | tuple[int, ...], mode='RGBA', size=(1, 1), fps=None, duration=None):
        data = Image.new(mode, size, color) # type: ignore
        super().__init__(data, fps=fps, duration=duration)

class TextClip(Data2ImageClip):
    def __init__(self, text: str, font_pth: None | str = None, font_size: int = 20, txt_color: str | tuple[int, ...]=(255, 255, 255), 
                 bg_color: str | tuple[int,...] = (0, 0, 0, 0), fps=None, duration=None):
        font = ImageFont.truetype(font_pth, font_size) if font_pth else ImageFont.load_default(font_size)
        
        # Get the bounding box of the text
        bbox = font.getbbox(text)
        # Calculate the image size to fit the text with some padding
        image_width = bbox[2] + bbox[0] # + 20  # Adding 20 pixels padding
        image_height = bbox[3] + bbox[1] # + 20  # Adding 20 pixels padding
        image = Image.new("RGBA", (image_width, image_height), bg_color) # type: ignore
        
        # Draw the text on the image
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, align='center', fill=txt_color) # type: ignore

        super().__init__(image, fps=fps, duration=duration)

if __name__ == '__main__':
    ...