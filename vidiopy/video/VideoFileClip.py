from typing import Self, Union
from PIL import Image
import ffmpegio
import numpy as np
from .VideoClip import VideoClip
from ..audio.AudioClip import AudioFileClip
from ..decorators import *


class VideoFileClip(VideoClip):
    """
    A class used to represent a video file clip.

    This class extends the VideoClip class and provides additional functionality for working with video files. It uses ffmpeg to read video files, extract frames, and set the properties of the video clip. It also provides methods for transforming frames, creating sub-clips, and generating frame representations.

    Attributes:
        filename (str): The name of the video file.
        fps (float): The frames per second of the video.
        size (tuple): The width and height of the video.
        start (float): The start time of the video clip.
        end (float): The end time of the video clip.
        duration (float): The duration of the video clip.
        audio (AudioFileClip): The audio of the video clip.
        clip (tuple): The frames of the video clip as PIL Images.

    Methods:
        fl_frame_transform(func, *args, **kwargs): Applies a function to each frame of the video clip.
        fl_clip_transform(func, *args, **kwargs): Applies a function to each frame of the video clip along with its timestamp.
        sub_clip(t_start=None, t_end=None): Returns a sub-clip of the video clip.
        sub_clip_copy(t_start=None, t_end=None): Returns a copy of a sub-clip of the video clip.
        make_frame_array(t): Returns a numpy array representation of a specific frame in the video clip.
        make_frame_pil(t): Returns a PIL Image representation of a specific frame in the video clip.
        _import_video_clip(file_name, ffmpeg_options=None): Imports a video clip from a file using ffmpeg.
    """

    def __init__(
        self, filename: str, audio: bool = True, ffmpeg_options: dict | None = None
    ) -> None:
        """
        Initializes a new instance of the VideoFileClip class.

        This method creates a new VideoFileClip from a video file. It uses ffmpeg to read the video file, extract the frames, and set the properties of the video clip.

        Args:
            filename (str): The name of the video file to import.
            audio (bool, optional): Whether to include audio in the video clip. Defaults to True.
            ffmpeg_options (dict | None, optional): Additional options to pass to ffmpeg. Defaults to None.

        Raises:
            None

        Example:
            >>> video_clip = VideoFileClip("video.mp4")

        Note:
            This method uses ffmpeg to read the video file.
        """
        super().__init__()

        self.filename = filename

        # Probe video streams and extract relevant information
        video_data = ffmpegio.probe.video_streams_basic(str(filename))[0]

        # Import video clip using ffmpeg
        self.clip, self.fps = self._import_video_clip(str(filename), ffmpeg_options)
        self.fps = float(self.fps)
        # Set video properties
        self.size = (video_data["width"], video_data["height"])
        self.start = 0.0
        # not all videos have a duration attribute in their metadata
        if video_data["duration"]:
            self.end = video_data["duration"]
            self._dur = video_data["duration"]
        else:
            self.end = len(self.clip) / self.fps
            self._dur = self.end
        # If audio is enabled, attach audio clip
        if audio:
            audio = AudioFileClip(filename, self._dur)
            audio.set_start(self.start).set_end(self.end)
            self.set_audio(audio)

    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, filename={self.filename}, id={hex(id(self))},
        audio={(self.audio)})"""

    def __str__(self) -> str:
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, filename={self.filename}, id={hex(id(self))},
        audio={(self.audio)})"""

    def __eq__(self, other) -> bool:
        if not hasattr(self, "clip"):
            return False

        return (
            isinstance(other, VideoFileClip)
            and self.fps == other.fps
            and self.size == other.size
            and self.start == other.start
            and self.end == other.end
            and self.duration == other.duration
            and self.audio == other.audio
            and self.clip == other.clip
        )

    #################
    # EFFECT METHODS#
    #################

    @requires_start_end
    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """
        Applies a function to each frame of the video clip.

        This method iterates over each frame in the video clip, applies a function to it, and replaces the original frame with the result.

        Args:
            func (callable): The function to apply to each frame. It should take an Image as its first argument, and return an Image.
            *args: Additional positional arguments to pass to func.
            **kwargs: Additional keyword arguments to pass to func.

        Returns:
            Self: Returns the instance of the class with updated frames.

        Raises:
            None

        Example:
            >>> video_clip = VideoClip()
            >>> def invert_colors(image):
            ...     return ImageOps.invert(image)
            >>> video_clip.fl_frame_transform(invert_colors)

        Note:
            This method requires the start and end of the video clip to be set.
        """
        clip: list[Image.Image] = []
        for frame in self.clip:
            frame: Image.Image = func(frame, *args, **kwargs)
            clip.append(frame)
        self.clip = tuple(clip)
        return self

    @requires_fps
    def fl_clip_transform(self, func, *args, **kwargs) -> Self:
        """
        Applies a function to each frame of the video clip along with its timestamp.

        This method iterates over each frame in the video clip, applies a function to it and its timestamp, and replaces the original frame with the result.

        Args:
            func (callable): The function to apply to each frame. It should take an Image and a float (representing the timestamp) as its first two arguments, and return an Image.
            *args: Additional positional arguments to pass to func.
            **kwargs: Additional keyword arguments to pass to func.

        Returns:
            Self: Returns the instance of the class with updated frames.

        Raises:
            None

        Example:
            >>> video_clip = VideoClip()
            >>> def add_timestamp(image, timestamp):
            ...     draw = ImageDraw.Draw(image)
            ...     draw.text((10, 10), str(timestamp), fill="white")
            ...     return image
            >>> video_clip.fl_clip_transform(add_timestamp)

        Note:
            This method requires the fps of the video clip to be set.
        """
        td = 1 / self.fps
        frame_time = 0.0
        clip: list[Image.Image] = []
        for frame in self.clip:
            clip.append(func(frame, frame_time, *args, **kwargs))
            frame_time += td
        del self.clip
        self.clip = tuple(clip)
        return self

    @requires_fps
    def sub_clip(
        self,
        t_start: Union[int, float, None] = None,
        t_end: Union[int, float, None] = None,
    ):
        if t_end is None and t_start is None:
            return self.copy()
        if t_end is None:
            t_end = (
                self.end
                if self.end
                else (
                    self.duration
                    if self.duration
                    else (_ for _ in ()).throw(
                        ValueError("end or duration must be set.")
                    )
                )
            )
        if t_start is None:
            t_start = self.start if self.start else 0.0
        frames = []
        time_per_frame = 1 / self.fps
        current_frame_time = self.start

        while current_frame_time < t_end:
            frames.append(self.make_frame_pil(current_frame_time))
            current_frame_time += time_per_frame

        self.clip = tuple(frames)
        self.start = 0.0
        self.end = t_end
        self._dur = t_end - t_start

        if self.audio:
            audio = self.audio.sub_clip(t_start, t_end)
            audio.set_start(self.start).set_end(self.end)
            self.set_audio(audio)
        return self

    @requires_fps
    def sub_clip_copy(
        self,
        t_start: Union[int, float, None] = None,
        t_end: Union[int, float, None] = None,
    ):
        clip = self.copy()
        if t_end is None and t_start is None:
            return clip.copy()
        if t_end is None:
            t_end = (
                clip.end
                if clip.end
                else (
                    clip.duration
                    if clip.duration
                    else (_ for _ in ()).throw(
                        ValueError("end or duration must be set.")
                    )
                )
            )
        if t_start is None:
            t_start = clip.start if clip.start else 0.0
        frames = []
        time_per_frame = 1 / clip.fps
        current_frame_time = clip.start

        while current_frame_time < t_end:
            frames.append(clip.make_frame_pil(current_frame_time))
            current_frame_time += time_per_frame

        instance = clip.copy()

        instance.clip = tuple(frames)
        instance.start = 0.0
        instance.end = t_end
        instance._dur = t_end - t_start

        if instance.audio:
            audio = instance.audio.sub_clip(t_start, t_end)
            audio.set_start(self.start).set_end(self.end)
            instance.set_audio(audio)
        return instance

    @requires_duration
    def make_frame_array(self, t: int | float) -> np.ndarray:
        """
        Generates a numpy array representation of a specific frame in the video clip.

        This method calculates the index of the frame for a specific time, retrieves the frame from the video clip, and converts it to a numpy array.

        Args:
            t (int | float): The time of the frame to convert.

        Returns:
            np.ndarray: The numpy array representation of the frame.

        Raises:
            ValueError: If the duration of the video clip is not set.

        Example:
            >>> video_clip = VideoClip()
            >>> frame_array = video_clip.make_frame_array(10)

        Note:
            This method requires the duration of the video clip to be set.
        """
        if self.duration is None:
            raise ValueError("Duration is Not Set.")
        time_per_frame = self.duration / len(self.clip)
        frame_index = t / time_per_frame
        frame_index = int(min(len(self.clip) - 1, max(0, frame_index)))
        return np.array(self.clip[frame_index])

    @requires_duration
    def make_frame_pil(self, t: int | float) -> Image.Image:
        """
        Generates a PIL Image representation of a specific frame in the video clip.

        This method calculates the index of the frame for a specific time, retrieves the frame from the video clip, and returns it as a PIL Image.

        Args:
            t (int | float): The time of the frame to convert.

        Returns:
            Image.Image: The PIL Image representation of the frame.

        Raises:
            ValueError: If the duration of the video clip is not set.

        Example:
            >>> video_clip = VideoClip()
            >>> frame_image = video_clip.make_frame_pil(10)

        Note:
            This method requires the duration of the video clip to be set.
        """
        if self.duration is None:
            raise ValueError("Duration is Not Set.")
        time_per_frame = self.duration / len(self.clip)
        frame_index = t / time_per_frame
        frame_index = int(min(len(self.clip) - 1, max(0, frame_index)))
        return self.clip[frame_index]

    def _import_video_clip(
        self, file_name: str, ffmpeg_options: dict | None = None
    ) -> tuple:
        """
        Imports a video clip from a file using ffmpeg.

        This method reads a video file using ffmpeg, converts each frame to a PIL Image, and returns a tuple of the images and the fps of the video.

        Args:
            file_name (str): The name of the video file to import.
            ffmpeg_options (dict | None, optional): Additional options to pass to ffmpeg. Defaults to None.

        Returns:
            tuple: A tuple of the frames as PIL Images and the fps of the video.

        Raises:
            None

        Example:
            >>> video_clip = VideoClip()
            >>> frames, fps = video_clip._import_video_clip("video.mp4")

        Note:
            This method uses ffmpeg to read the video file.
        """
        options = {**(ffmpeg_options if ffmpeg_options else {})}
        fps, frames = ffmpegio.video.read(file_name, **options)
        return tuple(Image.fromarray(frame) for frame in frames), fps
