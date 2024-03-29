import ctypes
from pathlib import Path
from typing_extensions import NoReturn, Self, Callable, Union
import sys

if sys.platform == "win32":
    lib = ctypes.cdll.LoadLibrary(str(Path(__file__).parent / "lib" / "Clip.dll"))
else:
    lib = ctypes.cdll.LoadLibrary(str(Path(__file__).parent / "lib" / "Clip.so"))


class Clip:
    """
    The Clip class represents a media clip that can be manipulated and processed.
    Which is the base class for all media clips in the library.

    Parameters:
        - `start: float`: The start time of the clip in seconds.
        - `end: float | None`: The end time of the clip in seconds. If None, the end time is set to -1.
        - `duration: float | None`: The duration of the clip in seconds. If None, the duration is set to -1.
        - `fps: float | None`: The frames per second (fps) of the clip. If None, the fps is set to -1.

    """

    def __init__(
        self,
        start: float = 0,
        end: Union[float, None] = -1,
        duration: Union[float, None] = -1,
        fps: Union[float, None] = -1,
    ):

        # region Ctypes_Clip_init

        lib._Clip_new.argtypes = [
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
        ]
        lib._Clip_new.restype = ctypes.c_void_p

        if end is None:
            end = -1
        if duration is None:
            duration = -1
        if fps is None:
            fps = -1

        self.obj = lib._Clip_new(start, end, duration, fps)

        # endregion

        # region Ctypes_Clip_methods

        lib._Clip_setStart.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib._Clip_setStart.restype = ctypes.c_void_p

        lib._Clip_getStart.argtypes = [ctypes.c_void_p]
        lib._Clip_getStart.restype = ctypes.c_double

        lib._Clip_setEnd.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib._Clip_setEnd.restype = ctypes.c_void_p

        lib._Clip_getEnd.argtypes = [ctypes.c_void_p]
        lib._Clip_getEnd.restype = ctypes.c_double

        lib._Clip_setDuration.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib._Clip_setDuration.restype = ctypes.c_void_p

        lib._Clip_getDuration.argtypes = [ctypes.c_void_p]
        lib._Clip_getDuration.restype = ctypes.c_double

        lib._Clip_setFps.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib._Clip_setFps.restype = ctypes.c_void_p

        lib._Clip_getFps.argtypes = [ctypes.c_void_p]
        lib._Clip_getFps.restype = ctypes.c_double

        # endregion

    # region start_property

    def set_start(self, start: Union[int, float]) -> Self:
        """
        The set_start method is used to set the start time of the clip.

        Args:
            `value: int | float`: The start time of the clip for Compositing.

        Returns:
            `Self`: For Chaining Purposes.

        Note:
            It Could Be Negative, to start playing clip early.

        """
        if start is None:
            start = 0
        return self.st_set_start(start)

    def st_set_start(self, start: float) -> Self:
        """
        The set_start method is used to set the start time of the clip.

        Args:
            `value: int | float`: The start time of the clip for Compositing.

        Returns:
            `Self`: For Chaining Purposes.

        Note:
            It Could Be Negative, to start playing clip early.
        """
        lib._Clip_setStart(self.obj, start)
        return self

    def get_start(self) -> float:
        """
        Get the start time of the clip in seconds.

        Returns:
            - `float`: The start time of the clip in seconds.

        Note:
            It Could Be Negative, to start playing clip early.
        """
        st = lib._Clip_getStart(self.obj)
        return st

    def st_get_start(self) -> float:
        """
        Get the start time of the clip in seconds.

        Returns:
            - `float`: The start time of the clip in seconds.
        """
        return lib._Clip_getStart(self.obj)

    @property
    def start(self) -> float:
        """
        Get the start time of the clip in seconds.

        Returns:
            - `float`: The start time of the clip in seconds.
        """
        return self.get_start()

    @start.setter
    def start(self, value: Union[int, float]) -> None:
        """
        The set_start method is used to set the start time of the clip.

        Args:
            `value: int | float`: The start time to set of the clip.

        Returns:
            `Self`: For Chaining Purposes.

        Note:
            It Could Be Negative, to start playing clip early.
        """
        self.st_set_start(value)

    @property
    def st_start(self) -> float:
        """
        The start property is a getter for the _st attribute.

        Returns:
            `float`: The start time of the clip.
        """
        return self.st_get_start()

    @st_start.setter
    def st_start(self, value: Union[int, float]) -> None:
        """
        The set_start method is used to set the start time of the clip.

        Args:
            `value: int | float`: The start time to set of the clip.

        Returns:
            `Self`: For Chaining Purposes.

        Note:
            It Could Be Negative, to start playing clip early.
        """
        self.st_set_start(value)

    # endregion

    # region end_property

    def set_end(self, end: Union[float, None]):
        """
        Sets the end time of the clip.

        Args:
            `end: float | None`: The end time of the clip. If None, the end time is set to -1.

        Returns:
            `Self`: For Chaining Purposes.
        """
        if end is None:
            end = -1
        return self.st_set_end(end)

    def st_set_end(self, end: float) -> Self:
        """
        Sets the end time of the clip.

        Input -1 For None.

        Parameters:
            - `end: float`: The end time of the clip.

        Returns:
            - `Self`: For chaining purposes.
        """
        lib._Clip_setEnd(self.obj, end)
        return self

    def get_end(self) -> Union[float, None]:
        """
        Get the end time of the clip.

        Returns:
            `float | None`: The end time of the clip if available, None otherwise.
        """
        end = lib._Clip_getEnd(self.obj)
        if end == -1:
            return None
        return end

    def st_get_end(self) -> float:
        """
        Get the end time of the clip.

        It Return -1 if the end is not set.

        Returns:
            `float`: The end time of the clip.
        """
        return lib._Clip_getEnd(self.obj)

    @property
    def end(self) -> Union[float, None]:
        """
        Get the end time of the clip.

        Returns None if the end is not set.

        Returns:
            `float | None`: The end time of the clip.
        """
        return self.get_end()

    @end.setter
    def end(self, value: Union[float, None]) -> None:
        """
        Set the end value of the clip.

        Args:
            `value`: The new end value for the clip.
        """
        self.set_end(value)

    @property
    def st_end(self) -> float:
        """
        Get the end time of the clip.

        Returns -1 if the end is not set.

        Returns:
            `float`: The end time of the clip.
        """
        return self.st_get_end()

    @st_end.setter
    def st_end(self, value: float) -> None:
        """
        Setter method for the st_end attribute.

        input -1 for None.

        Parameters:
            - `value`: The new value for the st_end attribute.
        """
        self.st_set_end(value)

    # endregion

    # region duration_property

    def set_duration(self, duration: Union[float, None] = None) -> NoReturn:
        """
        Setter for the duration of the clip.
        it raises a ValueError since duration is not allowed to be set.
        but you can change the duration using clip._dur = value or the _set_duration method.

        Args:
            `dur: int | float`: The duration to set for the clip.

        Returns:
            `NoReturn`: Raises a ValueError since duration is not allowed to be set.

        Raises:
            `ValueError`: If an attempt is made to set the duration, a ValueError is raised.
        """
        raise ValueError("Duration is not allowed to be set")

    def st_set_duration(self, duration: float) -> NoReturn:
        """
        Setter for the duration of the clip.
        it raises a ValueError since duration is not allowed to be set.
        but you can change the duration using clip._dur = value or the _set_duration method.

        Args:
            `dur: float`: The duration to set for the clip.

        Returns:
            `NoReturn`: Raises a ValueError since duration is not allowed to be set.

        Raises:
            `ValueError`: If an attempt is made to set the duration, a ValueError is raised.
        """
        return self.set_duration(duration)

    def _set_duration(self, value: Union[int, float]) -> Self:
        """
        Private method to set the duration of the clip.

        Args:
            `value: int | float`: The duration to set for the clip.

        Returns:
            `Self`: For Chaining Purposes.
        """
        lib._Clip_setDuration(self.obj, value)
        return self

    def get_duration(self) -> Union[float, None]:
        """
        Property that gets the duration of the clip.

        Return None if Not Set.

        Returns:
            `float | None`: The duration of the clip. If the duration is not set, it returns None.
        """
        duration = lib._Clip_getDuration(self.obj)
        if duration == -1:
            return None
        return duration

    def st_get_duration(self) -> float:
        """
        Property that gets the duration of the clip.

        return -1 if not set.

        Returns:
            `float`: The duration of the clip. If the duration is not set, it returns None.
        """
        return lib._Clip_getDuration(self.obj)

    @property
    def duration(self) -> Union[float, None]:
        """
        Property that gets the duration of the clip.

        return -1 if not set.

        Returns:
            `float`: The duration of the clip. If the duration is not set, it returns None.
        """
        return self.get_duration()

    @duration.setter
    def duration(self, value) -> NoReturn:
        """
        Setter for the duration of the clip.
        it raises a ValueError since duration is not allowed to be set.
        but you can change the duration using clip._dur = value or the _set_duration method.

        Args:
            `dur: float`: The duration to set for the clip.

        Raises:
            `ValueError`: If an attempt is made to set the duration, a ValueError is raised.
        """
        self.set_duration(value)

    @property
    def st_duration(self) -> float:
        """
        Property that gets the duration of the clip.

        return -1 if not set.

        Returns:
            `float`: The duration of the clip. If the duration is not set, it returns None.
        """
        return self.st_get_duration()

    @st_duration.setter
    def st_duration(self, value) -> None:
        """
        Setter for the duration of the clip.
        it raises a ValueError since duration is not allowed to be set.
        but you can change the duration using clip._dur = value or the _set_duration method.

        Args:
            `dur: float`: The duration to set for the clip.

        Raises:
            `ValueError`: If an attempt is made to set the duration, a ValueError is raised.
        """
        self.st_set_duration(value)

    # endregion

    # region fps_property

    def set_fps(self, fps: Union[float, None]):
        """
        Set the frames per second (fps) for the clip.

        This method allows you to set the fps for the clip. The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother playback.

        Parameters:
            `fps: int | float`: The frames per second value to set. This can be an integer or a float. For example, a value of 24 would mean 24 frames are shown per second.

        Raises:
            `TypeError`: If the provided fps value is not an integer or a float.

        Returns:
            `Self`: For Chaining Purposes.
        """
        if fps is None:
            fps = -1
        return self.st_set_fps(fps)

    def st_set_fps(self, fps: float) -> Self:
        """
        Set the frames per second (fps) for the clip.

        This method allows you to set the fps for the clip. The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother playback.

        Parameters:
            `fps: int | float`: The frames per second value to set. This can be an integer or a float. For example, a value of 24 would mean 24 frames are shown per second.

        Raises:
            `TypeError`: If the provided fps value is not an integer or a float.

        Returns:
            `Self`: Returns the instance of the class, allowing for method chaining.
        """
        lib._Clip_setFps(self.obj, fps)
        return self

    def get_fps(self) -> Union[float, None]:
        """
        Get the frames per second (fps) for the clip.

        The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother playback.

        Returns:
            `float`: The frames per second value of the clip.
        """
        fps = lib._Clip_getFps(self.obj)
        if fps == -1:
            return None
        return fps

    def st_get_fps(self) -> float:
        """
        Get the frames per second (fps) for the clip.

        The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother playback.

        return -1 if not set.

        Returns:
            `float`: The frames per second value of the clip.
        """
        return lib._Clip_getFps(self.obj)

    @property
    def fps(self) -> Union[float, None]:
        """
        property for the frames per second (fps) for the clip.

        The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother playback.

        Returns:
            `float | None`: The frames per second value of the clip `None` if not set.
        """
        return self.get_fps()

    @fps.setter
    def fps(self, value) -> None:
        """
        property the frames per second (fps) for the clip.

        This method allows you to set the fps for the clip. The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother playback.

        Parameters:
            `fps: int | float`: The frames per second value to set. This can be an integer or a float. For example, a value of 24 would mean 24 frames are shown per second.

        Raises:
            `TypeError`: If the provided fps value is not an integer or a float.
        """
        self.set_fps(value)

    @property
    def st_fps(self) -> float:
        """
        Property the frames per second (fps) for the clip.

        The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother playback.

        -1 stands for not setting.

        Returns:
            `float`: The frames per second value of the clip.
        """
        return self.st_get_fps()

    @st_fps.setter
    def st_fps(self, value) -> None:
        """
        property the frames per second (fps) for the clip.

        This method allows you to set the fps for the clip. The fps value
        determines how many frames are shown per second during playback. A higher
        fps value results in smoother playback.

        Parameters:
            `fps: int | float`: The frames per second value to set. This can be an integer or a float. For example, a value of 24 would mean 24 frames are shown per second.

        -1 stands for not setting.

        Raises:
            `TypeError`: If the provided fps value is not an integer or a float.
        """
        self.st_set_fps(value)

    # endregion

    def fx(self, func: Callable[..., Self], *args, **kwargs) -> Self:
        """
        Apply a function to the current instance and return the result.

        This method allows for the application of any callable to the current instance of the class.
        The callable should take the instance as its first argument, followed by any number of positional and keyword arguments.

        Parameters:
            func (Callable[..., Self]): The function to apply. This should take the instance as its first argument.
            *args: Variable length argument list for the function.
            **kwargs: Arbitrary keyword arguments for the function.

        Returns:
            Self: The result of applying the function to the instance.

        Example:
            >>> clip = Clip()
            >>> def do(instance):
            ...     # Do something with instance.
            ...     return instance.
            ...
            >>> new_clip = clip.fx(do)
        """
        return func(self, *args, **kwargs)

    def close(self):
        """
        Release any resources that are in use. & Delete the object.
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
