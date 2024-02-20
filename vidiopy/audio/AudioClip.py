from functools import wraps
import pathlib
from typing import Callable, Generator, NoReturn, Self
from copy import copy as copy_
import ffmpegio
import numpy as np
from ..Clip import Clip

__all__ = [
    "AudioClip",
    "AudioFileClip",
    "AudioArrayClip",
    "concatenate_audioclips",
    "composite_audioclips",
]


class AudioClip(Clip):
    """
    The AudioClip class represents an audio clip. It is a subclass of the Clip class.
    """

    def __init__(self, duration=None, fps=None):
        """
        Constructs all the necessary attributes for the AudioClip object.

        Parameters:
            duration (int or float, optional): The duration of the audio clip. Defaults to None.
            fps (int, optional): Frames per second of the audio clip. Defaults to None.
        """
        super().__init__()
        self.fps: int | None = fps
        self._original_dur: int | float | None = duration
        self._audio_data: np.ndarray | None = None
        self.channels: int | None = None
        self._st: int | float = 0.0
        self._ed: int | float | None = duration

    def __repr__(self):
        return f"""{self.__class__.__name__}(start={self.start}, end={self.end}, duration={self.duration}, fps={self.fps}, channels={self.channels}, id={hex(id(self))})"""

    def __str__(self):
        return f"""{self.__class__.__name__}(start={self.start}, end={self.end}, duration={self.duration}, fps={self.fps}, channels={self.channels})"""

    def __eq__(self, other):
        if isinstance(other, AudioClip):
            return (
                self.start == other.start
                and self.end == other.end
                and self.duration == other.duration
                and self.fps == other.fps
                and self.channels == other.channels
                and (
                    (
                        self._audio_data is not None
                        and other._audio_data is not None
                        and np.array_equal(self._audio_data, other._audio_data)
                    )
                    or (self._audio_data is None and other._audio_data is None)
                )
            )
        return False

    @property
    def audio_data(self) -> np.ndarray:
        """
        This property gets the audio data. If the audio data is not set, it raises a ValueError.

        Returns:
            np.ndarray: The audio data.

        Raises:
            ValueError: If the audio data is not set.

        Example:
            >>> clip = AudioClip()
            >>> clip.audio_data = np.array([1, 2, 3])
            >>> print(clip.audio_data)
            array([1, 2, 3])
        """
        if self._audio_data is None:
            raise ValueError("AudioClip._audio_data is None")
        return self._audio_data

    @audio_data.setter
    def audio_data(self, audio_data: np.ndarray) -> None:
        """
        This method sets the audio data.

        Args:
            audio_data (np.ndarray): The audio data to set.

        Example:
            >>> clip = AudioClip()
            >>> clip.audio_data = np.array([1, 2, 3])
            >>> print(clip.audio_data)
            array([1, 2, 3])
        """
        self._audio_data = audio_data

    def set_data(self, audio_data: np.ndarray) -> Self:
        """
        This method sets the audio data and returns the instance of the class.

        Args:
            audio_data (np.ndarray): The audio data to set.

        Returns:
            AudioClip: The instance of the class.

        Example:
            >>> clip = AudioClip()
            >>> clip.set_data(np.array([1, 2, 3]))
            >>> print(clip.audio_data)
            array([1, 2, 3])
        """
        self._audio_data = audio_data
        return self

    def set_fps(self, fps: int | None) -> Self:
        """
        This method sets the frames per second (fps) for the audio clip and returns the instance of the class.

        Args:
            fps (int | None): The frames per second to set. If None, the fps will be unset.

        Returns:
            AudioClip: The instance of the class.

        Example:
            >>> clip = AudioClip()
            >>> clip.set_fps(30)
            >>> print(clip.fps)
            30
        """
        self.fps = fps
        return self

    @property
    def duration(self) -> int | float | None:
        """
        This property gets the duration of the audio clip. The duration is represented in seconds and can be an integer,
        a float, or None if the duration is not set.

        Returns:
            int | float | None: The duration of the audio clip in seconds.
        """
        return self._original_dur

    @duration.setter
    def duration(self, duration: int | float) -> NoReturn:
        """
        This setter method raises an AttributeError when trying to set the duration directly.
        The duration of an AudioClip should be set using the set_duration method instead.

        Args:
            duration (int | float): The duration to set.

        Raises:
            AttributeError: Always raises an AttributeError to prevent direct setting of the duration.
        """
        raise AttributeError("Not Allowed to set duration")

    def set_duration(self, duration: int | float) -> Self:
        """
        This method sets the duration of the audio clip and returns the instance of the class.
        The duration is represented in seconds and can be an integer or a float.

        Args:
            duration (int | float): The duration to set in seconds.

        Returns:
            AudioClip: The instance of the class with the updated duration.
        """
        self._original_dur = duration
        return self

    get_duration = duration

    @property
    def start(self) -> int | float:
        """
        This property gets the start time of the audio clip. The start time is represented in seconds and can be an integer or a float.

        Returns:
            int | float: The start time of the audio clip in seconds.
        """
        return self._st

    @start.setter
    def start(self, start: int | float) -> None:
        """
        This setter method sets the start time of the audio clip. The start time is represented in seconds and can be an integer or a float.

        Args:
            start (int | float): The start time to set in seconds.
        """
        self._st = start

    def set_start(self, start: int | float) -> Self:
        """
        This method sets the start time of the audio clip and returns the instance of the class.
        The start time is represented in seconds and can be an integer or a float.

        Args:
            start (int | float): The start time to set in seconds.

        Returns:
            AudioClip: The instance of the class with the updated start time.
        """
        self._st = start
        return self

    @property
    def end(self) -> int | float | None:
        """
        This property gets the end time of the audio clip. The end time is represented in seconds and can be an integer,
        a float, or None if the end time is not set.

        Returns:
            int | float | None: The end time of the audio clip in seconds.
        """
        return self._ed

    @end.setter
    def end(self, end: int | float | None) -> None:
        """
        This setter method sets the end time of the audio clip. The end time is represented in seconds and can be an integer,
        a float, or None if the end time is not to be set.

        Args:
            end (int | float | None): The end time to set in seconds.
        """
        self._ed = end

    def set_end(self, end: int | float | None) -> Self:
        """
        This method sets the end time of the audio clip and returns the instance of the class.
        The end time is represented in seconds and can be an integer, a float, or None if the end time is not to be set.

        Args:
            end (int | float | None): The end time to set in seconds.

        Returns:
            AudioClip: The instance of the class with the updated end time.
        """
        self._ed = end
        return self

    def get_frame_at_t(self, t: int | float) -> np.ndarray:
        """
        This method gets the audio frame at a specific time `t`. The time `t` is represented in seconds and can be an integer or a float.
        It calculates the frame index using the duration, total frames, and time `t`, and returns the audio data at that frame index.

        Args:
            t (int | float): The time in seconds at which to get the audio frame.

        Returns:
            np.ndarray: The audio data at the specified time.

        Raises:
            ValueError: If frames per second (fps) is not set, audio data is not set, or original duration is not set.
        """
        if self.fps is None:
            raise ValueError("Frames per second (fps) is not set")
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None and self.end is None:
            raise ValueError("Original duration is not set")

        # Calculate the Frame index using the duration, total_frames & time t
        frame_index = int((t / (self.end or self.duration)) * len(self._audio_data)) - 1
        return self._audio_data[frame_index]

    def iterate_frames_at_fps(
        self, fps: int | float | None = None
    ) -> Generator[np.ndarray, None, None]:
        """
        This method generates audio frames at a specific frames per second (fps) rate. If no fps is provided, it uses the fps set in the AudioClip instance.
        It calculates the original fps using the duration and total frames, then generates frames at the specified fps rate.

        Args:
            fps (int | float | None, optional): The frames per second rate at which to generate frames. If not provided, the fps set in the AudioClip instance is used.

        Yields:
            np.ndarray: The audio data at each frame.

        Raises:
            ValueError: If frames per second (fps) is not set, audio data is not set, or original duration is not set.
        """
        if fps is None:
            if self.fps is None:
                raise ValueError("Frames per second (fps) is not set")
            fps = self.fps
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None:
            raise ValueError("Original duration is not set")

        # Calculate the original fps
        original_fps = len(self._audio_data) / self.duration

        # Calculate the frame index based on the original fps
        frame_index = 0
        while frame_index < len(self._audio_data):
            yield self._audio_data[frame_index]
            frame_index += int(original_fps / fps)

    def iterate_all_frames(self) -> Generator[np.ndarray, None, None]:
        """
        This method generates all audio frames in the AudioClip instance. It iterates over each frame in the audio data and yields it.

        Yields:
            np.ndarray: The audio data at each frame.

        Raises:
            ValueError: If audio data is not set.
        """
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        for frame in self._audio_data:
            yield frame

    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """
        This method applies a function to each frame of the audio data. The function should take a frame (an ndarray of channel data) as its first argument,
        followed by any number of additional positional and keyword arguments.

        Args:
            func (Callable): The function to apply to each frame. It should take a frame (an ndarray of channel data) as its first argument.
            *args: Additional positional arguments to pass to the function.
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            AudioClip: The instance of the class with the transformed audio data.

        Raises:
            ValueError: If audio data is not set.
        """
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        self._audio_data = np.array(
            [func(frame, *args, **kwargs) for frame in self._audio_data]
        )
        return self

    def fl_clip_transform(self, func, *args, **kwargs) -> Self:
        """
        This method applies a function to the entire audio data. The function should take the AudioClip instance as its first argument,
        followed by any number of additional positional and keyword arguments.

        Args:
            func (Callable): The function to apply to the audio data. It should take the AudioClip instance as its first argument.
            *args: Additional positional arguments to pass to the function.
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            AudioClip: The instance of the class with the transformed audio data.

        Raises:
            ValueError: If audio data is not set.
        """
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        func(self, *args, **kwargs)
        return self

    def fl_time_transform(self, func: Callable[[int | float], int | float]) -> Self:
        """
        This method applies a time transformation function to the `get_frame_at_t` method of the AudioClip instance.
        The transformation function should take a time (an integer or a float) as its argument and return a transformed time.

        The `get_frame_at_t` method is replaced with a new method that applies the transformation function to its argument before calling the original method.

        Args:
            func (Callable[[int | float], int | float]): The time transformation function to apply. It should take a time (an integer or a float) as its argument and return a transformed time.

        Returns:
            AudioClip: The instance of the class with the transformed `get_frame_at_t` method.

        Raises:
            ValueError: If the `get_frame_at_t` method is not set.
        """
        if self.get_frame_at_t is None:
            raise ValueError("`get_frame_at_t` method is not set")

        original_get_frame_at_t = copy_(self.get_frame_at_t)

        @wraps(original_get_frame_at_t)
        def new_get_frame_at_t(t: int | float) -> np.ndarray:
            return original_get_frame_at_t(func(t))

        self.get_frame_at_t = new_get_frame_at_t
        return self

    def sub_clip(
        self, start: float | int | None = None, end: float | int | None = None
    ) -> Self:
        """
        This method creates a subclip from the audio clip starting from `start` to `end`. If `start` or `end` is not provided,
        it uses the start or end time set in the AudioClip instance. If neither is set, it uses 0 for start and the duration for end.

        It calculates the original frames per second (fps) using the duration and total frames, then calculates the start and end frame indices using the original fps.
        It then updates the audio data, original duration, end time, and start time of the AudioClip instance.

        Args:
            start (float | int | None, optional): The start time of the subclip in seconds. If not provided, the start time set in the AudioClip instance is used. Defaults to None.
            end (float | int | None, optional): The end time of the subclip in seconds. If not provided, the end time set in the AudioClip instance is used. Defaults to None.

        Returns:
            AudioClip: The instance of the class with the updated audio data, original duration, end time, and start time.

        Raises:
            ValueError: If audio data is not set, original duration is not set, or end time is greater than the original duration.
        """
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None:
            raise ValueError("Original duration is not set")
        if start is None:
            start = self.start if self.start is not None else 0
        if end is None:
            end = (
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
        # Add check for end value
        if end > self.duration:
            raise ValueError("End value cannot be greater than the original duration")

        # Calculate the original fps
        original_fps = len(self._audio_data) / self.duration

        # Calculate the frame index based on the original fps
        start_frame_index = int(start * original_fps)
        end_frame_index = int(end * original_fps)

        self._audio_data = self._audio_data[start_frame_index:end_frame_index]
        self._original_dur = end - start
        self.end = end
        self.start = start
        return self

    def sub_clip_copy(
        self, start: float | int | None = None, end: float | int | None = None
    ) -> Self:
        """
        This method creates a copy of the AudioClip instance and then creates a subclip from the audio clip starting from `start` to `end` in the copied instance.
        If `start` or `end` is not provided, it uses the start or end time set in the AudioClip instance. If neither is set, it uses 0 for start and the duration for end.

        It calculates the original frames per second (fps) using the duration and total frames, then calculates the start and end frame indices using the original fps.
        It then updates the audio data, original duration, end time, and start time of the copied AudioClip instance.

        Args:
            start (float | int | None, optional): The start time of the subclip in seconds. If not provided, the start time set in the AudioClip instance is used. Defaults to None.
            end (float | int | None, optional): The end time of the subclip in seconds. If not provided, the end time set in the AudioClip instance is used. Defaults to None.

        Returns:
            AudioClip: A copy of the instance of the class with the updated audio data, original duration, end time, and start time.

        Raises:
            ValueError: If audio data is not set, original duration is not set, or end time is greater than the original duration.
        """
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None:
            raise ValueError("Original duration is not set")
        if start is None:
            start = self.start if self.start is not None else 0
        if end is None:
            end = (
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
        # Add check for end value
        if end > self.duration:
            raise ValueError("End value cannot be greater than the original duration")

        # Calculate the original fps
        original_fps = len(self._audio_data) / self.duration

        # Calculate the frame index based on the original fps
        start_frame_index = int(start * original_fps)
        end_frame_index = int(end * original_fps)

        audio_data = self._audio_data[start_frame_index:end_frame_index]

        instance = self.copy()
        instance._audio_data = audio_data
        instance.start = start
        instance.end = end
        instance._original_dur = end - start
        return instance

    def copy(self) -> Self:
        """
        This method creates a deep copy of the AudioClip instance and returns it.
        It uses the `copy_` function, which should be a deep copy function like `copy.deepcopy` in Python's standard library.

        Returns:
            AudioClip: A deep copy of the instance of the class.

        Raises:
            ValueError: If the `copy_` function is not set or does not correctly create a deep copy.
        """
        if copy_ is None:
            raise ValueError("`copy_` function is not set")
        return copy_(self)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, end = key.start, key.stop
            return self.sub_clip_copy(start, end)
        else:
            raise TypeError("Invalid argument type.")

    def write_audiofile(
        self,
        path: str,
        fps: int | None = None,
        overwrite=True,
        show_log=False,
        **kwargs,
    ):
        """
        This method writes the audio data to an audio file at the specified path.
        It uses the frames per second (fps) if provided, otherwise it uses the fps set in the AudioClip instance.
        It raises a ValueError if fps is not set in either way.
        It also raises a ValueError if audio data, original duration, or channels are not set.

        It creates a temporary audio data array by getting the frame at each time step from 0 to the end or duration with a step of 1/fps.
        It then writes the temporary audio data to the audio file using the `ffmpegio.audio.write` function.

        Args:
            path (str): The path to write the audio file to.
            fps (int | None, optional): The frames per second to use. If not provided, the fps set in the AudioClip instance is used. Defaults to None.
            overwrite (bool, optional): Whether to overwrite the audio file if it already exists. Defaults to True.
            show_log (bool, optional): Whether to show the log of the `ffmpegio.audio.write` function. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the `ffmpegio.audio.write` function.

        Raises:
            ValueError: If fps is not set, audio data is not set, original duration is not set, or channels are not set.
        """
        if fps is None:
            if self.fps is None:
                raise ValueError("Frames per second (fps) is not set")
            fps = self.fps
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None and self.end is None:
            raise ValueError("Original duration is not set")
        if self.channels is None:
            raise ValueError("Channels is not set")

        # Convert the audio Data to the temp_Audio_Data using the duration & fps & _audio_data
        temp_audio_data = np.array(
            [
                self.get_frame_at_t(t)
                for t in np.arange(0, self.end or self.duration, 1 / fps)
            ]
        )
        ffmpegio.audio.write(
            path, fps, temp_audio_data, overwrite=overwrite, show_log=show_log, **kwargs
        )


class SilenceClip(AudioClip):
    """
    SilenceClip is a subclass of AudioClip that represents a silent audio clip.

    Attributes:
        fps (int): The frames per second of the audio clip. Default is 44100.
        _original_dur (int | float): The original duration of the audio clip.
        channels (int): The number of audio channels. Default is 1.
        _audio_data (numpy.ndarray): The audio data represented as a numpy array of zeros.
    """

    def __init__(self, duration: int | float, fps: int = 44100, channels: int = 1):
        """
        Constructs all the necessary attributes for the SilenceClip object.

        Args:
            duration (int | float): The duration of the audio clip.
            fps (int, optional): The frames per second of the audio clip. Default is 44100.
            channels (int, optional): The number of audio channels. Default is 1.
        """
        self.fps = fps
        self._original_dur: int | float = duration
        super().__init__(self._original_dur, self.fps)
        self.channels = channels
        self._audio_data = np.zeros((int(duration * self.fps), self.channels))


class AudioFileClip(SilenceClip):
    """
    AudioFileClip is a class that represents an audio file. It extends the SilenceClip class.

    Attributes:
        fps (int): The sample rate of the audio file, default is 44100.
        channels (int): The number of channels in the audio file, default is 1.
        _original_dur (float): The original duration of the audio file.
        path (str): The path to the audio file.
        start (float): The start time of the audio file.
        end (float): The end time of the audio file.
        _audio_data (numpy.ndarray): The audio data read from the file.
        More from the SilenceClip Class

    """

    def __init__(self, path: str | pathlib.Path, duration: int | float | None = None):
        """
        Initializes an AudioFileClip instance.

        Args:
            path (str | pathlib.Path): The path to the audio file.
            duration (int | float | None, optional): The duration of the audio file. If not provided, it will be calculated from the audio file.

        Raises:
            ValueError: If the audio file is empty and duration is not provided.
        """
        info = ffmpegio.probe.audio_streams_basic(str(path))
        if not info:
            self.fps = 44100
            self.channels = 1
            duration = (
                duration
                if duration
                else (_ for _ in ()).throw(
                    ValueError("Audio is empty and duration is not provided")
                )
            )
            super().__init__(duration, self.fps, self.channels)
        else:
            info = info[0]
            self.fps = info["sample_rate"]
            self._original_dur = info["duration"]
            self.channels = info["channels"]
            super().__init__(info["duration"], info["sample_rate"], info["channels"])
            self.path = str(path)
            self.start = info["start_time"]
            self.end = info["duration"] - info["start_time"]
            self._audio_data = ffmpegio.audio.read(str(path))[1]


class AudioArrayClip(AudioClip):
    """
    AudioArrayClip is a class that represents an audio clip from an array. It extends the AudioClip class.

    Attributes:
        fps (int): The sample rate of the audio clip.
        _original_dur (float): The original duration of the audio clip.
        channels (int): The number of channels in the audio clip.
        _audio_data (numpy.ndarray): The audio data.
        More from the AudioClip Class
    """

    def __init__(self, audio_data: np.ndarray, fps: int, duration: int | float):
        """
        Initializes an AudioArrayClip instance.

        Args:
            audio_data (np.ndarray): The audio data.
            fps (int): The sample rate of the audio clip.
            duration (int | float): The duration of the audio clip.
        """
        self.fps = fps
        self._original_dur = duration
        super().__init__(self._original_dur, self.fps)
        self.channels = audio_data.shape[1]
        self._audio_data = audio_data


def concatenate_audioclips(
    clips: list[AudioClip], fps: int | None = 44100
) -> AudioClip | AudioArrayClip:
    """
    Concatenates multiple audio clips into a single audio clip.

    Parameters:
    clips (list[AudioClip]): A list of AudioClip objects to be concatenated.
    fps (int, optional): The frames per second (fps) for the output AudioClip.
        If not provided, it defaults to 44100, or the maximum fps value found in the input clips.

    Returns:
    AudioClip | AudioArrayClip: The concatenated AudioClip. If the input clips have different
        channels, the output AudioClip will have the maximum number of channels found in the input clips,
        and the missing channels in the other clips will be filled with the mean value of their existing channels.

    Raises:
    ValueError: If no clips are provided, or if no fps value is found or set, or if a clip's channels are not set.

    Note:
    The duration of the output AudioClip is the sum of the durations of the input clips.
    If a clip's end time is set, it is used to calculate its duration; otherwise, its duration attribute is used.
    If neither is set, a ValueError is raised.
    """
    if len(clips) == 0:
        raise ValueError("No clips to concatenate")
    if len(clips) == 1:
        return clips[0].copy()
    clip: list[np.ndarray] = []
    fps = fps if fps else max([c.fps if c.fps else 0 for c in clips])
    if not fps:
        raise ValueError("No fps value found place set fps value or fps value in clips")
    duration = sum(
        [
            (
                c.end - c.start
                if c.end
                else c.duration if c.duration else (_ for _ in ()).throw(ValueError(""))
            )
            for c in clips
        ]
    )
    channels: int = max(
        [
            (
                c.channels
                if c.channels
                else (_ for _ in ()).throw(ValueError("clip channels is not set"))
            )
            for c in clips
        ]
    )
    for c in clips:
        c_channels: int = (
            c.channels
            if c.channels
            else (_ for _ in ()).throw(ValueError("clip channels is not set"))
        )
        dif_channels = channels - c_channels
        for f in c.iterate_frames_at_fps(fps):
            clip.append(np.concatenate((f, [f.mean()] * dif_channels)))
    return AudioArrayClip(np.asarray(clip), fps, duration)


def composite_audioclips(
    clips: list[AudioClip], fps: int | None = 44100, use_bg_audio: bool = False
):
    """
    Composites multiple audio clips into a single audio clip.

    Parameters:
    clips (list[AudioClip]): A list of AudioClip objects to be composited.
    fps (int, optional): The frames per second (fps) for the output AudioClip.
        If not provided, it defaults to the maximum fps value found in the input clips.
    use_bg_audio (bool, optional): If True, the first clip in the list is used as the background audio.
        The remaining clips are overlaid on top of this background audio. If False, a SilenceClip of the
        maximum duration found in the clips is used as the background audio.

    Returns:
    AudioArrayClip: The composited AudioClip. The output AudioClip will have the maximum number of channels
        found in the input clips, and the missing channels in the other clips will be filled with the mean
        value of their existing channels.

    Raises:
    ValueError: If no clips are provided, or if no fps value is found or set, or if a clip's channels are not set,
        or if no duration is found or set in the clips when use_bg_audio is False.

    Note:
    The duration of the output AudioClip is the duration of the background audio.
    If a clip's end time is set, it is used to calculate its duration; otherwise, its duration attribute is used.
    If neither is set, a ValueError is raised.
    """
    fps = int(
        fps
        or max(*(clip.fps if clip.fps else 0.0 for clip in clips), 0.0)
        or (_ for _ in ()).throw(ValueError("fps is not set"))
    )
    channels = max(*(clip.channels if clip.channels else 0 for clip in clips), 0) or (
        _ for _ in ()
    ).throw(ValueError("No Channels"))

    if use_bg_audio:
        bg_audio = clips[0]
        clips = clips[1:]
    else:
        duration = 0.0
        for clip in clips:
            if clip.end:
                duration = max(clip.end, duration)
            elif clip.duration:
                duration = max(clip.duration, duration)
            else:
                ...
        if duration == 0.0:
            raise ValueError("duration is not set of any clip")
        bg_audio = SilenceClip(duration, fps, channels)

    frames = []
    t = 0.0
    td = 1 / fps
    while t < (bg_audio.duration or (_ for _ in ()).throw(ValueError(""))):
        f: list = bg_audio.get_frame_at_t(t).tolist()
        if len(f) < channels:
            f.append((sum(f) / len(f)) * (channels - len(f)))

        for clip in clips:
            if clip.start <= t <= (clip.end or float("inf")):
                f_c = list(clip.get_frame_at_t(t))
                if len(f_c) < channels:
                    f_c.append((sum(f_c) / len(f_c)) * (channels - len(f_c)))
                for i in range(channels):
                    f[i] += (f[i] + f_c[i]) / 2
        frames.append(np.array(f))
        t += td
    return AudioArrayClip(
        np.array(frames),
        fps,
        bg_audio.duration or (_ for _ in ()).throw(ValueError("")),
    )
