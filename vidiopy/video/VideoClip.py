from re import S
from rich import print as rich_print
from functools import wraps
import rich.progress as progress
from fractions import Fraction
import os
from copy import copy as copy_
import subprocess
import tempfile
from typing import Callable, Generator, Any, Self
from PIL import Image
import ffmpegio
import numpy as np
from ..Clip import Clip
from ..audio.AudioClip import AudioClip
from ..decorators import *
from .. import config


class VideoClip(Clip):
    def __init__(self) -> None:
        super().__init__()

        # Time-related properties
        self._st: int | float = 0.0
        self._ed: int | float | None = None
        self._dur: int | float | None = None

        # Video and audio properties
        self.audio: AudioClip | None = None
        self.fps: int | float | None = None
        self.size: tuple[int, int] | None = None

        # Position-related properties
        self.pos: Callable[
            [float | int], tuple[int | str | float, int | str | float]
        ] = lambda t: (0, 0)
        self.relative_pos = False

    #################
    # Magic Methods #
    #################

    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}, start={self.start}, end={self.end}, fps={self.fps}, size={self.size}, duration={self.duration}, audio={self.audio} id={hex(id(self))}"""

    def __str__(self) -> str:
        return f"""{self.__class__.__name__}, start={self.start}, end={self.end}, fps={self.fps}, size={self.size}, duration={self.duration}, audio={self.audio}"""

    def __len__(self) -> int | float | None:
        return self._dur

    @requires_fps
    def __iter__(self) -> Generator[np.ndarray[Any, Any], Any, None]:
        return self.iterate_frames_array_t(self.fps)

    #############################
    # Properties getter & setter#
    #############################

    @property
    @requires_size
    def width(self) -> int:
        """
        This is a property that returns the width of the video clip.

        The width is the first element of the size tuple (width, height).
        This property requires that the size of the video clip is set before accessing it.

        Raises:
            ValueError: If the size of the video clip is not set.

        Returns:
            int: The width of the video clip.
        """
        if self.size is not None:
            return self.size[0]
        else:
            raise ValueError("Size is not set")

    w = width

    @property
    @requires_size
    def height(self) -> int:
        """
        This is a property that returns the height of the video clip.

        The height is the second element of the size tuple (width, height).
        This property requires that the size of the video clip is set before accessing it.

        Raises:
            ValueError: If the size of the video clip is not set.

        Returns:
            int: The height of the video clip.
        """
        if self.size is not None:
            return self.size[1]
        else:
            raise ValueError("Size is not set")

    h = height

    @property
    @requires_size
    def aspect_ratio(self) -> Fraction:
        """
        This is a property that returns the aspect ratio of the video clip.

        The aspect ratio is the ratio of the width to the height of the video clip.
        It is represented as a Fraction for precise calculations.
        This property requires that the size of the video clip is set before accessing it.

        Raises:
            ValueError: If the size of the video clip is not valid.

        Returns:
            Fraction: The aspect ratio of the video clip.
        """
        if isinstance(self.w, int) and isinstance(self.h, int):
            return Fraction(self.w, self.h)
        else:
            raise ValueError("Size is not Valid")

    @property
    def start(self) -> int | float:
        """
        The start property is a getter for the _st attribute.

        Returns:
            int | float: The start time of the video clip.
        """
        return self._st

    @start.setter
    def start(self, t) -> "VideoClip":
        """
        The start property is a setter for the _st attribute.

        Args:
            t (int | float): The start time of the video clip.

        Returns:
            VideoClip: The instance of the VideoClip after setting the start time.
        """
        self._st = t

        if self.start is None:
            return self

        if self.audio:
            self.audio.start = self.start
        return self

    def set_start(self, value: int | float) -> "VideoClip":
        """
        The set_start method is used to set the start time of the video clip.

        Args:
            value (int | float): The start time of the video clip.

        Returns:
            VideoClip: The instance of the VideoClip after setting the start time.
        """
        self.start = value
        return self

    @property
    def end(self) -> int | float | None:
        """
        Property that gets the end time of the video clip.

        Returns:
            int | float | None: The end time of the video clip. If the end time is not set, it returns None.
        """
        return self._ed

    @end.setter
    def end(self, t) -> Self:
        """
        Setter for the end time of the video clip.

        Args:
            t (int | float): The end time to set for the video clip.

        Returns:
            VideoClip: The instance of the VideoClip after setting the end time.
        """
        self._ed = t
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
        return self

    def set_end(self, value) -> "VideoClip":
        """
        Method to set the end time of the video clip. This is an alternative to using the end property setter.

        Args:
            value (int | float): The end time to set for the video clip.

        Returns:
            VideoClip: The instance of the VideoClip after setting the end time.
        """
        self.end = value
        return self

    @property
    def duration(self) -> int | float | None:
        """
        Property that gets the duration of the video clip.

        Returns:
            int | float | None: The duration of the video clip. If the duration is not set, it returns None.
        """
        return self._dur

    @duration.setter
    def duration(self, dur: int | float) -> "VideoClip":
        """
        Setter for the duration of the video clip.
        it raises a ValueError since duration is not allowed to be set.
        but you can change the duration using clip._dur = value or _set_duration method.

        Args:
            dur (int | float): The duration to set for the video clip.

        Returns:
            NoReturn: Raises a ValueError since duration is not allowed to be set.

        Raises:
            ValueError: If an attempt is made to set the duration, a ValueError is raised.
        """
        self.set_duration(dur)
        return self

    def set_duration(self, value) -> "VideoClip":
        """
        Setter for the duration of the video clip.
        it raises a ValueError since duration is not allowed to be set.
        but you can change the duration using clip._dur = value or the _set_duration method.

        Args:
            dur (int | float): The duration to set for the video clip.

        Returns:
            NoReturn: Raises a ValueError since duration is not allowed to be set.

        Raises:
            ValueError: If an attempt is made to set the duration, a ValueError is raised.
        """
        raise ValueError("Duration is not allowed to be set")
        return self

    def _set_duration(self, value: int | float) -> "VideoClip":
        """
        Private method to set the duration of the video clip.

        Args:
            value (int | float): The duration to set for the video clip.

        Returns:
            VideoClip: The instance of the VideoClip after setting the duration.
        """
        self._dur = value
        return self

    def set_position(
        self,
        pos: (
            tuple[int | float | str, int | float | str]
            | list[int | float | str]
            | Callable[[float | int], tuple[int | float | str, int | float | str]]
        ),
        relative=False,
    ) -> Self:
        """
        Sets the position of the video clip.
        This is useful for the concatenate method, where the position of the video clip is used  to set it on other clip.
        This method allows the position of the video clip to be set either as a fixed tuple of coordinates, or as a function that returns a tuple of coordinates at each time. The position can be set as absolute or relative to the size of the clip using the relative.

        Note:
            - It Should Be the coordinates of the Video on the top left corner.
            - If relative is True, the position should be between the 0.0 & 1.0.
            - If relative is False, the position should be between the 0 & width or height of the video.


        Parameters:
            pos (tuple or callable): The position to set for the video clip. This can be either:
                - a tuple of two integers or floats, representing the x and y coordinates of the position, or
                - a callable that takes a single float or integer argument (representing the time) and returns a tuple of two integers or floats, representing the x and y coordinates of the position.
            relative (bool, optional): Whether the position is relative to the size of the clip. If True, the position is interpreted as a fraction of the clip's width and height. Defaults to False.

        Raises:
        TypeError:   If `pos` is not a tuple or a callable.

        Returns:
            self: Returns the instance of the class.
        """
        self.relative_pos = relative
        if callable(pos):
            self.pos = pos
        elif isinstance(pos, (tuple, list)):
            if len(pos) != 2:
                raise ValueError("Position must be a tuple of two elements")
            x = pos[0]
            y = pos[1]
            self.pos = lambda t: (x, y)
        return self

    def set_audio(self, audio: AudioClip | None) -> Self:
        """
        Sets the audio for the video clip.

        This method assigns the provided audio clip to the video clip. If the audio clip is not None,
        it also sets the start and end times of the audio clip to match the video clip's start and end times.

        Parameters:
        audio (AudioClip | None): The audio clip to be set to the video clip. If None, no audio is set.

        Returns:
        Self: Returns the instance of the class with updated audio clip.
        """
        self.audio = audio
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
        return self

    def without_audio(self) -> Self:
        """
        Removes the audio from the current VideoClip instance.

        This method sets the 'audio' attribute of the VideoClip instance to None, effectively removing any audio that the clip might have.

        Returns:
            VideoClip: The same instance of the VideoClip but without any audio. This allows for method chaining.

        Example:
            >>> clip = VideoClip(...)
            >>> clip_without_audio = clip.without_audio()

        Note:
            This method modifies the VideoClip instance in-place. If you want to keep the original clip with audio, consider making a copy before calling this method.
        """
        self.audio = None
        return self

    def set_fps(self, fps: int | float) -> "Self":
        """
        Set the frames per second (fps) for the video clip.

        This method allows you to set the fps for the video clip. The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother video playback.

        Parameters:
        fps (int | float): The frames per second value to set. This can be an integer
        or a float. For example, a value of 24 would mean 24 frames are shown per second.

        Raises:
        TypeError: If the provided fps value is not an integer or a float.

        Returns:
        Self: Returns the instance of the class, allowing for method chaining.

        Example:
        >>> clip = VideoClip()
        >>> clip.set_fps(24)
        """
        if not isinstance(fps, (int, float)):
            raise TypeError("fps must be an int or a float")

        self.fps = fps
        return self

    def __copy__(self) -> Self:
        """
        Create a shallow copy of the current instance.

        This method creates a new instance of the same class and copies all the
        attributes of the current instance to the new one. If the attribute value
        is an object, it will be a reference to the same object, not a new copy.

        Returns:
        Self: A new instance of the same class with the same attributes.

        Example:
        >>> clip1 = VideoClip()
        >>> clip2 = copy.copy(clip1)
        """
        # Get the class of the current instance
        cls = self.__class__

        # Create a new instance of the class
        new_clip = cls.__new__(cls)

        # Iterate through the attributes of the current instance
        for attr, value in self.__dict__.items():
            # Set the attribute in the new instance
            setattr(new_clip, attr, copy_(value))

        # Return the shallow copy
        return new_clip

    # Alias for the __copy__ method
    copy = __copy__

    ####################################
    # EFFECT METHODS  F I L T E R I N G#
    ####################################

    def make_frame_array(self, t) -> np.ndarray:
        """
        Generate a frame at time `t` as a NumPy array.

        This method is intended to be overridden in subclasses. It should return
        a NumPy array representing the frame at the given time.

        Parameters:
        t (float): The time at which to generate the frame.

        Raises:
        NotImplementedError: If the method is not overridden in a subclass.

        Returns:
        np.ndarray: A NumPy array representing the frame at time `t`.

        Example:
        >>> clip = VideoClipSubclass()
        >>> frame = clip.make_frame_array(0.5)
        """
        raise NotImplementedError(
            "Make Frame is Not Set., Must be overridden in the subclass."
        )

    def make_frame_pil(self, t) -> Image.Image:
        """
        Generate a frame at time `t` as a PIL Image.

        This method is intended to be overridden in subclasses. It should return
        a PIL Image representing the frame at the given time.

        Parameters:
        t (float): The time at which to generate the frame.

        Raises:
        NotImplementedError: If the method is not overridden in a subclass.

        Returns:
        Image.Image: A PIL Image representing the frame at time `t`.

        Example:
        >>> clip = VideoClipSubclass()
        >>> frame = clip.make_frame_pil(0.5)
        """
        raise NotImplementedError(
            "Make Frame pil is Not Set., Must be overridden in the subclass."
        )

    def get_frame(self, t: int | float, is_pil=None) -> np.ndarray | Image.Image:
        """
        Get a frame at time `t`.

        This method returns a frame at the given time `t`. The frame can be returned
        as a NumPy array or a PIL Image, depending on the value of `is_pil`.

        Parameters:
            t (int | float): The time at which to get the frame.
            is_pil (bool, optional): If True, the frame is returned as a PIL Image. If False or None, the frame is returned as a NumPy array. Defaults to None.

        Raises:
            ValueError: If `is_pil` is not True, False, or None.

        Returns:
            np.ndarray | Image.Image: The frame at time `t` as a NumPy array or a PIL Image.

        Example:
        >>> clip = VideoClip()
        >>> frame_array = clip.get_frame(0.5)
        >>> frame_pil = clip.get_frame(0.5, is_pil=True)
        """
        if is_pil is None or is_pil is False:
            return self.make_frame_array(t)
        elif is_pil is True:
            return self.make_frame_pil(t)
        else:
            raise ValueError("is_pil must be True, False, or None")

    def iterate_frames_pil_t(
        self, fps: int | float
    ) -> Generator[Image.Image, Any, None]:
        """
        Iterate over frames as PIL Images at a given frames per second (fps).

        This method generates frames at a given fps as PIL Images. The frames are
        generated from the start of the clip to the end or duration, whichever is set.

        Parameters:
            fps (int | float): The frames per second at which to generate frames.

        Raises:
            ValueError: If neither end nor duration is set.

        Yields:
            Image.Image: The next frame as a PIL Image.

        Example:
        >>> clip = VideoClip()
        >>> for frame in clip.iterate_frames_pil_t(24):
        ...     # Do something with frame
        """
        time_dif = 1 / fps
        t = self.start
        if self.end is not None:
            while t < self.end:
                yield self.make_frame_pil(t)
                t += time_dif
        elif self.duration is not None:
            while t < self.duration:
                yield self.make_frame_pil(t)
                t += time_dif
        else:
            raise ValueError("end or duration must be set.")

    def iterate_frames_array_t(
        self, fps: int | float
    ) -> Generator[np.ndarray, Any, None]:
        """
        Iterate over frames as NumPy arrays at a given frames per second (fps).

        This method generates frames at a given fps as NumPy arrays. The frames are
        generated from the start of the clip to the end or duration, whichever is set.

        Parameters:
            fps (int | float): The frames per second at which to generate frames.

        Raises:
            ValueError: If neither end nor duration is set.

        Yields:
            np.ndarray: The next frame as a NumPy array.

        Example:
        >>> clip = VideoClip()
        >>> for frame in clip.iterate_frames_array_t(24):
        ...     # Do something with frame
        """
        time_dif = 1 / fps
        t = 0
        if self.end is not None:
            while t < self.end:
                yield self.make_frame_array(t)
                t += time_dif
        elif self.duration is not None:
            while t < self.duration:
                yield self.make_frame_array(t)
                t += time_dif
        else:
            raise ValueError("end or duration must be set.")

    def sub_clip_copy(
        self, t_start: int | float | None = None, t_end: int | float | None = None
    ) -> Self:
        """
        Returns a subclip of the clip.__copy__, starting at time t_start (in seconds).

        Parameters:
            t_start (int | float | None, optional): The start time of the subclip in seconds. Defaults to None.
            t_end (int | float | None, optional): The end time of the subclip in seconds. Defaults to None.

        Returns:
            Self: The subclip of the clip.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.

        Example:
            >>> clip = VideoClip()
            >>> subclip = clip.sub_clip_copy(t_start=1.5, t_end=3.5)
        """
        raise NotImplementedError("sub_clip method must be overridden in the subclass.")

    def sub_clip(
        self, t_start: int | float | None = None, t_end: int | float | None = None
    ) -> Self:
        """
        Returns a subclip of the clip, starting at time t_start and ending at time t_end.

        Parameters:
            t_start (int | float | None, optional): The start time of the subclip in seconds. Defaults to None.
            t_end (int | float | None, optional): The end time of the subclip in seconds. Defaults to None.

        Returns:
            Self: The subclip of the clip.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.

        Example:
            >>> clip = VideoClip()
            >>> subclip = clip.sub_clip(t_start=1.5, t_end=3.5)
        """
        raise NotImplementedError("sub_clip method must be overridden in the subclass.")

    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """
        Apply a frame transformation function to each frame of the video clip.

        This method calls the provided function `func` on each frame of the clip and applies the transformation.
        The transformed frames are then stored in a list and assigned back to the clip.

        Parameters:
            - func: The frame transformation function to be applied.
            - *args: Additional positional arguments to be passed to the transformation function.
            - **kwargs: Additional keyword arguments to be passed to the transformation function.

        Returns:
            - Self: The modified video clip object.

        Example:
            >>> def grayscale(frame):
            >>>     # Convert frame to grayscale
            >>>     return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            >>>
            >>> clip = VideoClip()
            >>> clip.fl_frame_transform(grayscale)

        Note:
            - This method is meant to be overridden in the subclass. If not overridden, it raises a NotImplementedError.
            - The transformation function `func` should accept a single frame as the first argument and return the transformed frame.

        """
        raise NotImplementedError(
            "fl_frame_transform method must be overridden in the subclass."
        )
        return self

    def fl_clip_transform(self, func, *args, **kwargs) -> Self:
        """\
        Apply a function to the entire video clip, generating a new clip.
        calls the function func on the clip. like below
        >>> frames = []
        >>> for frame in clip._Depends_upon_sub_class_:
        >>>     frame = func(frame, frame_time, *args, **kwargs)
        >>>     frames.append(frame)
        >>> clip._Depends_upon_sub_class_ = tuple(frames)
        """
        raise NotImplementedError(
            "fl_clip_transform method must be overridden in the subclass."
        )
        return self

    def fl_time_transform(self, func_t: Callable[[int | float], int | float]) -> Self:
        """
        Apply a time transformation function to the clip.

        This method modifies the `make_frame_array` and `make_frame_pil` methods
        to apply a time transformation function `func_t` to the time `t` before
        generating the frame. This can be used to speed up, slow down, or reverse
        the clip, among other things.

        If the clip has audio, the same time transformation is applied to the audio.

        Parameters:
            func_t (Callable[[int | float], int | float]): The time transformation function to apply. This function should take a time `t` and return a new time.

        Returns:
            Self: Returns the instance of the class, allowing for method chaining.

        Example:
        >>> clip = VideoClip()
        >>> clip.fl_time_transform(lambda t: 2*t)  # Speed up the clip by a factor of 2
        """
        original_make_frame_pil_t = self.make_frame_pil
        original_make_frame_array_t = self.make_frame_array

        @wraps(original_make_frame_array_t)
        def modified_make_frame_array_t(t):
            transformed_t = func_t(t)
            return original_make_frame_array_t(transformed_t)

        @wraps(original_make_frame_pil_t)
        def modified_make_frame_pil_t(t):
            transformed_t = func_t(t)
            return original_make_frame_pil_t(transformed_t)

        self.make_frame_array = modified_make_frame_array_t
        self.make_frame_pil = modified_make_frame_pil_t

        if self.audio:
            self.audio = self.audio.fl_time_transform(func_t)
        return self

    def fx(self, func: Callable, *args, **kwargs) -> Self:
        """
        Apply an effect function to the clip.

        This method applies an effect function `func` to the clip. The effect function
        should take the clip as its first argument, followed by any number of positional
        and keyword arguments.

        The effect function should return a new clip, which is then returned by this method.

        Parameters:
            func (Callable[..., Self]): The effect function to apply. This function should take the clip as its first argument, followed by any number of positional and keyword arguments.
            *args: Positional arguments to pass to the effect function.
            **kwargs: Keyword arguments to pass to the effect function.

        Returns:
            Self: The new clip returned by the effect function.

        Example:
        >>> clip = VideoClip()
        >>> clip.fx(effect_function, arg1, arg2, kwarg1=value1)
        """
        func(self, *args, **kwargs)
        return self

    def sub_fx(
        self,
        func: Callable[..., Self],
        *args,
        start_t: int | float | None = None,
        end_t: int | float | None = None,
        **kwargs,
    ) -> Self:
        """
        Apply an effect function to a subclip of the clip.

        This method creates a subclip from `start_t` to `end_t`, applies an effect
        function `func` to the subclip, and returns the modified subclip.

        The effect function should take the clip as its first argument, followed by
        any number of positional and keyword arguments.

        Parameters:
            func (Callable[..., Self]): The effect function to apply. This function should take the clip as its first argument, followed by any number of positional and keyword arguments.
            *args: Positional arguments to pass to the effect function.
            start_t (int | float | None, optional): The start time of the subclip. If None, the start of the clip is used. Defaults to None.
            end_t (int | float | None, optional): The end time of the subclip. If None, the end of the clip is used. Defaults to None.
            **kwargs: Keyword arguments to pass to the effect function.

        Returns:
            Self: The modified subclip.

        Example:
        >>> clip = VideoClip()
        >>> subclip = clip.sub_fx(effect_function, arg1, arg2, start_t=1, end_t=2, kwarg1=value1)
        """
        clip = copy_(self)
        clip = clip.sub_clip(start_t, end_t)
        clip = clip.fx(func, *args, **kwargs)
        return clip

    def _sync_audio_video_s_e_d(self) -> Self:
        """
        Synchronizes the audio and video start, end, and duration attributes.

        This method is used to ensure that the audio and video parts of a clip are in sync.
        It sets the start, end, and original duration of the audio to match the video.

        Returns:
            Self: Returns the instance of the class with updated audio attributes.

        Raises:
            None

        Example:
            >>> video_clip = VideoClip()
            >>> video_clip._sync_audio_video_s_e_d()

        Note:
            This is an internal method, typically not meant to be used directly by the user.
        """
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
            self.audio._original_dur = self.duration
        return self

    #####################
    # EXPORT OPERATIONS #
    #####################

    def write_videofile(
        self,
        filename,
        fps=None,
        codec=None,
        bitrate=None,
        audio=True,
        audio_fps=44100,
        preset="medium",
        pixel_format=None,
        audio_codec=None,
        audio_bitrate=None,
        threads=None,
        ffmpeg_params: dict[str, str] | None = None,
        logger="bar",
        over_write_output=True,
        show_log=False,
    ) -> Self:
        """
        Writes the video clip to a file.

        This method generates video frames, processes them, and writes them to a file.
        If audio is present in the clip, it is also written to the file.

        Args:
            filename (str): The name of the file to write.
            fps (int, optional): The frames per second to use for the output video. If not provided, the fps of the video clip is used.
            codec (str, optional): The codec to use for the output video.
            bitrate (str, optional): The bitrate to use for the output video.
            audio (bool, optional): Whether to include audio in the output video. Defaults to True.
            audio_fps (int, optional): The frames per second to use for the audio. Defaults to 44100.
            preset (str, optional): The preset to use for the output video. Defaults to "medium".
            pixel_format (str, optional): The pixel format to use for the output video.
            audio_codec (str, optional): The codec to use for the audio.
            audio_bitrate (str, optional): The bitrate to use for the audio.
            threads (int, optional): The number of threads to use for writing the video file.
            ffmpeg_params (dict[str, str] | None, optional): Additional parameters to pass to ffmpeg.
            logger (str, optional): The logger to use. Defaults to "bar".
            over_write_output (bool, optional): Whether to overwrite the output file if it already exists. Defaults to True.

        Returns:
            Self: Returns the instance of the class.

        Raises:
            Exception: If fps is not provided and not set in the video clip.

        Example:
            >>> video_clip = VideoClip()
            >>> video_clip.write_videofile("output.mp4")

        Note:
            This method uses ffmpeg to write the video file.
        """
        # Generate video frames using iterate_frames_array_t method
        total_frames = (
            int(
                (self.end - self.start)
                / (
                    1
                    / (
                        fps
                        if fps
                        else (
                            self.fps
                            if self.fps
                            else (_ for _ in ()).throw(
                                Exception("fps is not provided and set.")
                            )
                        )
                    )
                )
            )
            if self.end is not None
            else 0
        )

        video_np = np.asarray(
            tuple(
                progress.track(
                    self.iterate_frames_array_t(
                        fps
                        if fps
                        else (
                            self.fps
                            if self.fps
                            else (_ for _ in ()).throw(
                                Exception("fps is not provided and set.")
                            )
                        )
                    ),
                    description="Processing Frames ...",
                    total=total_frames,
                    transient=True,
                    style="bar.back",
                )
            )
        )
        rich_print(
            "[bold magenta]Vidiopy[/bold magenta] - Video Frames Has Been Processed :thumbs_up:."
        )
        # Extract audio name without extension
        audio_name = os.path.split(filename)[1].split(".")[0]

        # Set default values for ffmpeg options
        ffmpeg_options = {
            "preset": preset,
            **(ffmpeg_params if ffmpeg_params is not None else {}),
            **({"c:v": codec} if codec else {}),
            **({"b:v": bitrate} if bitrate else {}),
            **({"pix_fmt": pixel_format} if pixel_format else {}),
            **({"c:a": audio_codec} if audio_codec else {}),
            **({"ar": audio_fps} if audio_fps else {}),
            **({"b:a": audio_bitrate} if audio_bitrate else {}),
            **({"threads": threads} if threads else {}),
        }

        audio_file_name = None
        temp_video_file_name = None

        try:
            # Determine the fps to use
            fps_to_use = fps if fps else self.fps if self.fps else None

            # Create a temporary video file
            dir__, file__ = os.path.split(filename)
            temp_video_file = tempfile.NamedTemporaryFile(
                dir=dir__,
                suffix="video__temp__" + os.path.splitext(file__)[1],
                delete=False,
            )
            temp_video_file_name = temp_video_file.name
            temp_video_file.close()

            # Write video frames to the temporary file using ffmpegio
            with progress.Progress(transient=True) as progress_bar:
                current_frame = 0
                pbar = progress_bar.add_task(
                    description="Writing Video File",
                    total=total_frames,
                )

                def function_callback(status: dict, done: bool):
                    nonlocal current_frame
                    current_frame = status["frame"] - current_frame
                    progress_bar.update(pbar, completed=current_frame, refresh=True)

                ffmpegio.video.write(
                    temp_video_file_name,
                    fps_to_use,
                    video_np,
                    overwrite=over_write_output,
                    progress=function_callback,
                    show_log=show_log,
                    **ffmpeg_options,
                )
                progress_bar.update(pbar, completed=True, visible=False)
            rich_print(
                "[bold magenta]Vidiopy[/bold magenta] - Video is Created :thumbs_up:"
            )
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
                    sp = progress_bar.add_task("Combining Video & Audio", total=None)
                    x = subprocess.run(
                        f'{config.FFMPEG_BINARY} -i "{temp_video_file_name}" -i "{audio_file_name}" -acodec copy {"-y " if over_write_output else ""} "{filename}"',
                        capture_output=True,
                        text=True,
                    )
                    progress_bar.update(sp, completed=True)
                rich_print(
                    f"[bold magenta]Vidiopy[/bold magenta] - ✔ Audio Video Combined Final video : - {filename} :thumbs_up:",
                    flush=True,
                )

            return self
        finally:
            if audio_file_name:
                os.remove(audio_file_name)
            # Rename temporary video file to the final filename if no audio is present
            if (not self.audio or not audio) and temp_video_file_name:
                print(temp_video_file_name)
                os.replace(temp_video_file_name, filename)
                temp_video_file_name = None
                rich_print(
                    f"[bold magenta]Vidiopy[/bold magenta] - ✔ Final video : - {filename} :thumbs_up:",
                    flush=True,
                )
            if temp_video_file_name:
                os.remove(temp_video_file_name)

    def write_videofile_subclip(
        self,
        filename,
        start_t: int | float | None = None,
        end_t: int | float | None = None,
        fps=None,
        codec=None,
        bitrate=None,
        audio=True,
        audio_fps=44100,
        preset="medium",
        pixel_format=None,
        audio_codec=None,
        audio_bitrate=None,
        write_logfile=False,
        verbose=True,
        threads=None,
        ffmpeg_params: dict[str, str] | None = None,
        logger="bar",
        over_write_output=True,
    ) -> Self:
        """
        Writes a subclip of the video clip to a file.

        This method generates video frames for a specific part of the video (subclip), processes them, and writes them to a file.
        If audio is present in the clip, it is also written to the file.

        Args:
            filename (str): The name of the file to write.
            start_t (int | float | None, optional): The start time of the subclip. If not provided, the start of the video is used.
            end_t (int | float | None, optional): The end time of the subclip. If not provided, the end of the video is used.
            fps (int, optional): The frames per second to use for the output video. If not provided, the fps of the video clip is used.
            codec (str, optional): The codec to use for the output video.
            bitrate (str, optional): The bitrate to use for the output video.
            audio (bool, optional): Whether to include audio in the output video. Defaults to True.
            audio_fps (int, optional): The frames per second to use for the audio. Defaults to 44100.
            preset (str, optional): The preset to use for the output video. Defaults to "medium".
            pixel_format (str, optional): The pixel format to use for the output video.
            audio_codec (str, optional): The codec to use for the audio.
            audio_bitrate (str, optional): The bitrate to use for the audio.
            write_logfile (bool, optional): Whether to write a logfile. Defaults to False.
            verbose (bool, optional): Whether to print verbose output. Defaults to True.
            threads (int, optional): The number of threads to use for writing the video file.
            ffmpeg_params (dict[str, str] | None, optional): Additional parameters to pass to ffmpeg.
            logger (str, optional): The logger to use. Defaults to "bar".
            over_write_output (bool, optional): Whether to overwrite the output file if it already exists. Defaults to True.

        Returns:
            Self: Returns the instance of the class.

        Raises:
            Exception: If fps is not provided and not set in the video clip.

        Example:
            >>> video_clip = VideoClip()
            >>> video_clip.write_videofile_subclip("output.mp4", start_t=10, end_t=20)

        Note:
            This method uses ffmpeg to write the video file.
        """
        clip = self.sub_clip_copy(start_t, end_t)
        clip.write_videofile(
            filename,
            fps,
            codec,
            bitrate,
            audio,
            audio_fps,
            preset,
            pixel_format,
            audio_codec,
            audio_bitrate,
            write_logfile,
            verbose,
            threads,
            ffmpeg_params,
            logger,
            over_write_output,
        )
        return self

    def write_image_sequence(
        self, nformat: str, fps: int | float | None = None, dir="."
    ) -> Self:
        """
        Writes the frames of the video clip as an image sequence.

        This method generates video frames, processes them, and writes them as images to a directory.
        The images are named by their frame number and the provided format.

        Args:
            nformat (str): The format to use for the output images.
            fps (int | float | None, optional): The frames per second to use for the output images. If not provided, the fps of the video clip is used.
            dir (str, optional): The directory to write the images to. Defaults to the current directory.

        Returns:
            Self: Returns the instance of the class.

        Raises:
            ValueError: If fps is not provided and fps and duration are not set in the video clip.

        Example:
            >>> video_clip = VideoClip()
            >>> video_clip.write_image_sequence("png", fps=24, dir="frames")

        """

        def save_frame(frame: Image.Image, frame_number: int):
            frame.save(
                os.path.join(
                    dir, f"{frame_number:0{len(str(total_frames)) + 1}}{nformat}"
                )
            )

        if dir != "." and not os.path.exists(dir):
            os.makedirs(dir)

        if fps:
            frames_generator = self.iterate_frames_pil_t(fps)
            total_frames = (1 / fps) * self.duration if self.duration else None
        elif self.fps and self.duration:
            frames_generator = self.iterate_frames_pil_t(self.fps)
            total_frames = (1 / self.fps) * self.duration if self.duration else None
        else:
            raise ValueError(
                "Warning: FPS is not provided, and fps and duration are not set."
            )

        frame_number = 0
        for frame in progress.track(
            frames_generator,
            total=total_frames,
            description="Vidiopy - Writing Image Sequence :smiley:",
            transient=True,
        ):
            save_frame(frame, frame_number)
            frame_number += 1
        rich_print(
            "[bold magenta]Vidiopy[/bold magenta] - Image Sequence Has Been Written:thumbs_up:."
        )
        return self

    def save_frame(self, t: int | float, filename: str) -> Self:
        """
        Saves a specific frame of the video clip as an image.

        This method generates a video frame for a specific time, processes it, and writes it as an image to a file.

        Args:
            t (int | float): The time of the frame to save.
            filename (str): The name of the file to write.

        Returns:
            Self: Returns the instance of the class.

        Raises:
            None

        Example:
            >>> video_clip = VideoClip()
            >>> video_clip.save_frame(10, "frame10.png")

        """
        self.make_frame_pil(t).save(filename)
        return self

    def to_ImageClip(self, t: int | float):
        """
        Converts a specific frame of the video clip to an ImageClip.

        This method generates a video frame for a specific time, processes it, and converts it to an ImageClip.

        Args:
            t (int | float): The time of the frame to convert.

        Returns:
            Data2ImageClip: The converted ImageClip.

        Raises:
            None

        Example:
            >>> video_clip = VideoClip()
            >>> image_clip = video_clip.to_ImageClip(10)
        """
        return ImageClips.Data2ImageClip(self.make_frame_pil(t))
