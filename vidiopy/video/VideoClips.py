from abc import abstractmethod
from fractions import Fraction
import os
from copy import copy as copy_
from pathlib import Path
from re import T
import subprocess
import tempfile
from typing import (Callable, TypeAlias, Self, override)
from PIL import Image
import ffmpegio
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from pydub import AudioSegment
from ..Clip import Clip
from ..audio.AudioClip import AudioFileClip, AudioClip, CompositeAudioClip, audio_segment2composite_audio_clip
from ..decorators import *

Num: TypeAlias = int | float
NumOrNone: TypeAlias = Num | None


class VideoClip(Clip):
    def __init__(self) -> None:
        super().__init__()

        # Time-related properties
        self.start: Num = 0.0
        self.end: NumOrNone = None
        self.duration: NumOrNone = None

        # Video and audio properties
        self.audio: AudioClip | None = None
        self.fps: NumOrNone = None
        self.size: tuple[int, int] | None = None

        # Position-related properties
        self.pos = lambda t: (0, 0)
        self.relative_pos = False

        # Frame generation properties
        self.make_frame: Callable[..., np.ndarray] = lambda t: (_ for _ in ()).throw(Exception('Make Frame is Not Set.'))
        self.make_frame_pil = lambda t: (_ for _ in ()).throw(Exception('Make Frame pil is Not Set.'))
        self.make_frame_any = lambda t: (_ for _ in ()).throw(Exception('Make Frame any is Not Set.'))

    @property
    @requires_size
    def width(self):
        if self.size is not None:
            return self.size[0]
        else:
            raise ValueError("Size is not set")
    
    w = width

    @property
    @requires_size
    def height(self):
        if self.size is not None:
            return self.size[1]
        else:
            raise ValueError("Size is not set")
    
    h = height
    @property
    @requires_size
    def aspect_ratio(self):
        if isinstance(self.w, int) and isinstance(self.w, int):
            return Fraction(self.w, self.h)
        else:
            raise ValueError("Size is not set")

    def set_start(self, t, change_end=True):
        self.start = t

        if self.start is None:
            return self

        if self.duration is not None and change_end:
            self.end = t + self.duration
        elif self.end is not None:
            self.duration = self.end - self.start

        return self

    def set_end(self, t, change_start=False) -> Self:
        self.end = t

        if self.end is None:
            return self

        if self.start and change_start:
            if self.duration is not None:
                self.start = max(0, t - self.duration)
        else:
            self.duration = max(0, self.end - self.start)

        return self

    def set_duration(self, t, change_end=True):
        self.duration = t

        if change_end and self.start is not None:
            self.end = None if t is None else (self.start + t)
        else:
            if self.duration is None:
                raise ValueError("Cannot change clip start when new duration is None")
            self.start = self.end - self.duration

        return self

    def set_position(self, pos, relative=False):
        self.relative_pos = relative

        if hasattr(pos, '__call__'):
            self.pos = pos
        else:
            self.pos = lambda t: pos

        return self

    def set_audio(self, audio: AudioClip):
        self.audio = audio
        return self

    def without_audio(self):
        self.audio = None
        return self

    def set_make_frame(self, func):
        self.make_frame = func
        return self

    def set_make_frame_pil(self, func):
        self.make_frame_pil = func
        return self

    def set_make_frame_any(self, func):
        self.make_frame_any = func
        return self

    def set_fps(self, fps):
        self.fps = fps
        return self

    def __copy__(self):
        # Get the class of the current instance
        cls = self.__class__

        # Create a new instance of the class
        new_clip = cls.__new__(cls)

        # Iterate through the attributes of the current instance
        for attr, value in self.__dict__.items():
            # If the attribute is 'audio', make a shallow copy
            if attr == "audio":
                value = copy_(value)

            # Set the attribute in the new instance
            setattr(new_clip, attr, value)

        # Return the shallow copy
        return new_clip

    # Alias for the __copy__ method
    copy = __copy__

    def get_frame(self, t, is_pil=None):
        if is_pil is None or is_pil is False:
            return self.make_frame(t)
        elif is_pil is True:
            return self.make_frame_pil(t)
        else:
            return self.make_frame_any(t)

    def iterate_all_frames_array(self):
        while True:
            yield np.zeros((self.h, self.w, 3), dtype=np.uint8)
            
            raise NotImplementedError("iterate_all_frames_array method must be overridden in the subclass.")

    def iterate_all_frames_pil(self):
        while True:
            yield np.zeros((self.h, self.w, 3), dtype=np.uint8)
            raise NotImplementedError("iterate_all_frames_pil method must be overridden in the subclass.")

    def iterate_frames_pil_t(self, fps: Num):
        time_dif = 1 / fps
        x = 0
        if self.end is not None:
            while x <= self.end:
                yield self.get_frame(x, is_pil=True)
                x += time_dif
        else:
            raise ValueError('end Is None')

    def iterate_frames_array_t(self, fps: Num):
        time_dif = 1 / fps
        x = 0
        if self.end is not None:
            while x <= self.end:
                yield self.get_frame(x, is_pil=False)
                x += time_dif
        else:
            raise ValueError('end Is None')

    def sub_fx(self):
        raise NotImplementedError("sub_fx method must be overridden in the subclass.")

    def fl(self, func, *args, **kwargs):
        """\
        Call The Function Like Follows
        >>> func(tuple(Frame, Frame_time, StartTime, EndTime), *args, **Kwargs)\
        """
        raise NotImplementedError("fl method must be overridden in the subclass.")

    def fx(self, func, *args, **kwargs):
        
        raise NotImplementedError("fx method must be overridden in the subclass.")

    def write_videofile(self, filename, fps=None, codec=None,   
                        bitrate=None, audio=True, audio_fps=44100,
                        preset="medium", pixel_format=None,
                        audio_codec=None, audio_bitrate=None,
                        write_logfile=False, verbose=True,
                        threads=None, ffmpeg_params: dict[str, str] | None = None,
                        logger='bar', over_write_output=True):
        
        # Generate video frames using iterate_frames_array_t method
        video_np = np.asarray(tuple(
            self.iterate_frames_array_t(fps if fps else self.fps if self.fps else
                                        (_ for _ in ()).throw(Exception('Make Frame is Not Set.')))
        ))

        # Extract audio name without extension
        audio_name, _ = os.path.splitext(filename)

        # Set default values for ffmpeg options
        ffmpeg_options = {
            'preset': preset,
            **(ffmpeg_params if ffmpeg_params is not None else {}),
            **({'c:v': codec} if codec else {}),
            **({'b:v': bitrate} if bitrate else {}),
            **({'pix_fmt': pixel_format} if pixel_format else {}),
            **({'c:a': audio_codec} if audio_codec else {}),
            **({'ar': audio_fps} if audio_fps else {}),
            **({'b:a': audio_bitrate} if audio_bitrate else {}),
            **({'threads': threads} if threads else {}),
        }

        audio_file_name = None
        temp_video_file_name = None

        try:
            # Determine the fps to use
            fps_to_use = fps if fps else self.fps if self.fps else None

            # Create a temporary video file
            dir__, file__ = os.path.split(filename)
            temp_video_file = tempfile.NamedTemporaryFile(
                dir=dir__, suffix="video__temp__" + os.path.splitext(file__)[1], delete=False
            )
            temp_video_file_name = temp_video_file.name
            temp_video_file.close()

            # Write video frames to the temporary file using ffmpegio
            ffmpegio.video.write(
                temp_video_file_name,
                fps_to_use,
                video_np,
                show_log=True,
                overwrite=over_write_output,
                **ffmpeg_options
            )

            if self.audio and audio:
                temp_audio_file = tempfile.NamedTemporaryFile(
                    suffix=".wav", prefix=audio_name + "_temp_audio_", delete=False
                )
                audio_file_name = temp_audio_file.name
                temp_audio_file.close()

                # Write audio to the temporary file
                self.audio.write_audio_file(audio_file_name)

                # Combine video and audio using ffmpeg
                result = subprocess.run(
                    f'ffmpeg -i {temp_video_file_name} -i {audio_file_name} -acodec copy '
                    f'{"-y" if over_write_output else ""} {filename}',
                    capture_output=True, text=True
                )
                print("Command output:", result.stdout)

        except Exception as e:
            raise e

        finally:
            # Clean up temporary files
            print('\n'*10)
            print(f'''{audio_file_name=}, {bool(audio_file_name)=}, 
                  {temp_video_file_name=}, {bool(temp_video_file_name)=}, 
                  {filename=}, {bool(filename)=}''')
            
            if audio_file_name:
                os.remove(audio_file_name)

            # Rename temporary video file to the final filename if no audio is present
            if (not self.audio or not audio) and temp_video_file_name:
                print('Running renaming')
                os.replace(temp_video_file_name, filename)
                temp_video_file_name = None

            if temp_video_file_name:
                os.remove(temp_video_file_name)

    def write_image_sequence(self, nformat, fps=None, dir='.', logger='bar'):
        # Initialize the frame number
        frame_number = 0

        # Function to save a frame to the specified directory with the appropriate file name
        def save_frame(frame, frame_number):
            file_path = os.path.join(dir, f"{frame_number:04d}{nformat}")
            frame.save(file_path)

        # Check if the specified directory exists, and create it if not
        if dir != '.' and not os.path.exists(dir):
            os.makedirs(dir)

        # Determine the frames generator based on the provided fps or the object's properties
        if fps:
            frames_generator = self.iterate_frames_pil_t(fps)
        elif self.fps and self.duration:
            frames_generator = self.iterate_frames_pil_t(self.fps)
        else:
            # Print a warning if neither fps nor object's properties are set
            print("Warning: FPS is not provided, and fps and duration are not set.")
            frames_generator = self.iterate_all_frames_pil()

        # Iterate through frames and save them to the specified directory
        for frame in frames_generator:
            save_frame(frame, frame_number)
            frame_number += 1

    def to_ImageClip(self, t):
        return Data2ImageClip(self.get_frame(t, is_pil=True))


class VideoFileClip(VideoClip):
    def __init__(self, filename, audio=True, ffmpeg_options=None):
        super().__init__()

        # Probe video streams and extract relevant information
        video_data = ffmpegio.probe.video_streams_basic(filename)[0]

        # Import video clip using ffmpeg
        self.clip = self._import_video_clip(filename, ffmpeg_options)

        # Set video properties
        self.fps: float = float(video_data['frame_rate'])
        self.size = (video_data['width'], video_data['height'])
        self.start = 0.0
        self.end = self.duration = video_data['duration']

        # Set frame generation functions
        self.set_make_frame_any(self.make_frame_any_sub_cls)
        self.set_make_frame(self.make_frame_sub_cls)
        self.set_make_frame_pil(self.make_frame_pil_sub_cls)

        # If audio is enabled, attach audio clip
        if audio:
            audio = AudioFileClip(filename)
            self.set_audio(audio)

    def _array2image(self):
        # Convert numpy array frames to PIL Image
        if isinstance(self.clip[0], np.ndarray):
            new_clip = [Image.fromarray(frame) for frame in self.clip]
            self.clip = np.array(new_clip)
        elif isinstance(self.clip[0], Image.Image):
            # Already in the correct format
            pass
        elif self.clip is None:
            raise ValueError("Clip is not Set.")
        else:
            raise ValueError("Clip is not an image or numpy array")

    def _image2array(self):
        # Convert PIL Image frames to numpy array
        if isinstance(self.clip[0], Image.Image):
            new_clip = [np.asarray(frame) for frame in self.clip]
            self.clip = np.array(new_clip)
        elif isinstance(self.clip[0], np.ndarray):
            # Already in the correct format
            pass
        elif self.clip is None:
            raise ValueError("Clip is not Set.")
        else:
            raise ValueError("Clip is not an image or numpy array")

    @requires_duration
    @requires_start_end
    def fl(self, f, *args, **kwargs):
        # Apply a function to each frame and return a new VideoFileClip
        clip = self.clip
        st = self.start
        ed = self.end
        dur = self.duration
        fps = self.fps
        td = 1 / fps
        t = 0.0
        self._array2image()
        clip = []
        while t <= dur:
            frame = self.make_frame_pil(t)
            clip.append(f(_do_not_pass=(frame, t, st, ed), *args, **kwargs))
            t += td
        self.clip = np.array(clip)
        return self

    def fx(self, func: Callable, *args, **kwargs):
        # Apply an effect function directly to the clip
        func(*args, **kwargs)
        return self

    def make_frame_any_sub_cls(self, t):
        # Frame generation function for arbitrary frame types
        frame_num = t * self.fps
        return self.clip[int(frame_num)]

    def make_frame_sub_cls(self, t):
        # Frame generation function returning numpy array
        frame_num = t * self.fps
        return np.array(self.clip[int(frame_num)])

    def make_frame_pil_sub_cls(self, t):
        # Frame generation function returning PIL Image
        frame_num = t * self.fps
        return Image.fromarray(self.clip[int(frame_num)])

    def _import_video_clip(self, file_name, ffmpeg_options):
        # Import video clip using ffmpeg
        options = {
            **(ffmpeg_options if ffmpeg_options else {})
        }
        return ffmpegio.video.read(file_name, **options)[1]


class ImageClip(VideoClip):
    def __init__(self, image: str | Path | None = None, fps: NumOrNone = None, duration: NumOrNone = None):
        super().__init__()

        # Import image if provided
        self.image = self._import_image(image) if image else None

        # Set frame generation functions
        self.set_make_frame_any(self.make_frame_any_image_clip)
        self.set_make_frame(self.make_frame_image_clip)
        self.set_make_frame_pil(self.make_frame_pil_image_clip)

        # Set properties
        self.fps = fps
        self.duration = duration
        self.start = 0.0
        self.end = self.duration
        self.size = self.image.size if self.image is not None else None

    def _import_image(self, image):
        # Import image using PIL
        return Image.open(image)

    def fl(self, f, *args, **kwargs):
        # Apply a function to the image and return the modified ImageClip
        self._array2image()
        self.image = f(_do_not_pass=(self.image, self.duration, self.start, self.end), *args, **kwargs)
        return self

    def fx(self, func: Callable, *args, **kwargs):
        # Apply an effect function directly to the ImageClip
        self._array2image()
        func(*args, **kwargs)
        return self

    def _array2image(self):
        # Convert numpy array image to PIL Image
        if isinstance(self.image, np.ndarray):
            self.image = Image.fromarray(self.image)
        elif isinstance(self.image, Image.Image):
            # Already in the correct format
            pass
        elif self.image is None:
            raise ValueError("Image is not set.")
        else:
            raise ValueError("Image is not an image or numpy array")

    def _image2array(self):
        # Convert PIL Image to numpy array
        if isinstance(self.image, Image.Image):
            self.image = np.array(self.image)
        elif isinstance(self.image, np.ndarray):
            # Already in the correct format
            pass
        elif self.image is None:
            raise ValueError("Image is not set.")
        else:
            raise ValueError("Image is not an image or numpy array")

    def make_frame_image_clip(self, t):
        # Frame generation function returning the current image
        self._image2array()
        return self.image

    def make_frame_any_image_clip(self, t):
        # Frame generation function returning the current image
        return self.image

    def make_frame_pil_image_clip(self, t):
        # Frame generation function returning the current image
        self._array2image()
        return self.image

    def to_video_clip(self, fps=None, duration=None, start=None, end=None):
        # Convert ImageClip to VideoClip
        if fps is None:
            fps = self.fps
        if duration is None:
            duration = self.duration
        if start is None:
            start = self.start
        if end is None:
            end = self.end

        # Check if necessary parameters are set
        if fps is None or duration is None or start is None or end is None:
            raise ValueError("FPS, duration, start, and end must be set before converting to a video clip.")

        # Generate frames using iterate_frames_array_t
        frames = list(self.iterate_frames_array_t(fps))
        
        # Create ImageSequenceClip from frames
        return ImageSequenceClip(frames, fps=fps).set_start(start).set_end(end)


class Data2ImageClip(ImageClip):
    def __init__(self, data: np.ndarray | Image.Image, fps: NumOrNone = None, duration: NumOrNone = None):
        # Initialize the class by calling the parent constructor
        super().__init__(fps=fps, duration=duration)

        # Import the image from the provided data
        self.image = self._import_image(data)
        
        # Set the size attribute based on the image size
        self.size = self.image.size

    def _import_image(self, image):
        # Convert the provided data (numpy array or PIL Image) into a PIL Image
        if isinstance(image, np.ndarray):
            return Image.fromarray(image)
        elif isinstance(image, Image.Image):
            return image
        else:
            # Raise an error if the input type is not supported
            raise TypeError(f"{type(image)} is not an Image.Image or numpy array Type.")


class ImageSequenceClip(VideoClip):
    def __init__(self, images: str | Path | list[str | Path | Image.Image | np.ndarray] | np.ndarray, fps: NumOrNone = None):
        # Call the parent class constructor
        super().__init__()

        # Import images from the provided data
        self.images = self._import_images(images)

        # Set frame generation functions
        self.set_make_frame(self.make_frame_sub_cls)
        self.set_make_frame_pil(self.make_frame_pil_sub_cls)

        # Set properties
        self.fps = fps
        self.duration = len(self.images)*(fps if fps is not None and fps else 0) # Brackets are important other wise: - Duration = fps
        self.start = 0.0
        self.end = self.duration

        # Set size attribute based on the size of the first image
        self.size = self.images[0].size

    def _import_images(self, images):
        # Check if the input is a single path (string or Path)
        if isinstance(images, (str, Path)):
            images_path = Path(images)
            # If it's a directory, load all supported image files in sorted order
            if images_path.is_dir():
                supported_extensions = {ext.lower() for ext in Image.registered_extensions()}
                image_files = tuple(sorted([file for file in images_path.iterdir() if file.is_file() and file.suffix.lower() in supported_extensions]))
                # Return a tuple of Image objects created from the files
                return tuple(Image.open(str(image)) for image in image_files)
            else:
                # If it's not a directory, raise a ValueError
                raise ValueError(f"{images} is not a directory.")
        # Check if the input is a collection of paths (list, tuple, set)
        elif isinstance(images, (list, tuple, set)):
            # Return a tuple of Image objects created from the paths in the collection
            return tuple(Image.open(str(image)) for image in images)
        # Check if the input is a NumPy array
        elif isinstance(images, np.ndarray):
            # Return a tuple of Image objects created from the NumPy array
            return tuple(Image.fromarray(image) for image in images)
        else:
            # If the input is not of any expected type, raise a ValueError
            raise ValueError("Invalid input. Provide a directory path, a list/tuple/set of paths, or a NumPy array.")

    def set_fps(self, fps: Num):
        self.fps = fps
        self.duration = len(self.images)*fps
        return self

    @requires_fps
    @requires_duration
    @override
    def fl(self, f, *args, **kwargs):
        td = 1 / self.fps # type: ignore
        t = 0.0
        st = self.start
        ed = self.end
        frames = []
        while t <= self.duration:
            frames.append(f((self.make_frame_pil_sub_cls(t), t, st, ed), *args, **kwargs))
            t += td
        self.images = tuple(frames)
        return self

    @requires_fps
    @requires_duration
    def fx(self, func: Callable, *args, **kwargs):
        func(*args, **kwargs)

    def _array2image(self):
        if isinstance(self.images[0], np.ndarray):
            # If the first image is a NumPy array, convert all array images to PIL Image
            self.images = tuple(Image.fromarray(image) for image in self.images)
        elif isinstance(self.images[0], Image.Image):
            # If the first image is already a PIL Image, do nothing (placeholder for future extensions)
            pass

    def _image2array(self):
        if isinstance(self.images[0], Image.Image):
            # If the first image is a PIL Image, convert all image objects to NumPy arrays
            self.images = tuple(np.array(image) for image in self.images)
        elif isinstance(self.images[0], np.ndarray):
            # If the first image is already a NumPy array, do nothing (placeholder for future extensions)
            pass

    @requires_fps
    def make_frame_sub_cls(self, t):
        # Convert images to arrays if they are not already in array format
        self._image2array()

        # Calculate the frame index based on time and FPS
        frame_index = int(t * self.fps)

        # Check if the calculated frame index is within the valid range
        if frame_index >= len(self.images):
            raise ValueError(f"Frame index {frame_index} exceeds the number of images in the sequence.")

        # Return the generated frame
        return self.images[frame_index]

    def make_frame_pil_sub_cls(self, t):
        # Convert images to PIL format if they are not already in that format
        self._array2image()

        # Check if FPS and duration are set
        if self.fps is None or self.duration is None:
            raise ValueError("FPS and duration must be set before generating frames.")

        # Calculate the frame index based on time and FPS
        frame_index = int(t * self.fps)

        # Check if the calculated frame index is within the valid range
        if frame_index >= len(self.images):
            raise ValueError(f"Frame index {frame_index} exceeds the number of images in the sequence.")

        # Return the generated frame as a PIL Image
        return self.images[frame_index]

    @requires_duration
    def iterate_frames_array_t(self, fps: Num):
        frame_t_dif = (1 / fps)
        st_0 = 0.0
        while st_0 < self.duration:
            yield self.make_frame(st_0)
            st_0 += frame_t_dif

    @requires_duration
    def iterate_frames_pil_t(self, fps: Num):
        frame_t_dif = (1 / fps)
        st_0 = 0.0
        while st_0 < self.duration:
            yield self.make_frame_pil(st_0)
            st_0 += frame_t_dif


class ColorClip(Data2ImageClip):
    def __init__(self, color: str | tuple[int, ...], mode='RGBA', size=(1, 1), fps=None, duration=None):
        data = Image.new(mode, size, color) # type: ignore
        super().__init__(data, fps=fps, duration=duration)


class TextClip(Data2ImageClip):
    def __init__(self, text: str, font_pth: None | str = None, font_size: int = 20, txt_color: str | tuple[int, ...]=(255, 255, 255), 
                 bg_color: str | tuple[int,...] = (0, 0, 0, 0), fps=None, duration=None):
        font = ImageFont.truetype(font_pth, font_size) if font_pth else ImageFont.load_default()

        bbox = font.getbbox(text)
        image_width, image_height = bbox[2] - bbox[0] + 20, bbox[3] - bbox[1] + 20

        image = Image.new("RGBA", (image_width, image_height), bg_color)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), text, font=font, align='center', fill=txt_color)

        super().__init__(image, fps=fps, duration=duration)


class CompositeVideoClip(VideoClip):
    def __init__(self, clips: list[VideoClip], size=None, bg_color=None, use_bgclip=False, fps=None, audio=None):
        super().__init__()
        if use_bgclip:
            self.bg_clip = clips[0]
            self.clips = clips[1:]
        else:
            max_width = 0
            max_height = 0

            for my_class in clips:
                if my_class.size is None:
                    raise ValueError("Size cannot be None")

                width, height = my_class.size
                max_width = max(max_width, width)
                max_height = max(max_height, height)
            
            self.bg_clip = Data2ImageClip(Image.new('RGBA', (max_width, max_height), bg_color if bg_color else (0, 0, 0, 0)))
            self.clips = clips
            self.blank_bg_Image = Image.new('RGBA', 
                                        self.bg_clip.size if self.bg_clip.size is not None else 
                                        self.size if self.size else 
                                        (_ for _ in ()).throw(Exception('Bg_clip has no attr size.')), 
                                        (0, 0, 0, 0))
        
        if fps:
            self.set_fps(fps)
        else:
            fpss = [c.fps for c in clips if getattr(c, 'fps', None) is not None and isinstance(c.fps, (int, float))]
            self.set_fps(max(fpss) if fpss else None)
        
        duration = 0

        if use_bgclip:
            duration = self.bg_clip.duration if self.bg_clip.duration is not None else (_ for _ in ()).throw(ValueError('Bg_clip duration is not Set.'))
        else:
            for obj in clips:
                if hasattr(obj, 'duration') and obj.duration is not None:
                    if obj.duration > duration:
                        duration = obj.duration


        # if audio:
        #     if use_bgclip:
        #         if self.bg_clip.duration or self.bg_clip.end:
        #             if isinstance(self.bg_clip.audio, AudioClip):
        #                 if isinstance(self.bg_clip.audio.clip, AudioSegment):
        #                     a_fps = self.bg_clip.audio.clip.frame_rate
        #                     bg_audio = self.bg_clip.audio.clip
        #                     ast = self.bg_clip.start
        #                     aed = self.bg_clip.end
        #                     if aed is None: bg_audio = bg_audio[ast*1000:]
        #                     else: bg_audio = bg_audio[ast*1000:aed*1000]
        #                     for clip in self.clips:
        #                         if clip.duration or clip.end:
        #                             ac_st = clip.start
        #                             ac_ed = clip.duration
        #                             if isinstance(clip.audio, AudioClip):
        #                                 if isinstance(clip.audio.clip, AudioSegment):
        #                                     audio_c = clip.audio.clip
        #                                     if ac_ed is not None: audio_c = audio_c[ac_st*1000: ac_ed*1000]
        #                                     else: audio_c = audio_c[ac_st*1000]
        #                                     bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore

        #                                 else:
        #                                     if ac_ed is not None:
        #                                         audio_c = AudioSegment.silent(int(ac_ed*1000))
        #                                         bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                             else:
        #                                 if ac_ed is not None:
        #                                     audio_c = AudioSegment.silent(int(ac_ed*1000))
        #                                     bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                         else:
        #                             raise ValueError('Clip Duration is Not Set')
        #                 else:
        #                     a_fps = 44100
        #                     bg_audio = AudioSegment.silent(int((self.bg_clip.duration or self.bg_clip.end)*1000), a_fps) # type: ignore
        #                     ast = self.bg_clip.start
        #                     aed = self.bg_clip.end
        #                     if aed is None: bg_audio = bg_audio[ast*1000:]
        #                     else: bg_audio = bg_audio[ast*1000:aed*1000]
        #                     for clip in self.clips:
        #                         if clip.duration or clip.end:
        #                             ac_st = clip.start
        #                             ac_ed = clip.duration
        #                             if isinstance(clip.audio, AudioClip):
        #                                 if isinstance(clip.audio.clip, AudioSegment):
        #                                     audio_c = clip.audio.clip
        #                                     if ac_ed is not None: audio_c = audio_c[ac_st*1000: ac_ed*1000]
        #                                     else: audio_c = audio_c[ac_st*1000]
        #                                     bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore

        #                                 else:
        #                                     if ac_ed is not None:
        #                                         audio_c = AudioSegment.silent(int(ac_ed*1000))
        #                                         bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                             else:
        #                                 if ac_ed is not None:
        #                                     audio_c = AudioSegment.silent(int(ac_ed*1000))
        #                                     bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                         else:
        #                             raise ValueError('Clip Duration is Not Set')
        #             else:
        #                 a_fps = 44100
        #                 bg_audio = AudioSegment.silent(int((self.bg_clip.duration or self.bg_clip.end)*1000), a_fps) # type: ignore
        #                 ast = self.bg_clip.start
        #                 aed = self.bg_clip.end
        #                 if aed is None: bg_audio = bg_audio[ast*1000:]
        #                 else: bg_audio = bg_audio[ast*1000:aed*1000]
        #                 for clip in self.clips:
        #                     if clip.duration or clip.end:
        #                         ac_st = clip.start
        #                         ac_ed = clip.duration
        #                         if isinstance(clip.audio, AudioClip):
        #                             if isinstance(clip.audio.clip, AudioSegment):
        #                                 audio_c = clip.audio.clip
        #                                 if ac_ed is not None: audio_c = audio_c[ac_st*1000: ac_ed*1000]
        #                                 else: audio_c = audio_c[ac_st*1000]
        #                                 bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                             else:
        #                                 if ac_ed is not None:
        #                                     audio_c = AudioSegment.silent(int(ac_ed*1000))
        #                                     bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                         else:
        #                             if ac_ed is not None:
        #                                 audio_c = AudioSegment.silent(int(ac_ed*1000))
        #                                 bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                     else:
        #                         raise ValueError('Clip Duration is Not Set')
        #         else:
        #             raise ValueError("Bg Clip 'Duration' and 'End' is Not Set")
        #     else:
        #         a_fps = 44100
        #         bg_audio = AudioSegment.empty() # type: ignore
        #         ast = self.bg_clip.start
        #         aed = self.bg_clip.end
        #         if aed is None: bg_audio = bg_audio[ast*1000:]
        #         else: bg_audio = bg_audio[ast*1000:aed*1000]
        #         for clip in self.clips:
        #             if clip.duration or clip.end:
        #                 ac_st = clip.start
        #                 ac_ed = clip.duration
        #                 if isinstance(clip.audio, AudioClip):
        #                     if isinstance(clip.audio.clip, AudioSegment):
        #                         audio_c = clip.audio.clip
        #                         if ac_ed is not None: audio_c = audio_c[ac_st*1000: ac_ed*1000]
        #                         else: audio_c = audio_c[ac_st*1000]
        #                         bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                     else:
        #                         if ac_ed is not None:
        #                             audio_c = AudioSegment.silent(int(ac_ed*1000))
        #                             bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #                 else:
        #                     if ac_ed is not None:
        #                         audio_c = AudioSegment.silent(int(ac_ed*1000))
        #                         bg_audio.overlay(audio_c, int(ac_st*1000))  # type: ignore
        #             else:
        #                 raise ValueError('Clip Duration is Not Set')
        #         bg_audio.set_frame_rate(a_fps) # type: ignore
        # else:
            audio_clip = None
        if audio:
            if use_bgclip:
                self._process_bgclip_audio()
            else:
                self._process_no_bgclip_audio()
        else:
            audio_clip = None

        audio_clip = AudioClip()
        audio_clip.clip = bg_audio # type: ignore
        self.audio = audio_clip
        self.set_make_frame_any(self.make_frame_composite_any)
        self.set_make_frame(self.make_frame_composite)
        self.set_make_frame_pil(self.make_frame_composite_pil)
        self.size = size
        self.bg_color = bg_color
        self.use_bgclip = use_bgclip
        self.duration = duration
        self.start = 0.0
        self.end = self.duration

    def _process_bgclip_audio(self):
        if self.bg_clip.duration or self.bg_clip.end:
            bg_audio = self._get_bg_audio_segment()
            for clip in self.clips:
                if clip.duration or clip.end:
                    audio_c = self._get_audio_clip_segment(clip)
                    bg_audio = self.overlay_audio(bg_audio, audio_c, clip.start)

            bg_audio.set_frame_rate(self._get_frame_rate())
        else:
            raise ValueError("Bg Clip 'Duration' and 'End' is Not Set")

    def _process_no_bgclip_audio(self):
        a_fps = 44100
        bg_audio = AudioSegment.empty()

        for clip in self.clips:
            if clip.duration or clip.end:
                audio_c = self._get_audio_clip_segment(clip)
                bg_audio = self.overlay_audio(bg_audio, audio_c, clip.start)

        bg_audio.set_frame_rate(a_fps)

    def _get_bg_audio_segment(self):
        a_fps = self.bg_clip.audio.clip.frame_rate
        bg_audio = self.bg_clip.audio.clip
        ast, aed = self.bg_clip.start, self.bg_clip.end

        if aed is None:
            bg_audio = bg_audio[ast * 1000:]
        else:
            bg_audio = bg_audio[ast * 1000: aed * 1000]

        return bg_audio

    def _get_frame_rate(self):
        return 44100

    def _get_audio_clip_segment(self, clip):
        ac_st, ac_ed = clip.start, clip.duration

        if isinstance(clip.audio, AudioClip) and isinstance(clip.audio.clip, AudioSegment):
            audio_c = clip.audio.clip
            if ac_ed is not None:
                audio_c = audio_c[ac_st * 1000: ac_ed * 1000]
            else:
                audio_c = audio_c[ac_st * 1000]
        else:
            audio_c = AudioSegment.silent(int(ac_ed * 1000))

        return audio_c

    def to_video_clip(self, fps=None, duration=None, start=None, end=None):
        if fps is None:
            fps = self.fps
        if duration is None:
            duration = self.duration
        if start is None:
            start = self.start
        if end is None:
            end = self.end

        if fps is None or duration is None or start is None or end is None:
            raise ValueError("FPS, duration, start, and end must be set before converting to a video clip.")

        frames = list(self.make_frame_composite(fps))
        return ImageSequenceClip(frames, fps=fps).set_start(start).set_end(end)

    def overlay_audio(self, bg_audio, audio_c, start_time):
        return bg_audio.overlay(audio_c, int(start_time * 1000))

    def make_frame_composite(self, t):
        return np.array(self.make_frame_composite_pil(t))

    def make_frame_composite_any(self, t):
        self.make_frame_composite_pil(t)

    def make_frame_composite_pil(self, t):
        bg_image = None
        if self.bg_clip.start is not None and self.bg_clip.end is None:
            if self.bg_clip.start <= t:
                bg_image = self.bg_clip.make_frame_pil(t)
            else:
                bg_image = None
        elif self.bg_clip.start is None and self.bg_clip.end is not None:
            if self.bg_clip.end >= t:
                bg_image = self.bg_clip.make_frame_pil(t)
            else:
                bg_image = None
        elif self.bg_clip.start is None and self.bg_clip.end is None:
                bg_image = self.bg_clip.make_frame_pil(t)

        if bg_image is None:
            bg_image = self.blank_bg_Image.copy()

        for clip in self.clips:
            st = clip.start
            ed = clip.end
            if st is None and ed is not None:
                if ed >= t:
                    pos = clip.pos(t)
                    clip_frame: Image.Image = clip.make_frame_pil(t)
                    bg_image.paste(clip_frame, pos, mask=clip_frame)
            elif st is not None and ed is None:
                if st <= t:
                    pos = clip.pos(t)
                    clip_frame: Image.Image = clip.make_frame_pil(t)
                    bg_image.paste(clip_frame, pos, mask=clip_frame)
            elif st is None and ed is None:
                pos = clip.pos(t)
                clip_frame: Image.Image = clip.make_frame_pil(t)
                bg_image.paste(clip_frame, pos, mask=clip_frame if clip_frame.mode=='RGBA' else None)
            elif st is not None and ed is not None:
                if st <= t <= ed:
                    pos = clip.pos(t)
                    clip_frame: Image.Image = clip.make_frame_pil(t)
                    bg_image.paste(clip_frame, pos, mask=clip_frame if clip_frame.mode=='RGBA' else None)
            else:
                raise ValueError(f'{clip.start=}, {clip.end=} are invalid.')
        return bg_image


if __name__ == '__main__':
    SystemExit()