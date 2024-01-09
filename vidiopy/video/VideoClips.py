from rich import print
import rich.progress as progress
from fractions import Fraction
import os
from copy import copy as copy_
from pathlib import Path
from re import T
import subprocess
import tempfile
from typing import (Callable, TypeAlias, Generator, override, Any, Self)
from abc import ABC, abstractmethod
from PIL import Image, ImageFont, ImageDraw
import ffmpegio
import numpy as np
from pydub import AudioSegment
from ..Clip import Clip
from ..audio.AudioClip import AudioFileClip, AudioClip, CompositeAudioClip
from ..decorators import *

Num: TypeAlias = int | float
NumOrNone: TypeAlias = Num | None


class VideoClip(ABC, Clip):
    def __init__(self) -> None:
        super().__init__()

        # Time-related properties
        self._st: Num = 0.0
        self._ed: NumOrNone = None
        self._dur = None

        # Video and audio properties
        self.audio: AudioClip | None = None
        self.fps: NumOrNone = None
        self.size: tuple[int, int] | None = None

        # Position-related properties
        self.pos = lambda t: (0, 0)
        self.relative_pos = False

        # Frame generation properties
        self.make_frame_array: Callable[..., np.ndarray] = abstractmethod(lambda t: (_ for _ in ()).throw(Exception('Make Frame is Not Set.')))
        self.make_frame_pil: Callable[..., Image.Image] = abstractmethod(lambda t: (_ for _ in ()).throw(Exception('Make Frame pil is Not Set.')))
        self.make_frame_any: Callable[..., Image.Image] | Callable[..., np.ndarray] = abstractmethod(lambda t: (_ for _ in ()).throw(Exception('Make Frame any is Not Set.')))

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

    @property
    def start(self):
        return self._st

    @start.setter
    def start(self, t):
        self.start = t

        if self.start is None:
            return self

        if self.duration is not None:
            self.end = t + self.duration
        elif self.end is not None:
            self.duration = self.end - self.start

        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
            self.audio.duration = self.duration
        return self

    def set_start(self, t):
        self.start = t
        return self

    @property
    def end(self):
        return self._ed

    @end.setter
    def end(self, t):
        self._ed = t
        self.duration = self.start + self._ed
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
            self.audio.duration = self.duration
        return self

    def set_end(self, t):
        self.end = t
        return self

    @property
    def duration(self):
        return self._dur

    @duration.setter
    def duration(self, dur: NumOrNone=None):
        if self.end:
            if dur != self.start + self.end and dur is not None:
                self.end = self.start + dur
        if not dur:
            if self.end:
                self._dur = self.end - self.start
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
            self.audio.duration = self.duration
        return self

    def set_duration(self, dur):
        self.duration = dur
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

    def set_fps(self, fps):
        self.fps = fps
        return self

    def without_audio(self):
        self.audio = None
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
            return self.make_frame_array(t)
        elif is_pil is True:
            return self.make_frame_pil(t)
        else:
            return self.make_frame_any(t)

    def iterate_frames_pil_t(self, fps: Num) -> Generator[Image.Image, Any, None]:
        time_dif = 1 / fps
        t = self.start
        if self.end is not None:
            while t <= self.end:
                yield self.make_frame_pil(t)
                t += time_dif
        else:
            raise ValueError('end Is None')

    def iterate_frames_array_t(self, fps: Num):
        time_dif = 1 / fps
        t = 0
        if self.end is not None:
            while t <= self.end:
                yield self.make_frame_array(t)
                t += time_dif
        else:
            raise ValueError('end Is None')

    def iterate_frames_any_t(self, fps: Num):
        time_dif = 1 / fps
        t = 0
        if self.end is not None:
            while t <= self.end:
                yield self.make_frame_array(t)
                t += time_dif
        else:
            raise ValueError('end Is None')

    def sub_fx(self) -> Self:
        raise NotImplementedError("sub_fx method must be overridden in the subclass.")
        return self

    def fl(self, func, *args, **kwargs) -> Self:
        """\
        Call The Function Like Follows
        >>> func(*args, tuple(Frame, Frame_time, StartTime, EndTime), **Kwargs)\
        """
        raise NotImplementedError("fl method must be overridden in the subclass.")
        return Self

    def fx(self, func, *args, **kwargs):
        self.fl(func, *args, **kwargs)
        return self

    def _sync_audio_video_s_e_d(self):
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
            self.audio.duration = self.duration
        return self

    def write_videofile(self, filename, fps=None, codec=None,   
                        bitrate=None, audio=True, audio_fps=44100,
                        preset="medium", pixel_format=None,
                        audio_codec=None, audio_bitrate=None,
                        write_logfile=False, verbose=True,
                        threads=None, ffmpeg_params: dict[str, str] | None = None,
                        logger='bar', over_write_output=True):
        
        # Generate video frames using iterate_frames_array_t method
        total_frames = int((self.end - self.start) / (1 / (fps if fps else self.fps if self.fps else
                                            (_ for _ in ()).throw(Exception('Make Frame is Not Set.'))))) if self.end is not None else 0
        video_np = np.asarray(tuple(
            progress.track(self.iterate_frames_array_t(fps if fps else self.fps if self.fps else (_ for _ in ()).throw(Exception('Make Frame is Not Set.'))),
                           description='Processing Frames ...',
                           total=total_frames,
                           transient=True,
                           style='bar.back')
            ))
        print('[bold magenta]Vidiopy[/bold magenta] - Video Frames Has Been Processed :thumbs_up:.')
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
            with progress.Progress(transient=True) as progress_bar:
                current_frame = 0
                pbar = progress_bar.add_task(description='Writing Video File', total=total_frames, )
                def function_callback(status: dict, done:bool):
                    nonlocal current_frame
                    current_frame =  status['frame'] - current_frame
                    progress_bar.update(pbar, completed=current_frame, refresh = True)

                ffmpegio.video.write(
                    temp_video_file_name,
                    fps_to_use,
                    video_np,
                    overwrite=over_write_output,
                    progress=function_callback,
                    **ffmpeg_options
                )
                progress_bar.update(pbar, completed=True, visible=False)
            print('[bold magenta]Vidiopy[/bold magenta] - Video is Created :thumbs_up:')
            if self.audio and audio:
                self._sync_audio_video_s_e_d()
                temp_audio_file = tempfile.NamedTemporaryFile(
                    suffix=".wav", prefix=audio_name + "_temp_audio_", delete=False
                )
                audio_file_name = temp_audio_file.name
                temp_audio_file.close()

                # Write audio to the temporary file
                self.audio.write_audio_file(audio_file_name)

                # Combine video and audio using ffmpeg
                with progress.Progress(transient=True) as progress_bar:
                    sp = progress_bar.add_task("Combining Video & Audio", total=None)
                    result = subprocess.run(
                        f'ffmpeg -i {temp_video_file_name} -i {audio_file_name} -acodec copy '
                        f'{"-y" if over_write_output else ""} {filename}',
                        capture_output=True, text=True
                    )
                    progress_bar.update(sp, completed=True)
                print("[bold magenta]Vidiopy[/bold magenta] - ✔ Audio Video Combined :thumbs_up:")
            return self
        except Exception as e:
            raise e
        finally:
            if audio_file_name:
                os.remove(audio_file_name)
            # Rename temporary video file to the final filename if no audio is present
            if (not self.audio or not audio) and temp_video_file_name:
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
            total_frames = (1 / fps)*self.duration if self.duration else None
        elif self.fps and self.duration:
            frames_generator = self.iterate_frames_pil_t(self.fps)
            total_frames = (1 / self.fps)*self.duration if self.duration else None
        else:
            # Print a warning if neither fps nor object's properties are set
            raise ValueError("Warning: FPS is not provided, and fps and duration are not set.")


        # Iterate through frames and save them to the specified directory
        for frame in progress.track(frames_generator, total=total_frames, description='Vidiopy - Writing Image Sequence :smiley:', transient=True):
            save_frame(frame, frame_number)
            frame_number += 1
        print('[bold magenta]Vidiopy[/bold magenta] - Image Sequence Has Been Written:thumbs_up:.')
        return self

    def to_ImageClip(self, t):
        return Data2ImageClip(self.make_frame_pil(t))


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
        self.end = video_data['duration']
        self.duration = video_data['duration']

        # If audio is enabled, attach audio clip
        if audio:
            audio = AudioFileClip(filename)
            self.set_audio(audio)

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
        clip = []
        while t <= dur:
            frame = self.make_frame_pil(t)
            clip.append(f(*args, _do_not_pass=(frame, t, st, ed), **kwargs))
            t += td
        self.clip = np.array(clip)
        return self

    def fx(self, func: Callable, *args, **kwargs):
        # Apply an effect function directly to the clip
        func(*args, **kwargs)
        return self
    
    @override
    def make_frame_any(self, t):
        self.make_frame_pil(t)

    @override
    def make_frame_array(self, t):
        # Frame generation function returning numpy array
        frame_num = t * self.fps
        return np.array(self.clip[int(frame_num)])

    @override
    def make_frame_pil(self, t):
        # Frame generation function returning PIL Image
        frame_num = t * self.fps
        return self.clip[int(frame_num)]

    def _import_video_clip(self, file_name, ffmpeg_options):
        # Import video clip using ffmpeg
        options = {
            **(ffmpeg_options if ffmpeg_options else {})
        }
        return tuple(Image.fromarray(frame) for frame in ffmpegio.video.read(file_name, **options)[1])


class ImageClip(VideoClip):
    def __init__(self, image: str | Path | Image.Image | np.ndarray | None = None, fps: NumOrNone = None, duration: NumOrNone = None):
        super().__init__()

        # Import image if provided
        self.image = self._import_image(image) if image is not None else None

        # Set properties
        self.fps = fps
        self.start = 0.0
        self.duration = duration
        self.end = self.duration
        self.size = self.image.size if self.image is not None else (None, None) # type: ignore

    def _import_image(self, image):
        if isinstance(image, Image.Image):
            return image
        elif isinstance(image, np.ndarray):
            return Image.fromarray(image)
        elif isinstance(image, (str, Path, bytes)):
            return Image.open(image)
        return Image.open(image)

    def fl(self, f, *args, **kwargs):
        # Apply a function to the image and return the modified ImageClip
        self.image = f(*args, _do_not_pass=(self.image, None, self.start, self.end), **kwargs)
        return self

    def fx(self, func: Callable, *args, **kwargs):
        func(*args, **kwargs)
        return self

    @override
    def make_frame_any(self, t):
        return self.image

    @override
    def make_frame_array(self, t):
        return np.asarray(self.image)

    def make_frame_pil(self, t):
        return self.image

    def to_video_clip(self, fps=None, duration=None, start=0.0, end=None):
        """Convert `ImageClip` to `VideoClip`"""
        if fps is None:
            fps = self.fps
            if fps is None:
                raise ValueError("fps should be set of specify")
        if duration is None:
            duration = self.duration
            if duration is None:
                raise ValueError("You must specify 'duration'")
        if end is None:
            end = self.end if self.end else start + duration

        # Generate frames using iterate_frames_array_t
        frames = tuple(self.iterate_frames_array_t(fps))
        
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
        self.start = 0.0
        self.duration = (len(self.images)*(fps if fps is not None and fps else 0))
        self.set_end(self.duration)
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
        elif isinstance(images, (list, tuple)):
            # Return a tuple of Image objects created from the paths in the collection
            if isinstance(images[0], str):
                return tuple(Image.open(str(image)) for image in images)
            elif isinstance(images[0], Image.Image):
                return tuple(images)
            elif isinstance(images[0], np.ndarray):
                return tuple(Image.fromarray(img) for img in images)
        # Check if the input is a NumPy array
        elif isinstance(images, np.ndarray):
            # Return a tuple of Image objects created from the NumPy array
            return tuple(Image.fromarray(image) for image in images)
        else:
            # If the input is not of any expected type, raise a ValueError
            raise ValueError("Invalid input. Provide a directory path, a list/tuple/set of paths, or a NumPy array.")


    def fps(self, fps: Num):
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


    @requires_fps
    def make_frame_sub_cls(self, t):
        # Convert images to arrays if they are not already in array format
        self._image2array()

        # Calculate the frame index based on time and FPS
        frame_index = int(t * self.fps)
        # Return the generated frame
        return self.images[frame_index]

    def make_frame_pil_sub_cls(self, t):
        # Convert images to PIL format if they are not already in that format
        self._array2image()
        # Calculate the frame index based on time and FPS
        frame_index = int(t * self.fps)
        # Return the generated frame as a PIL Image
        return self.images[frame_index]

    @requires_duration
    def iterate_frames_array_t(self, fps: Num):
        self._image2array()
        frame_t_dif = (1 / fps)
        st_0 = self.start
        while st_0 < self.end:
            yield self.make_frame(st_0)
            st_0 += frame_t_dif

    @requires_duration
    def iterate_frames_pil_t(self, fps: Num):
        self._image2array()
        frame_t_dif = (1 / fps)
        st_0 = self.start
        while st_0 < self.end:
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

        bbox = font.getbbox(text)
        image_width, image_height = bbox[2] - bbox[0] + 20, bbox[3] - bbox[1] + 20
        image = Image.new("RGBA", (image_width, image_height), bg_color)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), text, font=font, align='center', fill=txt_color)

        super().__init__(image, fps=fps, duration=duration)


class CompositeVideoClip(ImageSequenceClip):
    
    def __init__(self, clips: list[VideoClip], use_bgclip: bool = True, audio: bool = True, bitrate: int | None = None):
        self.use_bgclip = use_bgclip
        if use_bgclip:
            self.bg_clip = clips[0]
            self.clips = clips[1:]
            self.size = self.bg_clip.size
        else:
            mw = 0
            mh = 0
            for clip in clips:
                if clip.size is not None:
                    if clip.size[0] > mw:
                        mw = clip.size[0]
                    if clip.size[1] > mh:
                        mh = clip.size[1]
            self.size = mw, mh # Tuple Do Not Need Brackets

            self.bg_clip = Data2ImageClip(Image.new('RGB', (mw, mh), (0, 0, 0)))
            self.clips = clips
        if audio:
            self.bitrate = bitrate
            self.audio = self._composite_audio()
        else:
            self.audio = None
        audio = self.audio
        super().__init__(*self._composite_video_clip())
        self.set_audio(audio)

    def _composite_video_clip(self):
        fps = 0
        for clip in self.clips:
            if clip.fps:
                if clip.fps > fps:
                    fps = clip.fps
        if not fps:
            raise

        if self.use_bgclip:
            duration = self.use_bgclip
            td = 1 / fps
            ed = self.bg_clip.end if self.bg_clip.end else (_ for _ in ()).throw(ValueError())
            t = self.bg_clip.start
            clip_frames = []
            while t <= ed:
                bg_frame:Image.Image = self.bg_clip.get_frame(t, is_pil = True)
                for clip in self.clips:
                    if clip.start <= t <= (clip.end if clip.end is not None else float('inf')):
                        frm: Image.Image = clip.get_frame(t, is_pil=True)
                        bg_frame.paste(frm, clip.pos(t),)
                    clip_frames.append(np.asarray(bg_frame))
                t += td
            return clip_frames, fps

        else:
            duration = 0.0
            ed = 0.0
            for c in self.clips:
                if c.duration:
                    if c.duration > duration:
                        duration = c.duration
                if c.end:
                    if c.end > ed:
                        ed = c.end
            if not duration:
                raise
            if not ed:
                raise

            td = 1 / fps
            t = self.bg_clip.start
            clip_frames = []
            while t <= ed:
                bg_frame:Image.Image = self.bg_clip.get_frame(t, is_pil = True)
                for clip in self.clips:
                    if clip.start <= t <= (clip.end if clip.end is not None else float('inf')):
                        frm: Image.Image = clip.get_frame(t, is_pil=True)
                        bg_frame.paste(frm, clip.pos(t),)
                    clip_frames.append(np.asarray(bg_frame))
            return clip_frames, fps


    def _composite_audio(self):
        """Concatenates the audio of all clips in the stack"""
        bg_audio = self.bg_clip.audio
        if not bg_audio:
            if not self.bitrate:
                bitrate = 0
                for clip in self.clips:
                    if clip.audio:
                        if clip.audio.bitrate > bitrate:
                            bitrate = clip.audio.bitrate
                self.bitrate = bitrate
            else:
                self.bitrate = self.bitrate

            bg_audio = AudioClip()
            if self.bg_clip.duration:
                bg_audio.clip = AudioSegment.silent(int(self.bg_clip.duration*1000), self.bitrate)
        else:
            if self.bg_clip.audio:
                self.bitrate = self.bg_clip.audio.bitrate
            else:
                raise ValueError("bg_clip audio is not set")

        audios = [bg_audio]
        for clip in self.clips:
            clip._sync_audio_video_s_e_d()
            if clip.audio:
                audios.append(clip.audio)
            else:
                if clip.duration:
                    audio = AudioClip()
                    audio.start = clip.start
                    audio.end = clip.end
                    audio.duration = clip.duration
                    audio.clip = AudioSegment.silent(int(clip.duration*1000), self.bitrate)
                    audios.append(audio)
                else:
                    raise ValueError("The duration of the clip is Not Set.")
        return CompositeAudioClip(audios, self.use_bgclip, self.bitrate)


if __name__ == '__main__':
    SystemExit()