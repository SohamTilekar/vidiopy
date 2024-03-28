import ctypes
from pathlib import Path
from typing import NoReturn, Self
import sys

if sys.platform == "win32":
    lib = ctypes.cdll.LoadLibrary(str(Path(__file__).parent / "Clip.dll"))
else:
    lib = ctypes.cdll.LoadLibrary(str(Path(__file__).parent / "Clip.so"))


class Clip:
    """
    The Clip class represents a media clip that can be manipulated and processed.
    Which is the base class for all media clips in the library.

    Base: `object`

    It Was Imported from CPP Therefore None is Represented by -1 in it.
    The Method with st_ prefix means static_typed_ these method will return -1 is the parameter is not set.

    Parameters:
        - `start: float | None = -1`: The start time of the clip in seconds.
        - `end: float | None = -1`: The end time of the clip in seconds.
        - `duration: float | None = -1`: The duration of the clip in seconds.
        - `fps: float | None = -1`: The frames per second of the clip.

    Note:
        - The `duration` is not allowed to be set.
        - The `end`, `duration` and `fps` are represented by -1 under the hood if not set.

    """

    def __init__(
        self,
        start: float = 0,
        end: float | None = -1,
        duration: float | None = -1,
        fps: float | None = -1,
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

    def set_start(self, start: int | float) -> Self:
        """
        The set_start method is used to set the start time of the video clip.

        Args:
            value (int | float): The start time of the video clip.

        Returns:
            VideoClip: The instance of the VideoClip after setting the start time.
        """
        if start is None:
            start = 0
        return self.st_set_start(start)

    def st_set_start(self, start: float) -> Self:
        """
        The set_start method is used to set the start time of the video clip.

        Args:
            `value: int | float`: The start time of the video clip.

        Returns:
            `VideoClip`: The instance of the `VideoClip` after setting the start time.
        """
        lib._Clip_setStart(self.obj, start)
        return self

    def get_start(self) -> float:
        """
        Get the start time of the clip in seconds.

        Returns:
            - `float`: The start time of the clip in seconds.
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
        The start property of Video.

        Returns:
            float: The start time of the video clip.
        """
        return self.get_start()

    @start.setter
    def start(self, value: int | float) -> None:
        """
        set start of video.

        Args:
            `value: int | float`: The start time of the video clip.
        """
        self.st_set_start(value)

    @property
    def st_start(self) -> float:
        """
        The start property is a getter for the _st attribute.

        Returns:
            float: The start time of the video clip.
        """
        return self.st_get_start()

    @st_start.setter
    def st_start(self, value: int | float) -> None:
        """
        The start property is a getter for the _st attribute.

        Returns:
            int | float: The start time of the video clip.
        """
        self.st_set_start(value)

    # endregion

    # region end_property

    def set_end(self, end: float | None):
        """
        Sets the end time of the clip.

        Args:
            `end: float | None`: The end time of the clip. If None, the end time is set to -1.

        Returns:
            Self: For Chaining Pourposes.
        """
        if end is None:
            end = -1
        return self.st_set_end(end)

    def st_set_end(self, end: float) -> Self:
        """
        Sets the end time of the clip.

        Input -1 For None.

        Parameters:
        - end (float): The end time of the clip.

        Returns:
        - Self: For chaining purposes.
        """
        lib._Clip_setEnd(self.obj, end)
        return self

    def get_end(self) -> float | None:
        """
        Get the end time of the clip.

        Returns:
            float | None: The end time of the clip if available, None otherwise.
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
            float: The end time of the clip.
        """
        return lib._Clip_getEnd(self.obj)

    @property
    def end(self) -> float | None:
        """
        Get the end time of the clip.

        Returns None if the end is not set.

        Returns:
            The end time of the clip.
        """
        return self.get_end()

    @end.setter
    def end(self, value: float | None) -> None:
        """
        Set the end value of the clip.

        Args:
            value: The new end value for the clip.

        Returns:
            None
        """
        self.set_end(value)

    @property
    def st_end(self) -> float:
        """
        Get the end time of the clip.

        Returns -1 if the end is not set.

        Returns:
            float: The end time of the clip.
        """
        return self.st_get_end()

    @st_end.setter
    def st_end(self, value: float) -> None:
        """
        Setter method for the st_end attribute.

        input -1 for None.

        Parameters:
        - value: The new value for the st_end attribute.

        Returns:
        - None
        """
        self.st_set_end(value)

    # endregion

    # region duration_property

    def set_duration(self, duration: float | None) -> NoReturn:
        raise ValueError("Duration is not allowed to be set")

    def st_set_duration(self, duration: float) -> NoReturn:
        return self.set_duration(duration)

    def get_duration(self) -> float | None:
        duration = lib._Clip_getDuration(self.obj)
        if duration == -1:
            return None
        return duration

    def st_get_duration(self) -> float:
        return lib._Clip_getDuration(self.obj)

    @property
    def duration(self):
        return self.get_duration()

    @duration.setter
    def duration(self, value) -> None:
        self.set_duration(value)

    @property
    def st_duration(self) -> float:
        return self.st_get_duration()

    @st_duration.setter
    def st_duration(self, value) -> None:
        self.st_set_duration(value)

    # endregion

    # region fps_property

    def set_fps(self, fps: float | None):
        if fps is None:
            fps = -1
        return self.st_set_fps(fps)

    def st_set_fps(self, fps: float) -> Self:
        lib._Clip_setFps(self.obj, fps)
        return self

    def get_fps(self) -> float | None:
        fps = lib._Clip_getFps(self.obj)
        if fps == -1:
            return None
        return fps

    def st_get_fps(self) -> float:
        return lib._Clip_getFps(self.obj)

    @property
    def fps(self):
        return self.get_fps()

    @fps.setter
    def fps(self, value) -> None:
        self.set_fps(value)

    @property
    def st_fps(self) -> float:
        return self.st_get_fps()

    @st_fps.setter
    def st_fps(self, value) -> None:
        self.st_set_fps(value)

    # endregion
