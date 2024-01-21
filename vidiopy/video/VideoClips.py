from rich import print as rich_print
import rich.progress as progress
from fractions import Fraction
import os
import math
from copy import copy as copy_
from pathlib import Path
import subprocess
import tempfile
from typing import (Callable, TypeAlias, Generator,
                    override, Any, Self, Sequence)
from PIL import Image, ImageFont, ImageDraw
import ffmpegio
import numpy as np
from pydub import AudioSegment
from ..Clip import Clip
from ..audio.AudioClip import AudioFileClip, AudioClip, CompositeAudioClip
from ..decorators import *
from ..config import FFMPEG_BINARY, FFPROBE_BINARY

Num: TypeAlias = int | float
NumOrNone: TypeAlias = Num | None


class VideoClip(Clip):
    """
    Base class for all video clips.

    Attributes:
    - _st (float): Start time of the video clip.
    - _ed (float or None): End time of the video clip (can be None for indefinite duration).
    - _dur (float or None): Duration of the video clip (can be None for indefinite duration).
    - audio (AudioClip | None): Associated audio clip.
    - fps (float or None): Frames per second of the video clip.
    - size (tuple[int, int] | None): Size of the video clip (width, height).
    - pos (callable): Function defining the position of the video clip.
    - relative_pos (bool): Flag indicating whether the position is relative.

    Methods:
    - set_fps(fps: Num) -> self: Set the frames per second for the video clip.
    - set_audio(audio: AudioClip | None) -> self: Set the audio for the video clip.
    - set_position(pos, relative=False) -> self: Set the position for the video clip.
    - set_duration(dur: NumOrNone = None) -> self: Set the duration for the video clip.
    - set_start(t) -> self: Set the start time for the video clip.
    - set_end(t) -> self: Set the end time for the video clip.
    - without_audio() -> self: Remove audio from the video clip.
    - iterate_frames_array_t(fps: Num) -> Generator: Iterate over video frames as arrays.
    - iterate_frames_any_t(fps: Num) -> Generator: Iterate over video frames generically.
    - iterate_frames_pil_t(fps: Num) -> Generator[Image.Image, Any, None]: Iterate over video frames as PIL Images.
    - get_frame(t, is_pil=None) -> Union[array, Image.Image, Any]: Get a video frame at a specified time.
    - __copy__() -> VideoClip: Create a shallow copy of the video clip.
    - copy() -> VideoClip: Alias for __copy__ method.
    - width -> int: Get the width of the video clip.
    - height -> int: Get the height of the video clip.
    - aspect_ratio -> Fraction: Get the aspect ratio of the video clip.
    """

    def __init__(self) -> None:
        super().__init__()

        # Time-related properties
        self._st: Num = 0.0
        self._ed: NumOrNone = None
        self._dur: int | float | None = None

        # Video and audio properties
        self.audio: AudioClip | None = None
        self.fps: NumOrNone = None
        self.size: tuple[int, int] | None = None

        # Position-related properties
        self.pos = lambda t: (0, 0)
        self.relative_pos = False

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} start={self.start} end={self.end} fps={self.fps} size={self.size}, {id(self)}>'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} start={self.start} end={self.end} fps={self.fps} size={self.size}'

    def __len__(self):
        if self.end is None:
            return self.duration
        return int(self.end - self.start)

    def __iter__(self):
        return self.iterate_frames_array_t(self.fps)

    @property
    @requires_size
    def width(self):
        """
        Get the width of the video clip.

        Returns:
        - int: The width of the video clip.

        Raises:
        - ValueError: If the size is not set.
        """
        if self.size is not None:
            return self.size[0]
        else:
            raise ValueError("Size is not set")
    w = width

    @property
    @requires_size
    def height(self):
        """
        Get the height of the video clip.

        Returns:
        - int: The height of the video clip.

        Raises:
        - ValueError: If the size is not set.
        """
        if self.size is not None:
            return self.size[1]
        else:
            raise ValueError("Size is not set")
    h = height

    @property
    @requires_size
    def aspect_ratio(self):
        """
        Get the aspect ratio of the video clip.

        Returns:
        - Fraction: The aspect ratio of the video clip.

        Raises:
        - ValueError: If the size is not set.
        """
        if isinstance(self.w, int) and isinstance(self.w, int):
            return Fraction(self.w, self.h)
        else:
            raise ValueError("Size is not Valid")

    @property
    def start(self):
        """
        Get the start time of the current video clip.

        Returns:
        - float: The start time of the video clip.
        """
        return self._st

    @start.setter
    def start(self, t):
        """
        Set the start time for the current video clip.

        Parameters:
        - t (float): The new start time value.

        Returns:
        - self: The current video clip instance with the updated start time.

        Note:
        This method updates the start time and, if necessary, the end time and duration of the video clip. If the video clip has associated audio, it also updates the audio start, end, and duration attributes to match the new start time.

        Example:
        ```python
        v = VideoObject()
        v.start = 5.0  # Set the start time to 5 seconds
        ```
        """
        self._st = t

        if self.start is None:
            return self

        if self.duration is not None:
            self.end = t + self.duration
        elif self.end is not None:
            self.duration = self.end - self.start

        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
        return self

    def set_start(self, value: Num):
        self.start = value
        return self

    @property
    def end(self):
        """
        Get the end time of the current video clip.

        Returns:
        - float: The end time of the video clip.
        """
        return self._ed

    @end.setter
    def end(self, t):
        """
        Set the end time for the current video clip.

        Parameters:
        - t (float): The new end time value.

        Returns:
        - self: The current video clip instance with the updated end time.

        Note:
        This method updates the end time and duration of the video clip. If the video clip has associated audio, it also updates the audio start, end, and duration attributes to match the new end time.

        Example:
        ```python
        v = VideoObject()
        v.end = 20.0  # Set the end time to 20 seconds
        ```
        """
        self._ed = t
        self.duration = self.start + self._ed
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
        return self

    def set_end(self, value):
        self.end = value

    @property
    def duration(self):
        """
        Get the duration of the current video clip.

        Returns:
        - NumOrNone: The duration of the video clip.
        """
        return self._dur

    @duration.setter
    def duration(self, dur: Num):
        """Set the duration for the current video clip."""
        self._dur = dur

    def set_duration(self, value):
        self.duration = value

    def set_position(self, pos, relative=False):
        """
        Set the position for the current video clip.

        Parameters:
        - pos (callable | int | float): The position value. If a callable function, it is used directly; otherwise, a lambda function is created.
        - relative (bool, optional): If True, interprets the position as a relative value; if False (default), interprets it as an absolute value.

        Returns:
        - self: The current video clip instance with the updated position parameters.

        Note:
        This method sets the position for the video clip, allowing flexibility in defining the position either as a constant value or as a function of time. 
        The 'relative' parameter determines whether the position should be treated as a relative value.

        raises:
        - TypeError: If 'pos' is not callable, int, or float

        Example:
        ```python
        v = VideoObject()
        v.set_position(50)  # Set absolute position at 50
        v.set_position(lambda t: t * 10, relative=True)  # Set relative position as a function of time
        ```
        """
        self.relative_pos = relative

        if hasattr(pos, '__call__'):
            self.pos = pos
        elif isinstance(pos, (int, float)):
            self.pos = lambda t: pos
        else:
            raise TypeError('Pos is Invalid Type not Callable or int or float')

        return self

    def set_audio(self, audio: AudioClip | None):
        """
        Set the audio for the current video clip.

        Parameters:
        - audio (AudioClip | None): The audio clip to be associated with the video clip. 
        If None, removes any existing audio association.

        Returns:
        - self: The current video clip instance with the updated audio.
        """
        self.audio = audio
        if self.audio:
            self.audio.end = self.end
        return self

    def set_fps(self, fps: Num):
        """
        Set the frames per second (fps) for the current video clip.

        Parameters:
        - fps (float): The new frames per second value.

        Returns:
        - self: The current video clip instance with the updated frames per second.
        """
        self.fps = fps
        return self

    def without_audio(self):
        """
        Remove audio from the current video clip.

        Returns:
        - self: The current video clip instance with audio set to None.
        """
        self.audio = None
        return self

    def __copy__(self):
        """
        Create a shallow copy of the current video clip instance.

        Returns:
        - VideoObject: A new instance with the same attributes as the original, except for 'audio', which is shallow copied.
        """
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

    def make_frame_array(self, t) -> np.ndarray:
        raise NotImplemented('Make Frame is Not Set.')

    def make_frame_pil(self, t) -> Image.Image:
        raise NotImplemented('Make Frame pil is Not Set.')

    def make_frame_any(self, t) -> Image.Image | np.ndarray:
        raise NotImplemented('Make Frame any is Not Set.')

    def get_frame(self, t, is_pil=None):
        """
        Get a video frame at a specified time.

        Parameters:
        - t (float): Time in seconds for which to retrieve the frame.
        - is_pil (bool, optional): If True, returns the frame as a PIL Image; if False, returns the frame as an array. 
        If None (default), it uses the appropriate method based on the object's type.

        Returns:
        - Union[array, Image.Image, Any]: Video frame represented either as an array or a PIL Image.

        Note:
        This method retrieves a video frame at the specified time. The format of the returned frame can be specified using 
        the 'is_pil' parameter. If 'is_pil' is None, it uses the appropriate method based on the object's type.

        Example:
        ```python
        v = VideoObject()
        frame_array = v.get_frame(2.5, is_pil=False)
        frame_pil = v.get_frame(2.5, is_pil=True)
        frame_auto = v.get_frame(2.5)
        ```
        """
        if is_pil is None or is_pil is False:
            return self.make_frame_array(t)
        elif is_pil is True:
            return self.make_frame_pil(t)
        else:
            return self.make_frame_any(t)

    def iterate_frames_pil_t(self, fps: Num) -> Generator[Image.Image, Any, None]:
        """
        Iterate over video frames at a specified frames per second (fps) using PIL (Pillow) images.

        Parameters:
        - fps (float): Frames per second for the iteration.

        Yields:
        - Image.Image: PIL Image objects representing video frames.

        Raises:
        - ValueError: If the 'end' attribute is not set.

        Note:
        This method is a generator that iterates over video frames at the specified frames per second, yielding PIL Image 
        objects generated by the `make_frame_pil` method.

        Example:
        ```python
        v = VideoObject()
        for frame in v.iterate_frames_pil_t(30):
            # Process each frame as a PIL Image
            pass
        ```
        """
        time_dif = 1 / fps
        t = self.start
        if self.end is not None:
            while t <= self.end:
                yield self.make_frame_pil(t)
                t += time_dif
        else:
            raise ValueError('end Is None')

    @requires_end
    def iterate_frames_array_t(self, fps: Num):
        """
        Iterate over video frames at a specified frames per second (fps).

        Parameters:
        - fps (float): Frames per second for the iteration.

        Yields:
        - array: Video frames generated by the `make_frame_array` method.

        Note:
        This method requires the video to have an 'end' attribute set. It is a generator that iterates over video frames 
        at the specified frames per second, yielding the frames generated by the `make_frame_array` method.

        Example:
        ```python
        v = VideoObject()
        for frame in v.iterate_frames_array_t(30):
            # Process each frame
            pass
        ```
        """
        time_dif = 1 / fps
        t = 0
        while t <= self.end:  # type: ignore
            yield self.make_frame_array(t)
            t += time_dif

    @requires_end
    def iterate_frames_any_t(self, fps: Num):
        """
        Iterate over video frames at a specified frames per second (fps).

        Parameters:
        - fps (float): Frames per second for the iteration.

        Yields:
        - Any: Video frames generated by the `make_frame_array` method.

        Note:
        This method requires the video to have an 'end' attribute set. It is a generator that iterates over video frames 
        at the specified frames per second, yielding the frames generated by the `make_frame_array` method.

        Example:
        ```python
        v = VideoObject()
        for frame in v.iterate_frames_any_t(30):
            # Process each frame
            pass
        ```
        """
        time_dif = 1 / fps
        t = 0
        while t <= self.end:
            yield self.make_frame_array(t)
            t += time_dif

    def sub_fx(self) -> Self:
        raise NotImplementedError(
            "sub_fx method must be overridden in the subclass.")
        return self

    def fl_clip(self, func: Callable, *args, **kwargs) -> Self:
        """\
        Call The Function Like Follows
        >>> func(*args, **Kwargs, 
            _do_not_pass=dict{
                        'clip': clip: self, 
                        'frame': Frame: PIL.Image.Image,
                        'frame_time': Frame_time: Num,
                        'st': StartTime: NumOrNone,
                        'ed': EndTime: NumOrNone}
                        ))\
        """
        raise NotImplementedError(
            "fl method must be overridden in the subclass.")
        return self

    def fl_image(self, func, *args, **kwargs) -> Self:
        """\
        Transform each frame using a function.
        Call the function as Follows
        >>> func(Frame, *args, **kwargs)\
        """
        self.fl_frame_transform(func, *args, **kwargs)
        return self

    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """\
        Transform each frame using a function.
        Call the function as Follows
        >>> func(Frame, *args, **kwargs)\
        """
        raise NotImplementedError(
            'frame_transform method must be overridden in the subclass.')
        return self

    def fl_time_transform(self, func, *args, **kwargs) -> Self:
        """\
        Call the Function like below
        >>> func(clip: self, clip_frames: tuple[PIL.Image.Image], *args, **kwargs)\
        """
        raise NotImplementedError(
            "fl_time_transform method must be overridden in the subclass.")
        return self

    def fx(self, func, *args, **kwargs) -> Self:
        """
        Apply the specified function to the instance, modifying the state of the VideoClip.

        Parameters:
        - func (callable): The function to be applied to the instance.
        - *args: Positional arguments to be passed to the function.
        - **kwargs: Keyword arguments to be passed to the function.

        Returns:
        - YourClass: The modified instance of the class after applying the specified function.

        Notes:
        - This method allows the application of a custom function to the instance of the class.
        - The function is called with the instance itself as the first argument, followed by any additional positional
          and keyword arguments passed to this method.
        - The state of the VideoClip is modified in-place.
        - The modified instance is returned for potential further chaining of methods.

        Usage Example:
        >>> your_instance = YourClass()
        >>> your_instance = your_instance.fx(some_function, arg1, arg2, kwarg1=value1)  # Apply some_function to modify the instance.
        """
        self = func(self, *args, **kwargs)
        return self

    def _sync_audio_video_s_e_d(self):
        """
        Synchronize the audio start, end, and duration with the video's start, end, and duration.

        If audio is present, updates the audio start, end, and duration attributes to match the corresponding 
        attributes of the video object.

        Returns:
        - self: The current object instance.
        """
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
        return self

    def write_videofile(self, filename, fps=None, codec=None,
                        bitrate=None, audio=True, audio_fps=44100,
                        preset="medium", pixel_format=None,
                        audio_codec=None, audio_bitrate=None,
                        write_logfile=False, verbose=True,
                        threads=None, ffmpeg_params: dict[str, str] | None = None,
                        logger='bar', over_write_output=True):
        """
        Write a video file with optional audio.

        Parameters:
        - filename (str): The name of the output video file, including the extension.
        - fps (float, optional): Frames per second to determine the timing of the video. If not provided, 
        the function uses the object's properties or raises an Exception if neither fps nor object's properties are set.
        - codec (str, optional): The video codec to use.
        - bitrate (str, optional): The video bitrate.
        - audio (bool, optional): Whether to include audio in the output file. Defaults to True.
        - audio_fps (int, optional): Audio frames per second.
        - preset (str, optional): The video encoding preset.
        - pixel_format (str, optional): The video pixel format.
        - audio_codec (str, optional): The audio codec to use.
        - audio_bitrate (str, optional): The audio bitrate.
        - write_logfile (bool, optional): Whether to write a log file. Defaults to False.
        - verbose (bool, optional): Whether to print verbose information. Defaults to True.
        - threads (int, optional): The number of threads to use during encoding.
        - ffmpeg_params (dict[str, str], optional): Additional parameters to pass to ffmpeg.
        - logger (str, optional): The logger description to be used during progress tracking. Defaults to 'bar'.
        - over_write_output (bool, optional): Whether to overwrite the output file if it already exists. Defaults to True.

        Returns:
        - self: The current object instance.

        Raises:
        - Exception: If neither fps nor the object's properties (fps and duration) are set.

        Note:
        This function processes video frames using the `iterate_frames_array_t` method, writes a temporary video file using 
        ffmpegio, and combines it with audio (if specified) using ffmpeg. The final video file is saved with the provided filename.

        Example:
        ```python
        v = VideoObject()
        v.write_videofile('output.mp4', fps=30, codec='h264', bitrate='5000k', audio=True, audio_fps=44100)
        ```
        """
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
        rich_print(
            '[bold magenta]Vidiopy[/bold magenta] - Video Frames Has Been Processed :thumbs_up:.')
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
                pbar = progress_bar.add_task(
                    description='Writing Video File', total=total_frames, )

                def function_callback(status: dict, done: bool):
                    nonlocal current_frame
                    current_frame = status['frame'] - current_frame
                    progress_bar.update(
                        pbar, completed=current_frame, refresh=True)

                ffmpegio.video.write(
                    temp_video_file_name,
                    fps_to_use,
                    video_np,
                    overwrite=over_write_output,
                    progress=function_callback,
                    **ffmpeg_options
                )
                progress_bar.update(pbar, completed=True, visible=False)
            rich_print(
                '[bold magenta]Vidiopy[/bold magenta] - Video is Created :thumbs_up:')
            if self.audio and audio:
                self._sync_audio_video_s_e_d()
                temp_audio_file = tempfile.NamedTemporaryFile(
                    suffix=".wav", prefix=audio_name + "_temp_audio_", delete=False
                )
                audio_file_name = temp_audio_file.name
                temp_audio_file.close()

                # Write audio to the temporary file
                self.audio.write_audiofile(audio_file_name)

                # Combine video and audio using ffmpeg
                with progress.Progress(transient=True) as progress_bar:
                    sp = progress_bar.add_task(
                        "Combining Video & Audio", total=None)
                    result = subprocess.run(
                        f'{FFMPEG_BINARY} -i {temp_video_file_name} -i {
                            audio_file_name} -acodec copy '
                        f'{"-y" if over_write_output else ""} {filename}',
                        capture_output=True, text=True
                    )
                    progress_bar.update(sp, completed=True)
                rich_print(
                    "[bold magenta]Vidiopy[/bold magenta] - ✔ Audio Video Combined :thumbs_up:")
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
        """
        Write an image sequence to the specified directory.

        Parameters:
        - nformat (str): The format string for the image files, including the extension (e.g., '.png', '.jpg').
        - fps (float, optional): Frames per second to determine the timing of the image sequence. If not provided, 
        the function uses the object's properties or raises a ValueError if neither fps nor object's properties are set.
        - dir (str, optional): The directory where the image sequence will be saved. Defaults to the current directory.
        - logger (str, optional): The logger description to be used during the progress tracking. Defaults to 'bar'.

        Returns:
        - self: The current object instance.

        Raises:
        - ValueError: If neither fps nor the object's properties (fps and duration) are set.

        Note:
        This function uses the provided fps or the object's properties (if available) to determine the timing of the 
        image sequence. It creates the specified directory if it doesn't exist, iterates through frames, and saves 
        them with the appropriate file name in the specified directory.

        Example:
        ```python
        v = VideoObject()
        v.write_image_sequence('.png', fps=30, dir='output_frames', logger='progress_bar')
        ```
        """
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
            total_frames = (1 / self.fps) * \
                self.duration if self.duration else None
        else:
            # Print a warning if neither fps nor object's properties are set
            raise ValueError(
                "Warning: FPS is not provided, and fps and duration are not set.")

        # Iterate through frames and save them to the specified directory
        for frame in progress.track(frames_generator, total=total_frames, description='Vidiopy - Writing Image Sequence :smiley:', transient=True):
            save_frame(frame, frame_number)
            frame_number += 1
        rich_print(
            '[bold magenta]Vidiopy[/bold magenta] - Image Sequence Has Been Written:thumbs_up:.')
        return self

    def to_ImageClip(self, t):
        """
        Convert a frame of the video clip to an ImageClip.

        Parameters:
        - t (float): Time in seconds.

        Returns:
        - Data2ImageClip: An instance of Data2ImageClip created from the frame.

        Note:
        This method allows converting a specific frame of the VideoFileClip to an ImageClip using
        the make_frame_pil method. The resulting Data2ImageClip instance can be used for further
        processing or exporting as needed.

        Example Usage:
        ```python
        video_clip = VideoFileClip('video.mp4', audio=True)
        image_clip = video_clip.to_ImageClip(4.0)  # Converts frame at 4.0 seconds to ImageClip
        ```
        """
        return Data2ImageClip(self.make_frame_pil(t))


class VideoFileClip(VideoClip):
    """
    A class representing a video clip loaded from a video file.

    Attributes:
    - clip (tuple[Image.Image]): Tuple of frames representing the video clip.
    - fps (float): Frames per second of the video clip.
    - size (Tuple[int, int]): Size of the video frames (width, height).
    - start (float): Start time of the video clip in seconds (always 0.0).
    - end (float): End time of the video clip in seconds.
    - duration (float): Duration of the video clip in seconds.

    Methods:
    - __init__(self, filename, audio=True, ffmpeg_options=None):
        Initialize a VideoFileClip instance from a video file.
    - fl_frame_transform(self, func, *args, **kwargs) -> VideoFileClip:
        Apply a frame transformation function to each frame of the video clip.
    - fl_clip(self, func, *args, **kwargs) -> VideoFileClip:
        Apply a function to the entire video clip, generating a new clip.
    - fx(self, func: Callable, *args, **kwargs) -> VideoFileClip:
        Apply a generic function directly to the clip.
    - make_frame_any(self, t) -> Image.Image:
        Generate a frame for a given time.
    - make_frame_array(self, t) -> np.ndarray:
        Generate a frame array for a given time.
    - make_frame_pil(self, t) -> Image.Image:
        Generate a frame using PIL for a given time.

    Note:
    The VideoFileClip class extends the VideoClip class and is designed for loading video clips
    from video files. It uses ffmpeg to probe video streams, extract relevant information, and import
    the video clip frames. The class provides methods for frame transformations, applying functions,
    and generating frames in different formats.

    Example Usage:
    ```python
    video_clip = VideoFileClip('video.mp4', audio=True)
    transformed_clip = video_clip.fl_frame_transform(resize, width=640, height=480)
    final_video = transformed_clip.to_video_clip()
    ```
    """

    def __init__(self, filename, audio=True, ffmpeg_options=None):
        super().__init__()

        self.filename = filename

        # Probe video streams and extract relevant information
        video_data = ffmpegio.probe.video_streams_basic(filename)[0]

        # Import video clip using ffmpeg
        self.clip = self._import_video_clip(filename, ffmpeg_options)

        # Set video properties
        self.fps: float = float(video_data['frame_rate'])
        self.size = (video_data['width'], video_data['height'])
        self.start = 0.0
        self.end = video_data['duration']
        self.duration = float(self.end)
        # If audio is enabled, attach audio clip
        if audio:
            audio = AudioFileClip(filename)
            self.set_audio(audio)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} path={self.filename} start={self.start} end={self.end} fps={self.fps} size={self.size}, {id(self)}>'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} path={self.filename} start={self.start} end={self.end} fps={self.fps} size={self.size}'

    @override
    @requires_start_end
    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """
        Apply a frame transformation function to each frame of the video clip.

        Parameters:
        - func (Callable): The frame transformation function.
        - *args: Additional positional arguments for the function.
        - **kwargs: Additional keyword arguments for the function.

        Returns:
        - VideoFileClip: A new VideoFileClip instance with the transformed frames.

        Note: 
        - This method modifies the current VideoFileClip instance in-place by applying func to clip.
        - requires Clip Start and End

        Example Usage:
        ```python
        video_clip = VideoFileClip('video.mp4', audio=True)
        transformed_clip = video_clip.fl_frame_transform(resize, width=640, height=480)
        ```
        """
        clip: list[Image.Image] = []
        for frame in self.clip:
            frame: Image.Image = func(frame, *args, **kwargs)
            clip.append(frame)
        self.clip = tuple(clip)
        return self

    @override
    def fl_clip(self, func, *args, **kwargs):
        """
        Apply a function to the entire video clip, generating a new clip.

        Parameters:
        - func (Callable): The function to apply.
        - *args: Additional positional arguments for the function.
        - **kwargs: Additional keyword arguments for the function.

        Returns:
        - VideoFileClip: A new VideoFileClip instance generated by applying the function.

        Note: 
        - This method modifies the current VideoFileClip instance in-place by applying the function to the clip.

        Example Usage:
        ```python
        video_clip = VideoFileClip('video.mp4', audio=True)
        video_clip.fl_clip(some_function)
        ```
        """
        td = 1/self.fps
        start_t = self.start
        end_t = self.end
        frame_time = 0.0
        clip: list[Image.Image] = []
        for frame in self.clip:
            clip.append(func(*args, **kwargs, _do_not_pass={'clip': self,
                        'frame': frame, 'frame_time': frame_time, 'st': start_t, 'ed': end_t}))
            frame_time += td
        del self.clip
        self.clip = clip
        return self

    def fx(self, func: Callable, *args, **kwargs):
        # Apply an effect function directly to the clip
        self = func(self, *args, **kwargs)
        return self

    @override
    @requires_duration
    def make_frame_any(self, t):
        """
        Generate a frame for a given time.

        Parameters:
        - t (float): Time in seconds.
        Note:
        - Requires Duration: make_frame_pil Requires Duration else raise ValueError

        Raise:
        - ValueError: Raise ValueError if the Duration is Not Set.

        Returns:
        - Image.Image: The image data for the given time.

        Example Usage:
        ```python
        video_clip = VideoFileClip('video.mp4', audio=True)
        frame = video_clip.make_frame_any(2.5)  # Generates frame at 2.5 seconds
        ```
        """
        if self.duration is None:
            raise ValueError('Duration is Not Set.')
        time_per_frame = self.duration / len(self.clip)
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return self.make_frame_pil(frame_index)

    @override
    @requires_duration
    def make_frame_array(self, t):
        """
        Generate a frame array for a given time.

        Parameters:
        - t (float): Time in seconds.

        Returns:
        - np.ndarray: The image data as a NumPy array for the given time.

        Note:
        - Requires Duration: make_frame_pil Requires Duration else raise ValueError

        Raise:
        - ValueError: Raise ValueError if the Duration is Not Set.

        Example Usage:
        ```python
        video_clip = VideoFileClip('video.mp4', audio=True)
        frame_array = video_clip.make_frame_array(3.0)  # Generates frame array at 3.0 seconds
        ```
        """
        if self.duration is None:
            raise ValueError('Duration is Not Set.')
        time_per_frame = self.duration / len(self.clip)
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return np.array(self.clip[frame_index])

    @override
    @requires_duration
    def make_frame_pil(self, t):
        """
        Generate a frame using PIL for a given time.

        Parameters:
        - t (float): Time in seconds.

        Returns:
        - Image.Image: The image data for the given time.

        Note:
        - Requires Duration: make_frame_pil Requires Duration else raise ValueError

        Raise:
        - ValueError: Raise ValueError if the Duration is Not Set.

        Example Usage:
        ```python
        video_clip = VideoFileClip('video.mp4', audio=True)
        pil_frame = video_clip.make_frame_pil(4.0)  # Generates PIL image frame at 4.0 seconds
        ```
        """
        if self.duration is None:
            raise ValueError('Duration is Not Set.')
        time_per_frame = self.duration / len(self.clip)
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return self.clip[frame_index]

    def _import_video_clip(self, file_name, ffmpeg_options):
        """
        Import video clip using ffmpeg.

        Parameters:
        - file_name (str): The name of the video file.
        - ffmpeg_options (dict | None): Options to be passed to ffmpeg.

        Returns:
        - tuple[Image.Image]: Tuple of frames representing the video clip.

        Note: Internal method used for importing video clip frames.

        Example Usage:
        ```python
        clip_frames = self._import_video_clip('video.mp4', ffmpeg_options)
        ```
        """
        options = {
            **(ffmpeg_options if ffmpeg_options else {})
        }
        return tuple(Image.fromarray(frame) for frame in ffmpegio.video.read(file_name, **options)[1])


class ImageClip(VideoClip):
    """
    A class representing a video clip generated from a single image.

    Attributes:
    - image (Image.Image | None): The image data used in the ImageClip.
    - fps (NumOrNone): Frames per second of the video clip.
    - start (float): Start time of the video clip in seconds (always 0.0).
    - duration (NumOrNone): Duration of the video clip in seconds.
    - end (NumOrNone): End time of the video clip in seconds (equals duration).
    - size (Tuple[int, int] | None): Size of the image (width, height).

    Methods:
    - __init__(self, image: str | Path | Image.Image | np.ndarray | None = None, fps: NumOrNone = None, duration: NumOrNone = None):
        Initialize an ImageClip instance.
    - fl_frame_transform(self, func, *args, **kwargs) -> ImageClip:
        Apply a frame transformation function to the image.
    - fl_clip(self, func, *args, **kwargs) -> ImageClip:
        Raise a ValueError indicating that fl_clip is not applicable for ImageClip.
    - fx(self, func: Callable, *args, **kwargs) -> ImageClip:
        Apply a generic function to the ImageClip.
    - make_frame_any(self, t) -> Image.Image:
        Generate a frame for a given time.
    - make_frame_array(self, t) -> np.ndarray:
        Generate a frame array for a given time.
    - make_frame_pil(self, t) -> Image.Image:
        Generate a frame using PIL for a given time.

    Note:
    The ImageClip class extends the VideoClip class from the moviepy library and is designed
    for creating video clips from a single image. It provides methods for frame transformations,
    applying generic functions, and generating frames in different formats.

    Example Usage:
    ```python
    image_clip = ImageClip(image_path, fps=30, duration=5.0)
    transformed_clip = image_clip.fl_frame_transform(resize, width=640, height=480)
    final_video = transformed_clip.to_video_clip()
    ```
    """

    def __init__(self, image: str | Path | Image.Image | np.ndarray | None = None, fps: NumOrNone = None, duration: NumOrNone = None):
        """
        Initialize an ImageClip instance.

        Parameters:
        - image (str | Path | Image.Image | np.ndarray | None, optional):
            Input image path or image data. Defaults to None.
        - fps (NumOrNone, optional): Frames per second of the video clip. Defaults to None.
        - duration (NumOrNone, optional): Duration of the video clip in seconds. Defaults to None.

        Note: If image is provided, it will be imported and used as the source for the ImageClip.
              If not provided, the ImageClip will be initialized with default values.

        Attributes:
        - image (Image.Image | None): The image data used in the ImageClip.
        - fps (NumOrNone): Frames per second of the video clip.
        - start (float): Start time of the video clip in seconds (always 0.0).
        - duration (NumOrNone): Duration of the video clip in seconds.
        - end (NumOrNone): End time of the video clip in seconds (equals duration).
        - size (Tuple[int, int] | None): Size of the image (width, height).

        Returns:
        - None
        """
        super().__init__()
        if isinstance(self.image, (str, Path)):
            self.imagepath = self.image
        else:
            self.imagepath = None
        # Import image if provided
        self.image = self._import_image(image) if image is not None else None

        # Set properties
        self.fps = fps
        self.start = 0.0
        if duration is not None:
            self.duration = duration
        self.end = self.duration
        self.size = self.image.size if self.image is not None else (
            None, None)  # type: ignore

    def _import_image(self, image):
        """
        Import the image from various sources.

        Parameters:
        - image (str | Path | Image.Image | np.ndarray): Input image data.

        Returns:
        - Image.Image: The imported image data.
        """
        if isinstance(image, Image.Image):
            return image
        elif isinstance(image, np.ndarray):
            return Image.fromarray(image)
        elif isinstance(image, (str, Path, bytes)):
            return Image.open(image)
        return Image.open(image)

    def __repr__(self):
        return f'<{self.__class__.__name__} image path={self.imagepath} start={self.start} end={self.end} fps={self.fps} size={self.size}, {id(self)}>'

    def __str__(self):
        return f'{self.__class__.__name__} image path={self.imagepath} start={self.start} end={self.end} fps={self.fps} size={self.size}'

    @override
    @requires_start_end
    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """
        Apply a frame transformation function to the image.

        Parameters:
        - func (Callable): The frame transformation function.
        - *args: Additional positional arguments for the function.
        - **kwargs: Additional keyword arguments for the function.

        Returns:
        - ImageClip: A new ImageClip instance with the transformed image.

        Note: This method modifies the current ImageClip instance in-place.

        Example Usage:
        ```python
        image_clip = ImageClip(image_path, fps=30, duration=5.0)
        transformed_clip = image_clip.fl_frame_transform(resize, width=640, height=480)
        ```
        """
        self.image = func(self.image, *args, **kwargs)
        return self

    @override
    def fl_clip(self, func, *args, **kwargs) -> Self:
        """
        Raise a ValueError indicating that fl_clip is not applicable for ImageClip.

        Parameters:
        - func: Unused.
        - *args: Unused.
        - **kwargs: Unused.

        Returns:
        - ImageClip: The current ImageClip instance.

        Raises:
        - ValueError: This method is not applicable for ImageClip.

        Example Usage:
        ```python
        image_clip = ImageClip(image_path, fps=30, duration=5.0)
        image_clip.fl_clip(some_function)  # Raises ValueError
        ```
        """
        raise ValueError(
            "Convert this Image Clip to Video Clip following is the function `to_video_clip`")
        return self

    def fx(self, func: Callable, *args, **kwargs):
        """
        Apply a generic function to the ImageClip.

        Parameters:
        - func (Callable): The function to apply.
        - *args: Additional positional arguments for the function.
        - **kwargs: Additional keyword arguments for the function.

        Returns:
        - ImageClip: The current ImageClip instance.

        Note: This method modifies the current ImageClip instance in-place.

        Example Usage:
        ```python
        def custom_function(image):
            # Some custom processing on the image
            return modified_image

        image_clip = ImageClip(image_path, fps=30, duration=5.0)
        image_clip.fx(custom_function, some_arg=42)
        ```
        """
        func(*args, **kwargs)
        return self

    @override
    def make_frame_any(self, t):
        """
        Generate a frame for a given time.

        Parameters:
        - t (float): Time in seconds.

        Returns:
        - Image.Image: The image data for the given time.

        Example Usage:
        ```python
        image_clip = ImageClip(image_path, fps=30, duration=5.0)
        frame = image_clip.make_frame_any(2.5)  # Generates frame at 2.5 seconds
        ```
        """
        return self.image

    @override
    def make_frame_array(self, t):
        """
        Generate a frame array for a given time.

        Parameters:
        - t (float): Time in seconds.

        Returns:
        - np.ndarray: The image data as a NumPy array for the given time.

        Example Usage:
        ```python
        image_clip = ImageClip(image_path, fps=30, duration=5.0)
        frame_array = image_clip.make_frame_array(3.0)  # Generates frame array at 3.0 seconds
        ```
        """
        return np.asarray(self.image)

    def make_frame_pil(self, t):
        """
        Generate a frame using PIL for a given time.

        Parameters:
        - t (float): Time in seconds.

        Returns:
        - Image.Image: The image data for the given time.

        Example Usage:
        ```python
        image_clip = ImageClip(image_path, fps=30, duration=5.0)
        pil_frame = image_clip.make_frame_pil(4.0)  # Generates PIL image frame at 4.0 seconds
        ```
        """
        return self.image

    def to_video_clip(self, fps=None, duration=None, start=0.0, end=None):
        """
        Convert `ImageClip` to `VideoClip`

        If fps or duration is not provided, it defaults to the corresponding attribute
        of the ImageClip instance. If those attributes are not available, a ValueError is raised.

        Parameters:
        - fps (float, optional): Frames per second of the resulting video clip.
            If not provided, it defaults to the fps attribute of the ImageClip instance.
            If that is also not available, a ValueError is raised.
        - duration (float, optional): Duration of the resulting video clip in seconds.
            If not provided, it defaults to the duration attribute of the ImageClip instance.
            If that is also not available, a ValueError is raised.
        - start (float, optional): Start time of the resulting video clip in seconds. Default is 0.0.
        - end (float, optional): End time of the resulting video clip in seconds.
            If not provided, it defaults to the end attribute of the ImageClip instance,
            or if that is not available, it is calculated based on start and duration.

        Returns:
        - ImageSequenceClip: A VideoClip subclass instance generated from the ImageClip frames.

        Raises:
        - ValueError: If fps or duration is not provided and the corresponding attribute is not available.

        Note:
        The `to_video_clip` method returns an instance of the `ImageSequenceClip` class,
        which is a subclass of the `VideoClip` Class.

        Example Usage:
        ```python
        # Example Usage
        image_clip = ImageClip()
        video_clip = image_clip.to_video_clip(fps=24, duration=10.0, start=2.0, end=12.0)
        ```
        """
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
    """
    A class representing a video clip generated from raw data (numpy array or PIL Image).

    Parameters:
    - data (np.ndarray or PIL Image): The raw data to be converted into a video clip.
    - fps (int or float, optional): Frames per second of the video. If not provided, it will be inherited
      from the parent class (ImageClip) or set to the default value.
    - duration (int or float, optional): Duration of the video in seconds. If not provided, it will be
      inherited from the parent class (ImageClip) or set to the default value.

    Attributes:
    - image (PIL Image): The PIL Image representation of the provided data.
    - size (tuple): The size (width, height) of the image.

    Methods:
    - _import_image(image): Private method to convert the provided data (numpy array or PIL Image)
      into a PIL Image.

    Example:
    ```
    # Import necessary libraries

    # Create a Data2ImageClip instance from a numpy array
    data_array = np.random.randint(0, 255, size=(480, 640, 3), dtype=np.uint8)
    video_clip = Data2ImageClip(data=data_array, fps=30, duration=5)

    # Create a Data2ImageClip instance from a PIL Image
    from PIL import Image
    data_image = Image.new('RGB', (640, 480), color='red')
    video_clip = Data2ImageClip(data=data_image, fps=24, duration=10)
    ```

    Note:
    The `Data2ImageClip` class extends the `ImageClip`. It allows
    users to create video clips from raw data, supporting either numpy arrays or PIL Images as input.
    """

    def __init__(self, data: np.ndarray | Image.Image, fps: NumOrNone = None, duration: NumOrNone = None):
        # Initialize the class by calling the parent constructor
        super().__init__(fps=fps, duration=duration)

        # Import the image from the provided data
        self.image = self._import_image(data)

        # Set the size attribute based on the image size
        self.size = self.image.size

    def _import_image(self, image):
        """
        Private method to convert the provided data (numpy array or PIL Image) into a PIL Image.

        Parameters:
        - image (np.ndarray or PIL Image): The raw data to be converted.

        Returns:
        - PIL Image: The PIL Image representation of the provided data.

        Raises:
        - TypeError: If the input type is not supported (neither numpy array nor PIL Image).
        """
        # Convert the provided data (numpy array or PIL Image) into a PIL Image
        if isinstance(image, np.ndarray):
            return Image.fromarray(image)
        elif isinstance(image, Image.Image):
            return image
        else:
            # Raise an error if the input type is not supported
            raise TypeError(
                f"{type(image)} is not an Image.Image or numpy array Type.")


class ImageSequenceClip(VideoClip):
    """
    A class for creating a video clip from a sequence of images.

    Parameters:
    - images: A sequence of images, where each element can be of type str: ImagePath, Path: ImagePath, PIL.Image.Image, numpy.ndarray,
              or a NumPy array representing frames.
    - fps (Optional): Frames per second of the resulting video clip.
    - duration (Optional): Duration of the resulting video clip in seconds.

    Attributes:
    - clip: A tuple of frames representing the video clip.
    - fps: Frames per second of the video clip.
    - duration: Duration of the video clip in seconds.

    Notes:
    - If both fps and duration are provided, fps takes precedence.
    - If only fps is provided, the duration is calculated based on the number of frames and fps.
    - If only duration is provided, fps is calculated based on the number of frames and duration.
    - If neither fps nor duration is provided, the clip is imported with no specified fps or duration.

    Usage Example:
    >>> image_paths = ['frame1.jpg', 'frame2.jpg', 'frame3.jpg']
    >>> video_clip = ImageSequenceClip(image_paths, fps=24)
    # Create a video clip from a sequence of images with a specified fps.
    """

    def __init__(self, images: Sequence[str | Path | Image.Image | np.ndarray] | np.ndarray, fps: NumOrNone = None, duration: NumOrNone = None):
        super().__init__()
        if fps and duration:
            self.clip = self._import_images(images)
            self.fps = fps
            self.duration = duration
        elif fps:
            self.clip = self._import_images(images)
            self.fps = fps
            if fps:
                self.end = len(self.clip)/fps
                self.duration = self.end
        elif duration:
            self.clip = self._import_images(images)
            self.fps = len(self.clip) / float(duration)
            self.end = duration
            self.duration = duration
        else:
            self.clip = self._import_images(images)

    def _import_images(self, images):
        """
        Import images into the image sequence clip.

        Parameters:
        - images: A list of images, where each element can be of type PIL.Image.Image, numpy.ndarray, str: ImagePath, Path: ImagePath,
                  or an object with a 'read' method returning bytes.

        Returns:
        - tuple: A tuple of imported frames in the form of PIL.Image.Image.

        Notes:
        - This method is used to import frames into the image sequence clip.
        - The method supports multiple formats for the input images: PIL Image, NumPy array, file paths (str or Path),
          or an object with a 'read' method returning bytes.
        - If the input is a NumPy array, it is converted to a PIL Image using Image.fromarray().
        - If the input is a file path, the image is opened using Image.open().
        - If the input is an object with a 'read' method returning bytes, the bytes are treated as an image and added to the clip.
        - The resulting frames are returned as a tuple.

        Usage Example:
        >>> your_instance = ImageSequenceClip()
        >>> image_paths = ['frame1.jpg', 'frame2.jpg', 'frame3.jpg']
        >>> imported_frames = your_instance._import_images(image_paths)
        # Import frames from image paths into the image sequence clip.
        """
        frames = []
        if isinstance(images[0], (Image.Image)):
            for frame in images:
                frames.append(frame)
        elif isinstance(images[0], (np.ndarray)):
            for frame in images:
                frames.append(Image.fromarray(frame))
        elif isinstance(images[0], (str, Path)):
            for frame in images:
                frames.append(Image.open(frame))
        elif isinstance(images, np.ndarray):
            for frame in images:
                frames.append(Image.fromarray(frame))
        elif hasattr(images[0], 'read') and callable(getattr(images[0], 'read')) and 'b' in getattr(images[0], 'mode', ''):
            for frame in images:
                frames.append(frame)
        return tuple(frames)

    @override
    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """
        Apply a frame transformation function to each frame in the image sequence, modifying the clip in-place.

        Parameters:
        - func (callable): The function to be applied to each frame.
        - *args: Positional arguments to be passed to the function.
        - **kwargs: Keyword arguments to be passed to the function.

        Returns:
        - ImageSequenceClip: The modified instance of the class after applying the frame transformation function.

        Notes:
        - This method allows the application of a custom frame transformation function to each frame in the image sequence.
        - The function is called for each frame and is expected to return a modified frame in the form of a Pillow Image.
        - The modified frames are then stored in the instance's 'clip' attribute.
        - The modified instance is returned for potential further chaining of methods.

        Usage Example:
        >>> your_instance = ImageSequenceClip()
        >>> your_instance = your_instance.fl_frame_transform(some_function, arg1, arg2, kwarg1=value1)
        # Apply some_function to each frame in the image sequence to modify the instance.
        """
        clip: list[Image.Image] = []
        for frame in self.clip:
            frame: Image.Image = func(frame, *args, **kwargs)
            frame.show("temp")
            breakpoint()
            clip.append(frame)
        del self.clip
        self.clip = tuple(clip)
        return self

    @override
    def fl_clip(self, func, *args, **kwargs):
        """
        Apply a function to each frame in the video clip, modifying the clip in-place.

        Parameters:
        - func (callable): The function to be applied to each frame.
        - *args: Positional arguments to be passed to the function.
        - **kwargs: Keyword arguments to be passed to the function.

        Returns:
        - ImageSequenceClip: The modified instance of the class after applying the function to each frame.

        Raises:
        - ValueError: If both 'fps' and 'duration' are not set.

        Notes:
        - This method allows the application of a custom function to each frame in the video clip.
        - The function is called for each frame and is expected to return a modified frame in the form of a Pillow Image.
        - The modified frames are then stored in the instance's 'clip' attribute.
        - The 'fps' or 'duration' of the clip is used to determine the time duration between frames.
        - The modified instance is returned for potential further chaining of methods.

        Usage Example:
        >>> your_instance = ImageSequenceClip()
        >>> your_instance = your_instance.fl_clip(some_function, arg1, arg2, kwarg1=value1)
        # Apply some_function to each frame in the clip to modify the instance.
        """
        td = 1/self.fps if self.fps \
            else self.duration/len(self.clip) if self.duration \
            else (_ for _ in ()).throw(ValueError("Duration or Fps Should Be Set."))
        start_t = self.start
        end_t = self.end
        frame_time = 0.0
        clip: list[Image.Image] = []
        for frame in self.clip:
            clip.append(func(*args, **kwargs, _do_not_pass=(self,
                        frame, frame_time, start_t, end_t)))
            frame_time += td
        self.clip = tuple(clip)
        return self

    @override
    def fx(self, func: Callable, *args, **kwargs):
        func(*args, **kwargs)
        return self

    @override
    def make_frame_any(self, t):
        """
        Generate a frame at the specified time 't' in the video clip, returning either a PIL Image or a NumPy array.

        Parameters:
        - t (float): The time (in seconds) at which to generate the frame.

        Returns:
        - Union[PIL.Image.Image, numpy.ndarray]: The generated frame as either a PIL Image or a NumPy array.

        Raises:
        - ValueError: If both 'make_frame_pil' and 'make_frame_array' methods fail to generate a frame.

        Notes:
        - This method attempts to generate a frame using 'make_frame_pil' and 'make_frame_array' methods.
        - It first tries to generate a frame as a PIL Image using the 'make_frame_pil' method.
        - If that fails, it then attempts to generate a frame as a NumPy array using the 'make_frame_array' method.
        - If both attempts fail, a ValueError is raised.

        Usage Example:
        >>> your_instance = ImageSequenceClip()
        >>> frame_at_t = your_instance.make_frame_any(5.0)  # Get the frame at 5 seconds as either PIL Image or NumPy array.
        """
        return self.make_frame_pil(t) or self.make_frame_array(t) or (_ for _ in ()).throw(ValueError(""))

    @override
    def make_frame_array(self, t):
        """
        Generate a NumPy array representing the frame at the specified time 't' in the video clip.

        Parameters:
        - t (float): The time (in seconds) at which to generate the frame.

        Returns:
        - numpy.ndarray: The generated NumPy array representing the frame at time 't'.

        Raises:
        - ValueError: If either 'duration' or 'fps' is not set, as one of them must be specified to calculate time_per_frame.

        Notes:
        - This method calculates the frame to be generated based on the specified time 't' and the properties of the video clip.
        - If 'duration' is set, it calculates 'time_per_frame' based on the total duration and the number of frames in the clip.
        - If 'fps' is set (and 'duration' is not), it calculates 'time_per_frame' using the frames per second.
        - If neither 'duration' nor 'fps' is set, a ValueError is raised.
        - The frame at the calculated index is then converted to a NumPy array using np.array().

        Usage Example:
        >>> your_instance = ImageSequenceClip()
        >>> frame_at_t_array = your_instance.make_frame_array(5.0)  # Get the frame at 5 seconds as a NumPy array.
        """
        time_per_frame = self.duration / len(self.clip) if self.duration else 1/self.fps if self.fps else (
            _ for _ in ()).throw(ValueError("Duration or FPS should be set"))
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return np.array(self.clip[int(frame_index)])

    @override
    def make_frame_pil(self, t):
        """
        Generate a PIL Image representing the frame at the specified time 't' in the video clip.

        Parameters:
        - t (float): The time (in seconds) at which to generate the frame.

        Returns:
        - PIL.Image.Image: The generated PIL Image representing the frame at time 't'.

        Raises:
        - ValueError: If either 'duration' or 'fps' is not set, as one of them must be specified to calculate time_per_frame.

        Notes:
        - This method calculates the frame to be generated based on the specified time 't' and the properties of the video clip.
        - If 'duration' is set, it calculates 'time_per_frame' based on the total duration and the number of frames in the clip.
        - If 'fps' is set (and 'duration' is not), it calculates 'time_per_frame' using the frames per second.
        - If neither 'duration' nor 'fps' is set, a ValueError is raised.
        - The frame at the calculated index is then retrieved from the video clip ('self.clip').

        Usage Example:
        >>> your_instance = ImageSequenceClip()
        >>> frame_at_t = your_instance.make_frame_pil(5.0)  # Get the frame at 5 seconds as Pillow image.
        """
        time_per_frame = self.duration / len(self.clip) if self.duration else 1/self.fps if self.fps else (
            _ for _ in ()).throw(ValueError("Duration or FPS should be set"))
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return self.clip[int(frame_index)]


class ColorClip(Data2ImageClip):
    """
    A video clip class with a solid color.

    Parameters:
    - color: str or tuple[int, ...]
        Color of the image. It can be a color name (e.g., 'red', 'blue') or RGB tuple.
    - mode: str
        Mode to use for the image. Default is 'RGBA'.
    - size: tuple
        Size of the image in pixels (width, height). Default is (1, 1) for changing size after wards.
    - fps: float, optional
        Frames per second for the video clip.
    - duration: float, optional
        Duration of the video clip in seconds.

    Examples:
    1. Create a red square video clip (500x500, 30 FPS, 5 seconds):
    ```python
    red_square = ColorClip(color='red', size=(500, 500), fps=30, duration=5)
    ```

    2. Create a blue fullscreen video clip (1920x1080, default FPS and duration):
    ```python
    blue_fullscreen = ColorClip(color='blue', size=(1920, 1080))
    ```

    3. Create a green transparent video clip (RGBA mode, 800x600):
    ```python
    green_transparent = ColorClip(color=(0, 255, 0, 0), mode='RGBA', size=(800, 600))
    ```
    Accepted Color string:
    ```
    {   "aliceblue": "#f0f8ff",
        "antiquewhite": "#faebd7",
        "aqua": "#00ffff",
        "aquamarine": "#7fffd4",
        "azure": "#f0ffff",
        "beige": "#f5f5dc",
        "bisque": "#ffe4c4",
        "black": "#000000",
        "blanchedalmond": "#ffebcd",
        "blue": "#0000ff",
        "blueviolet": "#8a2be2",
        "brown": "#a52a2a",
        "burlywood": "#deb887",
        "cadetblue": "#5f9ea0",
        "chartreuse": "#7fff00",
        "chocolate": "#d2691e",
        "coral": "#ff7f50",
        "cornflowerblue": "#6495ed",
        "cornsilk": "#fff8dc",
        "crimson": "#dc143c",
        "cyan": "#00ffff",
        "darkblue": "#00008b",
        "darkcyan": "#008b8b",
        "darkgoldenrod": "#b8860b",
        "darkgray": "#a9a9a9",
        "darkgrey": "#a9a9a9",
        "darkgreen": "#006400",
        "darkkhaki": "#bdb76b",
        "darkmagenta": "#8b008b",
        "darkolivegreen": "#556b2f",
        "darkorange": "#ff8c00",
        "darkorchid": "#9932cc",
        "darkred": "#8b0000",
        "darksalmon": "#e9967a",
        "darkseagreen": "#8fbc8f",
        "darkslateblue": "#483d8b",
        "darkslategray": "#2f4f4f",
        "darkslategrey": "#2f4f4f",
        "darkturquoise": "#00ced1",
        "darkviolet": "#9400d3",
        "deeppink": "#ff1493",
        "deepskyblue": "#00bfff",
        "dimgray": "#696969",
        "dimgrey": "#696969",
        "dodgerblue": "#1e90ff",
        "firebrick": "#b22222",
        "floralwhite": "#fffaf0",
        "forestgreen": "#228b22",
        "fuchsia": "#ff00ff",
        "gainsboro": "#dcdcdc",
        "ghostwhite": "#f8f8ff",
        "gold": "#ffd700",
        "goldenrod": "#daa520",
        "gray": "#808080",
        "grey": "#808080",
        "green": "#008000",
        "greenyellow": "#adff2f",
        "honeydew": "#f0fff0",
        "hotpink": "#ff69b4",
        "indianred": "#cd5c5c",
        "indigo": "#4b0082",
        "ivory": "#fffff0",
        "khaki": "#f0e68c",
        "lavender": "#e6e6fa",
        "lavenderblush": "#fff0f5",
        "lawngreen": "#7cfc00",
        "lemonchiffon": "#fffacd",
        "lightblue": "#add8e6",
        "lightcoral": "#f08080",
        "lightcyan": "#e0ffff",
        "lightgoldenrodyellow": "#fafad2",
        "lightgreen": "#90ee90",
        "lightgray": "#d3d3d3",
        "lightgrey": "#d3d3d3",
        "lightpink": "#ffb6c1",
        "lightsalmon": "#ffa07a",
        "lightseagreen": "#20b2aa",
        "lightskyblue": "#87cefa",
        "lightslategray": "#778899",
        "lightslategrey": "#778899",
        "lightsteelblue": "#b0c4de",
        "lightyellow": "#ffffe0",
        "lime": "#00ff00",
        "limegreen": "#32cd32",
        "linen": "#faf0e6",
        "magenta": "#ff00ff",
        "maroon": "#800000",
        "mediumaquamarine": "#66cdaa",
        "mediumblue": "#0000cd",
        "mediumorchid": "#ba55d3",
        "mediumpurple": "#9370db",
        "mediumseagreen": "#3cb371",
        "mediumslateblue": "#7b68ee",
        "mediumspringgreen": "#00fa9a",
        "mediumturquoise": "#48d1cc",
        "mediumvioletred": "#c71585",
        "midnightblue": "#191970",
        "mintcream": "#f5fffa",
        "mistyrose": "#ffe4e1",
        "moccasin": "#ffe4b5",
        "navajowhite": "#ffdead",
        "navy": "#000080",
        "oldlace": "#fdf5e6",
        "olive": "#808000",
        "olivedrab": "#6b8e23",
        "orange": "#ffa500",
        "orangered": "#ff4500",
        "orchid": "#da70d6",
        "palegoldenrod": "#eee8aa",
        "palegreen": "#98fb98",
        "paleturquoise": "#afeeee",
        "palevioletred": "#db7093",
        "papayawhip": "#ffefd5",
        "peachpuff": "#ffdab9",
        "peru": "#cd853f",
        "pink": "#ffc0cb",
        "plum": "#dda0dd",
        "powderblue": "#b0e0e6",
        "purple": "#800080",
        "rebeccapurple": "#663399",
        "red": "#ff0000",
        "rosybrown": "#bc8f8f",
        "royalblue": "#4169e1",
        "saddlebrown": "#8b4513",
        "salmon": "#fa8072",
        "sandybrown": "#f4a460",
        "seagreen": "#2e8b57",
        "seashell": "#fff5ee",
        "sienna": "#a0522d",
        "silver": "#c0c0c0",
        "skyblue": "#87ceeb",
        "slateblue": "#6a5acd",
        "slategray": "#708090",
        "slategrey": "#708090",
        "snow": "#fffafa",
        "springgreen": "#00ff7f",
        "steelblue": "#4682b4",
        "tan": "#d2b48c",
        "teal": "#008080",
        "thistle": "#d8bfd8",
        "tomato": "#ff6347",
        "turquoise": "#40e0d0",
        "violet": "#ee82ee",
        "wheat": "#f5deb3",
        "white": "#ffffff",
        "whitesmoke": "#f5f5f5",
        "yellow": "#ffff00",
        "yellowgreen": "#9acd32",
    }
    ```
    """

    def __init__(self, color: str | tuple[int, ...], mode='RGBA', size=(1, 1), fps=None, duration=None):
        data = Image.new(mode, size, color)  # type: ignore
        self.color = color
        self.mode = mode
        super().__init__(data, fps=fps, duration=duration)

    def __repr__(self):
        return f'<{self.__class__.__name__} color={self.color} mode={self.mode} start={self.start} end={self.end} fps={self.fps} size={self.size}, {id(self)}>'

    def set_size(self, size: tuple[int, int]):
        """
        Set the size of the video clip.

        Parameters:
        - size: tuple[int, int]
            New size of the video clip in pixels (width, height).

        Examples:
        1. Resize the video clip to 800x600:
        ```python
        color_clip.set_size((800, 600))
        ```
        """
        self.size = size
        self.image = self.image.resize(size)


class TextClip(Data2ImageClip):
    """
    A class representing a text clip to be used in video compositions.

    Parameters:
    - text (str): The text content to be displayed in the clip.
    - font_pth (None | str, optional): The file path to the TrueType font file (.ttf). If None, the default system font is used. Defaults to None.
    - font_size (int, optional): The font size for the text. Defaults to 20.
    - txt_color (str | tuple[int, ...], optional): The color of the text specified as either a string (e.g., 'white') or a tuple representing RGBA values. Defaults to (255, 255, 255, 0) (fully transparent white).
    - bg_color (str | tuple[int, ...], optional): The background color of the text clip, specified as either a string (e.g., 'black') or a tuple representing RGBA values. Defaults to (0, 0, 0, 0) (fully transparent black).
    - fps (float, optional): Frames per second of the video. If None, the value is inherited from the parent class. Defaults to None.
    - duration (float, optional): Duration of the video clip in seconds. If None, the value is inherited from the parent class. Defaults to None.

    Attributes:
    - font (PIL.ImageFont.FreeTypeFont): The font object used for rendering the text.
    - image (PIL.Image.Image): The image containing the rendered text.
    - fps (float): Frames per second of the video clip.
    - duration (float): Duration of the video clip in seconds.

    Example:
    ```python
    # Create a TextClip with custom text and styling
    text_clip = TextClip("Contribute to Vidiopy", font_size=30, txt_color='red', bg_color='blue', fps=24, duration=5.0)

    # Use the text clip in a video composition
    composition = CompositeVideoClip([other_clip, text_clip])
    composition.write_videofile("output.mp4", codec='libx264', fps=24)
    ```
    """

    def __init__(self, text: str, font_pth: None | str = None, font_size: int = 20, txt_color: str | tuple[int, ...] = (255, 255, 255, 0),
                 bg_color: str | tuple[int, ...] = (0, 0, 0, 0), fps=None, duration=None):
        font = ImageFont.truetype(
            font_pth, font_size) if font_pth else ImageFont.load_default(font_size)

        bbox = font.getbbox(text)
        image_width, image_height = bbox[2] - \
            bbox[0] + 20, bbox[3] - bbox[1] + 20
        image = Image.new("RGBA", (image_width, image_height),
                          bg_color)  # type: ignore
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), text, font=font, align='center',
                  fill=txt_color)  # type: ignore

        self.text = text
        self.font = font
        self.font_size = font_size
        self.txt_color = txt_color
        self.bg_color = bg_color

        super().__init__(image, fps=fps, duration=duration)

    def __repr__(self):
        return f'<{self.__class__.__name__} font={self.font} font_size={self.font_size} txt_color={self.txt_color} bg_color={self.bg_color} start={self.start} end={self.end} fps={self.fps} size={self.size} text={self.text}, {id(self)}>'

    def __str__(self):
        return f'{self.__class__.__name__} font={self.font} font_size={self.font_size} txt_color={self.txt_color} bg_color={self.bg_color} start={self.start} end={self.end} fps={self.fps} size={self.size} text={self.text}'


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
            self.size = mw, mh  # Tuple Do Not Need Brackets

            self.bg_clip = Data2ImageClip(
                Image.new('RGB', (mw, mh), (0, 0, 0)))
            self.clips = clips
        if audio:
            self.bitrate = bitrate
            self.audio = self._composite_audio()
        else:
            self.audio = None
        audio_clip = self.audio
        super().__init__(*self._composite_video_clip())
        self.set_audio(audio_clip)

    def __repr__(self):
        return f'<{self.__class__.__name__} start={self.start} end={self.end} fps={self.fps} size={self.size} use_bgclip={self.use_bgclip}, {id(self)}>'

    def __str__(self):
        return f'{self.__class__.__name__} start={self.start} end={self.end} fps={self.fps} size={self.size} use_bgclip={self.use_bgclip}'

    def _composite_video_clip(self):
        fps = 0
        for clip in self.clips:
            if clip.fps:
                if clip.fps > fps:
                    fps = clip.fps
        if not fps:
            raise

        if self.use_bgclip:
            td = 1 / fps
            ed = self.bg_clip.end if self.bg_clip.end else (
                _ for _ in ()).throw(ValueError())
            t = self.bg_clip.start
            clip_frames = []
            while t <= ed:
                bg_frame: Image.Image = self.bg_clip.make_frame_pil(
                    t)  # type: ignore
                for clip in self.clips:
                    if clip.start <= t <= (clip.end if clip.end is not None else float('inf')):
                        frm: Image.Image = clip.make_frame_pil(t)
                        bg_frame.paste(frm, clip.pos(t))
                clip_frames.append(bg_frame)
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
                bg_frame: Image.Image = self.bg_clip.make_frame_pil(
                    t)  # type: ignore
                for clip in self.clips:
                    if clip.start <= t <= (clip.end if clip.end is not None else float('inf')):
                        frm: Image.Image = clip.make_frame_pil(t)
                        bg_frame.paste(frm, clip.pos(t),)
                clip_frames.append(bg_frame)
                t += td
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
                bg_audio.clip = AudioSegment.silent(
                    int(self.bg_clip.duration*1000), self.bitrate)
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
                    audio.clip = AudioSegment.silent(
                        int(clip.duration*1000), self.bitrate)
                    audios.append(audio)
                else:
                    raise ValueError("The duration of the clip is Not Set.")
        return CompositeAudioClip(audios, self.use_bgclip, self.bitrate)

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

# def concatenate_videoclips(clips: list[VideoClip], audio=True, scale=False):
#     frames = []
#     if scale:
#         for clip in clips:
#             clip.f


if __name__ == '__main__':
    SystemExit()
