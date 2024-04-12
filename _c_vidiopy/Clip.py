from typing_extensions import Callable, Self
from _c_vidiopy.config import lib
import ctypes


class Clip:

    def __init__(self, inherited=False):

        if inherited:
            self.c_new: Callable[[], ctypes.c_void_p] = lib.Clip_new
            self.c_new.argtypes = []
            self.c_new.restype = ctypes.POINTER(ctypes.c_void_p)

            self.obj: ctypes.c_void_p = self.c_new()

        self.c_setStart: Callable[[ctypes.c_void_p, float], None] = lib.Clip_setStart
        self.c_setStart.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_double]
        self.c_setStart.restype = None

        self.c_getStart: Callable[[ctypes.c_void_p], float] = lib.Clip_getStart
        self.c_getStart.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.c_getStart.restype = ctypes.c_double

        self.c_setEnd: Callable[[ctypes.c_void_p, ctypes.c_double], None] = (
            lib.Clip_setEnd
        )
        self.c_setEnd.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_double]
        self.c_setEnd.restype = None

        self.c_getEnd: Callable[[ctypes.c_void_p], float] = lib.Clip_getEnd
        self.c_getEnd.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.c_getEnd.restype = ctypes.c_double

        self.c_setDuration: Callable[[ctypes.c_void_p, ctypes.c_double], None] = (
            lib.Clip_setDuration
        )
        self.c_setDuration.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_double]
        self.c_setDuration.restype = None

        self.c_getDuration: Callable[[ctypes.c_void_p], float] = lib.Clip_getDuration
        self.c_getDuration.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.c_getDuration.restype = ctypes.c_double

        self.c_setFps: Callable[[ctypes.c_void_p, ctypes.c_double], None] = (
            lib.Clip_setFps
        )
        self.c_setFps.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_double]
        self.c_setFps.restype = None

        self.c_getFps: Callable[[ctypes.c_void_p], float] = lib.Clip_getFps
        self.c_getFps.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.c_getFps.restype = ctypes.c_double

        self.c_setName: Callable[[ctypes.c_void_p, ctypes.c_char_p], None] = (
            lib.Clip_setName
        )
        self.c_setName.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p]
        self.c_setName.restype = None

        self.c_getName: Callable[[ctypes.c_void_p], str] = lib.Clip_getName
        self.c_getName.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.c_getName.restype = ctypes.c_char_p

        self.c_setTimeTransforms: Callable[
            [ctypes.c_void_p, Callable[[float], float]], None
        ] = lib.Clip_setTimeTransforms
        self.c_setTimeTransforms.argtypes = [
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.py_object,
        ]
        self.c_setTimeTransforms.restype = None

    @property
    def start(self) -> float:
        return self.c_getStart(self.obj)

    @start.setter
    def start(self, value: float) -> None:
        self.c_setStart(self.obj, value)

    def get_start(self) -> float:
        return self.c_getStart(self.obj)

    def set_start(self, value: float) -> Self:
        self.c_setStart(self.obj, value)
        return self
